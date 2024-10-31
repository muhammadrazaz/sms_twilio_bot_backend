from .views import TaskViewSet,TaskFilterApiView
from rest_framework.routers import DefaultRouter
from django.urls import path,include

routes = DefaultRouter()

routes.register(r'task',TaskViewSet,basename='task')

urlpatterns = [
    path('',include(routes.urls)),
    path('task/fitler-options',TaskFilterApiView.as_view()),

]

