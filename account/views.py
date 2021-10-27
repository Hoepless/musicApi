from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer, CompleteResetPasswordSerializer, ResetPasswordSerializer


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response("Successfully registered", 201)


class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = User.objects.filter(
            email=email,activation_code=activation_code
        ).first()
        message = (
            "User does not exists",
            "Successfully activated",
                   )
        if not user:
            return Response(message[0], 400)
        user.activation_code = ""
        user.is_active = True
        user.save()
        return Response(message[-1], 200)


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