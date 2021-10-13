from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer, ChangePasswordSerializer, \
    ResetPasswordSerializer, CompleteResetPasswordSerializer
from .permissions import IsActivePermission


class RegistrationView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(
                "Account successfully created", status=201
            )


class ActivationView(APIView):

    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
            return Response(
                "Account successfully activated", status=200
            )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

# Если вам нужно передать request в сериализаторы то нужно переопределить методы get_serializer_context & get_serializer


class LogoutView(APIView):

    permission_classes = (IsActivePermission, )

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response("Successfully logged out")


class ChangePasswordView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                "Password successfully updated"
            )


class ResetPasswordView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response(
                "Password reset message was sent to your email"
            )


class CompleteResetPasswordView(APIView):

    def post(self, request):
        serializer = CompleteResetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Password successfully reset'
            )