from .views import LoginAPIView,StateViewsSet,NotificationApiView,UserUpdateView,BotViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path,include

routes = DefaultRouter()
routes.register(r'state',StateViewsSet)

bot_routes = DefaultRouter()
bot_routes.register(r'bot',BotViewSet)

urlpatterns = [
    path('login/',LoginAPIView.as_view()),
    path('notifications/',NotificationApiView.as_view()),
    path('update-profile/', UserUpdateView.as_view(), name='update-profile'),
    path('',include(routes.urls)),
    path('bot/',include(bot_routes.urls))
]
