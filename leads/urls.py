from .views import BotLeadViewSet,LeadViewSet,BotShippingViewSet,ShippingViewSet,ShippingFilterOptionsApiView,LeadFilterOptionsApiView,DashboardApiView,BotStateViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path,include

routes = DefaultRouter()
routes.register(r'leads',LeadViewSet,basename='leads')
routes.register(r'shippings',ShippingViewSet,basename='shippings')

bot_routes = DefaultRouter()
bot_routes.register(r'leads',BotLeadViewSet,basename='bot-leads')
bot_routes.register(r'shippings',BotShippingViewSet,basename='bot-shippings')
bot_routes.register(r'states',BotStateViewSet)


urlpatterns = [
    path('',include(routes.urls)),
    path('bot/',include(bot_routes.urls)),
    path('lead/filter-options',LeadFilterOptionsApiView.as_view()),
    path('shipping/filter-options',ShippingFilterOptionsApiView.as_view()),
    path('dashboard/',DashboardApiView.as_view())
]
