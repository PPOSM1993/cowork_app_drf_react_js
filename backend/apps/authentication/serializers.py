from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password2'}, label="Confirm Password")

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'rut', 'phone', 'birth_date', 'accepted_terms', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if not attrs.get("accepted_terms"):
            raise serializers.ValidationError({"accepted_terms": "Debes aceptar los términos y condiciones."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get("username")  # Puede ser email, username o rut
        password = attrs.get("password")

        user = None
        for field in ['email', 'username', 'rut']:
            try:
                user = User.objects.get(**{field: identifier})
                break
            except User.DoesNotExist:
                continue

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Usuario o contraseña incorrectos.")
        if not user.is_active:
            raise serializers.ValidationError("El usuario está inactivo.")

        data = super().validate({'username': user.email, 'password': password})
        data['user'] = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "rut": user.rut,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'rut', 'phone', 'birth_date', 'accepted_terms', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['is_active', 'is_staff', 'date_joined']
