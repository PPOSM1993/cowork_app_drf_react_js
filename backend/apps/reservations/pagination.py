from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # permite ajustar desde frontend ?page_size=20
    max_page_size = 100