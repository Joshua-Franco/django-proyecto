from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cuenta
from .serializers import CuentaSerializer


class CuentaListCreateView(APIView):
    """GET: listar todas las cuentas. POST: crear una cuenta."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        cuentas = Cuenta.objects.all()                        # SELECT *
        serializer = CuentaSerializer(cuentas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CuentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()                                 # INSERT
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuentaDetailView(APIView):
    """GET: ver una cuenta. PUT/PATCH: actualizar. DELETE: eliminar."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Cuenta, pk=pk)               # SELECT ... WHERE id = pk

    def get(self, request, pk):
        cuenta = self.get_object(pk)
        serializer = CuentaSerializer(cuenta)
        return Response(serializer.data)

    def put(self, request, pk):
        cuenta = self.get_object(pk)
        serializer = CuentaSerializer(cuenta, data=request.data)
        if serializer.is_valid():
            serializer.save()                                 # UPDATE
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        cuenta = self.get_object(pk)
        serializer = CuentaSerializer(cuenta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cuenta = self.get_object(pk)
        cuenta.delete()                                       # DELETE
        return Response(status=status.HTTP_204_NO_CONTENT)