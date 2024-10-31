from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from .serializer import AgentSerializer
from django.shortcuts import render
from auth_app.models import State
from .models import AgentProfile
from django.db.models import F
from datetime import datetime




class AgentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = AgentSerializer
    # queryset = AgentProfile.objects.all()
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
        queryset = AgentProfile.objects.select_related('user').filter(**filter_conditions).annotate(
        username=F('user__username'),
        email=F('user__email')
        ).order_by('-created_at')
        return queryset

    

class AgentFilterOptionApiView(APIView):
    def get(self,request):
        response = {
            'states' : State.objects.all().order_by('state_name').values_list('state_name',flat=True) 
        }

        return Response(response,status=status.HTTP_200_OK)

    
