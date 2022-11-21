from rest_framework import viewsets, mixins
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from .models import User
from api.permissions import IsAdminOrSuperUser
from .serializers import UserSerializer, UserMeSerializer, CustomTokenObtainPairSerializer, SignupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdminOrSuperUser, ]


class UserMeViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet
    ):
    queryset = User.objects.all()
    serializer_class = UserMeSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(username=self.request.user.username)
        self.check_object_permissions(self.request, obj)
        return obj


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny,]


class SignupViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            email = serializer.initial_data['email']
            username = serializer.initial_data['username']
        except KeyError:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        if not User.objects.filter(username=username, email=email).exists():
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        confirmation_code = get_random_string(length=6)
        User.objects.filter(username=username).update(confirmation_code=confirmation_code)
        send_mail(
            'Ваш код подтверждения',
            f'"confirmation_code": "{confirmation_code}"',
            'from@example.com',
            [f'{email}'],
            fail_silently=False,
        )
        headers = self.get_success_headers(serializer.initial_data)
        return Response(serializer.initial_data, status=status.HTTP_200_OK, headers=headers)
        

    def perform_create(self, serializer):
        email = serializer.validated_data['email']
        confirmation_code = get_random_string(length=6)
        send_mail(
            'Ваш код подтверждения',
            f'"confirmation_code": "{confirmation_code}"',
            'from@example.com',
            [f'{email}'],
             fail_silently=False,
        )
        serializer.save(confirmation_code=confirmation_code)