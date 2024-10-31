
from .serializers import LoginSerializer,StateSerializer,UserUpdateSerializer,BotDetailSerializer
from rest_framework.generics import GenericAPIView,UpdateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import viewsets,status
from .models import State,Notification,Bot
from .bot_auth import TokenAuthentication
from rest_framework.views import APIView


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # Get the serializer and validate the data
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            username = data['username']
            password = data['password']


            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)  # Convert to string
                refresh_token = str(refresh)  # Convert to string

               
                user_data = self.get_serializer(user).data
                
                # Manually add tokens to the response
                user_data['access_token'] = access_token
                user_data['refresh_token'] = refresh_token
                

                #Get User role
                role = user.groups.filter().first()
                user_data['role'] = role.name if role else ''

                return Response(user_data, status=status.HTTP_200_OK)

            return Response({'username': 'No active account found with the given credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
   

    def get_object(self):
        return self.request.user
    


class StateViewsSet(viewsets.ModelViewSet):
    permission_classes  = [IsAuthenticated]
    serializer_class = StateSerializer
    queryset = State.objects.all().order_by('state_name')


class NotificationApiView(APIView):
    # permission_classes = [AllowAny]

    def get(self,request):
        unread_notification = Notification.objects.filter(user=request.user,is_read = False).count()
        notifications = Notification.objects.filter(user=request.user).values('title','description','created_at','is_read').order_by('-created_at')

        response = {
            'notifications' : notifications,
            'unread_notification' : unread_notification
        }
        return Response(response,status=status.HTTP_200_OK)
    
    def post(self,request):
        Notification.objects.filter(user=request.user,is_read = False).update(is_read = True)
        return Response({"message":"success"},status=status.HTTP_200_OK)



class BotViewSet(viewsets.ModelViewSet):
    serializer_class = BotDetailSerializer
    authentication_classes = [TokenAuthentication]
    queryset = Bot.objects.filter()