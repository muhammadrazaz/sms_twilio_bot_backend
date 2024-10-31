from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets,status
from rest_framework.views import APIView
from .serializers import TaskSerializer
from django.shortcuts import render
from datetime import datetime
from .models import Task




class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
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

        filter_conditions['user'] = self.request.user
        queryset = Task.objects.filter(**filter_conditions)
        return queryset
    

class TaskFilterApiView(APIView):
    def get(self,request):
   
        # tasks = Task.objects.filter(start_date__gte=datetime.now().date()).values_list('start_date', flat=True)
        # distinct_start_dates = set(tasks)
        # distinct_start_dates_list = sorted(distinct_start_dates)


        response = {
            'status' : Task.get_status_choices(),
            'category': Task.get_category_choices(),
            'priority' : Task.get_priority_choices(),
            # 'start_date' :  distinct_start_dates_list,
            }

        return Response(response,status=status.HTTP_200_OK)