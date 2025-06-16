from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import date

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name',
            'rut', 'phone', 'birth_date',
            'accepted_terms', 'password', 'password2'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        if not attrs.get("accepted_terms"):
            raise serializers.ValidationError({"accepted_terms": "Debes aceptar los términos y condiciones."})
        return attrs

    def validate_birth_date(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("Debes tener al menos 18 años.")
        return value

    def validate_rut(self, value):
        if User.objects.filter(rut=value).exists():
            raise serializers.ValidationError("Este RUT ya está registrado.")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.first_name
        token['is_staff'] = user.is_staff
        return token


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Email, Username o RUT")
    password = serializers.CharField(label="Contraseña", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Credenciales inválidas.")
        else:
            raise serializers.ValidationError("Se requieren 'username' y 'password'.")

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'rut', 'phone', 'birth_date',
            'accepted_terms', 'is_active', 'is_staff', 'date_joined'
        ]
        read_only_fields = ['is_active', 'is_staff', 'date_joined']
