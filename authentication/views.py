from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import serializers
from django.contrib.auth.models import User
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self,attrs):
        data=super().validate(attrs)
        data['role']=self.user.role
        return data
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logged_in_user(request):
    return Response({"message":"User is logged in"},status=status.HTTP_200_OK)


# class UserReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields="__all__"
# class UserReadView(ListAPIView):
#     queryset=User.objects.all()
#     serializer_class=UserReadSerializer