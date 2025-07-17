import datetime
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import APIKey, APIAccessLog
from django.utils.timezone import now

class APIKeyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Solo proteger rutas que empiecen con /api/ (ajusta según necesidad)
        if not request.path.startswith('/api/'):
            return None

        api_key_value = request.headers.get('X-API-KEY')
        if not api_key_value:
            return JsonResponse({'detail': 'API key requerida.'}, status=401)

        try:
            api_key = APIKey.objects.get(key=api_key_value, is_active=True)
        except APIKey.DoesNotExist:
            return JsonResponse({'detail': 'API key inválida o inactiva.'}, status=403)

        # Verificar expiración
        if api_key.expires_at and api_key.expires_at < now():
            return JsonResponse({'detail': 'API key expirada.'}, status=403)

        # Contar llamadas hoy
        today_start = now().replace(hour=0, minute=0, second=0, microsecond=0)
        usage_count = APIAccessLog.objects.filter(api_key=api_key, timestamp__gte=today_start).count()
        if usage_count >= api_key.usage_limit_per_day:
            return JsonResponse({'detail': 'Límite diario de uso excedido.'}, status=429)

        # Guardar api_key en request para uso en vistas si es necesario
        request.api_key = api_key

        return None

    def process_response(self, request, response):
        # Registrar el acceso si existe api_key en request
        api_key = getattr(request, 'api_key', None)
        if api_key:
            APIAccessLog.objects.create(
                api_key=api_key,
                endpoint=request.path,
                method=request.method,
                success=200 <= response.status_code < 300,
                response_code=response.status_code,
                ip_address=self.get_client_ip(request),
            )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')