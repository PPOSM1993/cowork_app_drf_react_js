from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils.dateparse import parse_date
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from apps.employee.models import Employee
from apps.identity_verification.models import IdentityVerification
from apps.recommendation.models import Recommendation
from apps.chat.models import Message


User = get_user_model()


class AdvancedAnalyticsDashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        start_date = parse_date(request.query_params.get('start_date'))  # formato: YYYY-MM-DD
        end_date = parse_date(request.query_params.get('end_date'))

        messages_qs = Message.objects.all()
        if start_date:
            messages_qs = messages_qs.filter(created_at__gte=start_date)
        if end_date:
            messages_qs = messages_qs.filter(created_at__lte=end_date)

        # Conteos generales
        data = {
            'total_users': User.objects.count(),
            'active_employees': Employee.objects.filter(is_active=True).count(),
            'verified_users': IdentityVerification.objects.filter(status='approved').count(),
            'active_recommendations': Recommendation.objects.filter(is_active=True).count(),
            'total_messages': messages_qs.count(),
        }

        # Ranking: top usuarios con más mensajes
        top_users = messages_qs.values('sender__id', 'sender__email').annotate(
            total_messages=Count('id')
        ).order_by('-total_messages')[:5]

        data['top_users_by_messages'] = list(top_users)

        # Reportes por semana
        messages_per_week = messages_qs.extra({
            'week': "strftime('%%Y-%%W', created_at)"
        }).values('week').annotate(total=Count('id')).order_by('week')

        data['messages_per_week'] = list(messages_per_week)

        # Reportes por mes
        messages_per_month = messages_qs.extra({
            'month': "strftime('%%Y-%%m', created_at)"
        }).values('month').annotate(total=Count('id')).order_by('month')

        data['messages_per_month'] = list(messages_per_month)

        return Response(data)
