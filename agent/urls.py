from .views import AgentViewSet,AgentFilterOptionApiView
from rest_framework.routers import DefaultRouter
from django.urls import path,include
routes = DefaultRouter()


routes.register(r'agent',AgentViewSet,basename='agent')


urlpatterns = [
    path('',include(routes.urls)),
    path('agent/filter-options',AgentFilterOptionApiView.as_view())
]
