from rest_framework import serializers
from django.core.mail import send_mail


from .models import User
from .tasks import send_activation_code_task, send_beat_mail_task


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirmation = serializers.CharField(min_length=4, required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            "email", "password",
            "password_confirmation"
        )

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.pop('password_confirmation')
        if password != password_confirmation:
            message = "Passwords do not match"
            raise serializers.ValidationError(message)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_task.delay(user.email, user.activation_code)
        send_beat_mail_task.delay(user.email)
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Given user is not exists")
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Password reset',
            f'your reset code: {user.activation_code}',
            'test@gmail.com',
            [user.email]
        )


class CompleteResetPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=4)
    password_confirmation = serializers.CharField(required=True, min_length=4)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        password1 = data.get('password')
        password2 = data.get('password_confirmation')

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError("Wrong email or activation code")

        if password1 != password2:
            raise serializers.ValidationError("Unmatched passwords!")
        return data

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
