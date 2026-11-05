"""
Vistas de la app `accounts`.

CRUD de cuentas mediante APIViews de DRF (una vista por operación).
`CrearCuentaView`, `ListarCuentasView` y `ObtenerCuentaView` son públicas.
`ActualizarCuentaView` y `EliminarCuentaView` requieren token JWT (simplejwt).
`EliminarCuentaView` hace borrado lógico (solo pone `activo=False`).
Solo se listan/consultan/actualizan cuentas activas (`activo=True`).
`IniciarSesionView` es el endpoint de login JWT.
"""

from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Cuenta
from .serializers import CuentaSerializer


class CrearCuentaView(APIView):
    """POST: crear una cuenta."""

    def post(self, request):
        serializer = CuentaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()                                 # INSERT
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarCuentasView(APIView):
    """GET: listar todas las cuentas activas."""

    def get(self, request):
        cuentas = Cuenta.objects.filter(activo=True)          # SELECT * WHERE activo = True
        serializer = CuentaSerializer(cuentas, many=True)
        return Response(serializer.data)


class ObtenerCuentaView(APIView):
    """GET: obtener una cuenta activa por su id."""

    def get(self, request, pk):
        cuenta = get_object_or_404(Cuenta, pk=pk, activo=True)  # SELECT ... WHERE id = pk AND activo = True
        serializer = CuentaSerializer(cuenta)
        return Response(serializer.data)


class ActualizarCuentaView(APIView):
    """PUT: reemplazo completo. PATCH: actualización parcial."""

    # Requiere token JWT válido (simplejwt).
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        cuenta = get_object_or_404(Cuenta, pk=pk, activo=True)
        serializer = CuentaSerializer(cuenta, data=request.data)
        if serializer.is_valid():
            serializer.save()                                 # UPDATE
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        cuenta = get_object_or_404(Cuenta, pk=pk, activo=True)
        serializer = CuentaSerializer(cuenta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()                                 # UPDATE parcial
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EliminarCuentaView(APIView):
    """DELETE: desactivar una cuenta (borrado lógico, no elimina de la BD)."""

    # Requiere token JWT válido (simplejwt).
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        cuenta = get_object_or_404(Cuenta, pk=pk, activo=True)
        cuenta.activo = False                                 # Borrado lógico
        cuenta.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IniciarSesionView(TokenObtainPairView):
    """POST: iniciar sesión y obtener tokens JWT (access + refresh)."""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
