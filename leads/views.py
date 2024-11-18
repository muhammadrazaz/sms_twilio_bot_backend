from .serializers import BotLeadSerializer,LeadSerializer,BotShippingSerializer,ShippingSerializer,BotStateSerializer
from django.db.models import Case, When, Value, CharField,F,Count
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db.models.functions import Concat,ExtractMonth
from auth_app.bot_auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from django.shortcuts import render
from auth_app.models import State
from .models import Lead,Shipping
from calendar import month_abbr
from datetime import datetime
from task.models import Task

class LeadFilterOptionsApiView(APIView):
    def get(self,request):
        response ={
            'status' : Lead.get_status_choices(),
            'state_names':State.objects.all().values_list('state_name',flat=True)
        }

        return Response(response,status=status.HTTP_200_OK)

class ShippingFilterOptionsApiView(APIView):
    def get(self,request):
        response ={
            'status' : Shipping.get_status_choices()
        }

        return Response(response,status=status.HTTP_200_OK)


class DashboardApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        lead_filter_options = {

        }
        state_filter_options = {}
        user = request.user
        
        if not user.groups.filter(name="admin").exists():
            user_states = user.agentprofile.states.values_list('state_name', flat=True)
            lead_filter_options['states__state_name__in'] = user_states
            state_filter_options['state_name__in'] = user_states
            

        recent_leads = Lead.objects.filter(**lead_filter_options).annotate(
            preferred_contact=Case(
                When(whatsapp__isnull=False, whatsapp__gt="", then=Concat(Value("whatsapp: "),F('whatsapp'))),
                When(sms__isnull=False, sms__gt="", then=Concat(Value("sms: "), F('sms'))),
                When(email__isnull=False, email__gt="", then=Concat(Value("email: ") , F('email'))),
                When(discord__isnull=False, discord__gt="", then=Concat(Value("discord: ") , F('discord'))),
                When(instagram__isnull=False, instagram__gt="", then=Concat(Value("instagram: ") , F('instagram'))),
                default=Value("No preferred contact"),
                output_field=CharField(),
            ),
            # state_names = Subquery(Concat(State.objects.filter(lead=OuterRef('id')).values_list('state_name',flat=True)))

        ).values('id','user_id', 'preferred_contact', 'status').order_by('-created_at')[:5]

        for lead in recent_leads: 
            lead['states'] = ", ".join([state.state_name for state in State.objects.filter(lead=lead['id'])])

        leads_by_states = dict(State.objects.filter(**state_filter_options).annotate(lead_count=Count('lead')).values_list('state_name', 'lead_count'))

        lead_count_by_state = {
            'label':[],
            'data':[]
        }
        for state_name,state_data in leads_by_states.items():
            lead_count_by_state['label'].append(state_name)
            lead_count_by_state['data'].append(state_data)

        months = [ month_abbr[i] for i in range(1, 13)]
        lead_counts = dict(
                Lead.objects
                .filter(**lead_filter_options)
                .annotate(month=ExtractMonth('created_at'))  # Assuming you have a created_at field
                .values('month')
                .annotate(count=Count('id'))
                .values_list('month','count')
            )
        
        shipping_counts = dict(
                Shipping.objects
                .filter()
                .annotate(month=ExtractMonth('created_at'))  # Assuming you have a created_at field
                .values('month')
                .annotate(count=Count('id'))
                .values_list('month','count')
            )
        lead_counts_by_month = {
            'label':[],
            'data' :[]
        }
        
        for i in range(0,len(months)):
            lead_counts_by_month['label'].append(months[i])
            lead_counts_by_month['data'].append(lead_counts.get(i+1,0) + shipping_counts.get(i+1,0) )

      
        lead_counts_by_status = dict(
            Lead.objects
            .filter(**lead_filter_options)
            .values('status')  
            .annotate(count=Count('id'))
            .values_list('status','count')
        )

        shipping_counts_by_status = dict(
            Shipping.objects
            .filter()
            .values('status')  
            .annotate(count=Count('id'))
            .values_list('status','count')
        )
        lead_by_status = {
            'label':[],
            'data': []
        }
        for lead_status in Lead.get_status_choices():
            lead_by_status['label'].append(lead_status)
            lead_by_status['data'].append(lead_counts_by_status.get(lead_status.replace(' ','_').lower(),0) + shipping_counts_by_status.get(lead_status.replace(' ','_').lower(),0))

        task_counts_by_status = dict(
            Task.objects
            .filter(user=user)
            .values('status')  
            .annotate(count=Count('id'))
            .values_list('status','count')
        )

        task_by_status = {
            'label':[],
            'data': []
        }
        for task_status in Task.get_status_choices():
            task_by_status['label'].append(task_status)
            task_by_status['data'].append(task_counts_by_status.get(task_status.replace(' ','_').lower(),0))

        




        response = {
            'recent_leads':recent_leads,
            'lead_counts_by_states' : lead_count_by_state,
            'lead_counts_by_month':lead_counts_by_month,
            'lead_by_status' : lead_by_status,
            'task_by_status' : task_by_status
        }
        return Response(response,status=status.HTTP_200_OK)

class LeadViewSet(viewsets.ModelViewSet):
    serializer_class = LeadSerializer
    # permission_classes = [AllowAny]

    def get_queryset(self):
        dates = self.request.GET.getlist('dates[]')
        filter_conditions = {}
        
        if dates:
            start_date  = datetime.strptime(dates[0], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            end_date = datetime.strptime(dates[1], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            
            filter_conditions = {
            'created_at__date__gte': start_date,
            'created_at__date__lte': end_date,
            }

        user = self.request.user
        if not user.groups.filter(name="admin").exists():
            user_states = user.agentprofile.states.values_list('state_name', flat=True)
            filter_conditions['states__state_name__in'] = user_states


        queryset = Lead.objects.filter(**filter_conditions).order_by('-created_at')
        queryset_with_states = []
        for query in queryset:
            states = State.objects.filter(lead = query.id).values_list('state_name',flat=True)
        
            query.state_names = states
            queryset_with_states.append(query)
            
        return queryset_with_states

    def get_object(self):
        pk = self.kwargs.get('pk')
       
        queryset = Lead.objects.get(pk=pk)
        
        states = State.objects.filter(lead = queryset.id).values_list('state_name',flat=True)

        queryset.state_names = states
        return queryset
    
class ShippingViewSet(viewsets.ModelViewSet):
    serializer_class = ShippingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        dates = self.request.GET.getlist('dates[]')
        filter_conditions = {}
        if dates:
            start_date  = datetime.strptime(dates[0], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            end_date = datetime.strptime(dates[1], "%Y-%m-%dT%H:%M:%S.%fZ").date()
    
            filter_conditions = {
            'created_at__date__gte': start_date,
            'created_at__date__lte': end_date,
            }

        
        
        queryset = Shipping.objects.filter(**filter_conditions).order_by('-created_at')
        return queryset






class BotLeadViewSet(viewsets.ModelViewSet):
    serializer_class = BotLeadSerializer
    authentication_classes = [TokenAuthentication]
    

    def get_queryset(self):
        
        queryset = Lead.objects.all()
        queryset_with_states = []
        for query in queryset:
            states = State.objects.filter(lead = query.id).values_list('state_name',flat=True)
        
            query.user_states = ','.join(states)
            queryset_with_states.append(query)
            
        return queryset_with_states

    def get_object(self):
        pk = self.kwargs.get('pk')
  
        queryset = Lead.objects.get(pk=pk)
        
        states = State.objects.filter(lead = queryset.id).values_list('state_name',flat=True)

        queryset.user_states = ','.join(states)
        return queryset
    
class BotShippingViewSet(viewsets.ModelViewSet):
    serializer_class = BotShippingSerializer
    authentication_classes = [TokenAuthentication]
    queryset = Shipping.objects.all()


class BotStateViewSet(viewsets.ModelViewSet):
    serializer_class = BotStateSerializer
    authentication_classes = [TokenAuthentication]
    queryset = State.objects.all()
    
    


    