from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm Password")

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

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.USERNAME_FIELD

    def validate(self, attrs):
        # Aquí validamos manualmente email/username/rut para login
        credentials = attrs.get("username"), attrs.get("password")
        username_or_email_or_rut = attrs.get("username")

        user = None
        # Intentamos obtener el usuario por email, username o rut
        try:
            user = User.objects.get(email=username_or_email_or_rut)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username_or_email_or_rut)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(rut=username_or_email_or_rut)
                except User.DoesNotExist:
                    pass

        if user is None:
            raise serializers.ValidationError('Usuario o contraseña incorrectos.')

        if not user.check_password(attrs.get('password')):
            raise serializers.ValidationError('Usuario o contraseña incorrectos.')

        if not user.is_active:
            raise serializers.ValidationError('Usuario inactivo.')

        data = super().validate({'username': user.email, 'password': attrs.get('password')})

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
