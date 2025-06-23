from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics, permissions, filters
from .pagination import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
class BranchesListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        branch = Branch.objects.all()
        serializer = BranchSerializer(branch, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Filtros y búsqueda
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'address', 'email', 'phone']
    search_fields = ['name', 'address']
    ordering_fields = ['capacity', 'email', 'phone']
    ordering = ['name']
    pagination_class = CustomPagination

class CreateBranchesAPIView(CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteBranches(request, pk):
    try:
        branch = Branch.objects.get(pk=pk)
    except Branch.DoesNotExist:
        return Response({"error": "Rama no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    branch.delete()
    return Response({"message": "Rama eliminada correctamente"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SearchBranch(request):
    query = request.GET.get('q', '')
    if query:
        customers = Branch.objects.filter(
            name__icontains=query
        ) | Branch.objects.filter(
            address__icontains=query  
        ) | Branch.objects.filter(
            email__icontains=query
        ) | Branch.objects.filter(
            phone__icontains=query
        )
    else:
        branches = Branch.objects.all()

    serializer = BranchSerializer(branches, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def BranchesDetail(request, pk):
    try:
        branch = Branch.objects.get(pk=pk)
    except Branch.DoesNotExist:
        return Response({"error": "Rama no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BranchSerializer(branch)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BranchSerializer(branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)