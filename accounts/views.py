"""
Vistas de la app `accounts`.

CRUD de cuentas mediante APIViews de DRF (una vista por operación).
`CrearCuentaView`, `ListarCuentasView` y `ObtenerCuentaView` son públicas.
`ActualizarCuentaView` y `EliminarCuentaView` requieren token JWT (simplejwt).
`EliminarCuentaView` hace borrado lógico (solo pone `activo=False`).
Solo se listan/consultan/actualizan cuentas activas (`activo=True`).
"""

import bcrypt
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from .models import Cuenta
from .serializers import (
    CuentaSerializer,
    CrearCuentaSerializer,
    IniciarSesionSerializer,
)


class CuentaJWTAuthentication(JWTAuthentication):
    """Autentica tokens de cuentas cuyo ID es UUID."""

    def get_user(self, validated_token):
        user_id = validated_token.get(api_settings.USER_ID_CLAIM)
        if user_id is None:
            raise AuthenticationFailed("El token no contiene un ID.")

        try:
            return Cuenta.objects.get(pk=user_id, activo=True)
        except (Cuenta.DoesNotExist, ValueError, ValidationError) as exc:
            raise AuthenticationFailed(
                "La cuenta no existe o está inactiva."
            ) from exc


class CrearCuentaView(APIView):
    """POST: crear una cuenta y devolver token de acceso."""
    def post(self, request):
        serializer = CrearCuentaSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Devolver los datos de la cuenta y solo el token 'access'.
            access_token = AccessToken.for_user(user)

            return Response({
                **serializer.data,
                'access': str(access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IniciarSesionView(APIView):
    """POST: autenticar una cuenta y devolver su token de acceso."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = IniciarSesionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data
        cuenta = Cuenta.objects.filter(
            nombre=datos['nombre'],
            correo_electronico__iexact=datos['correo_electronico'],
            activo=True,
        ).first()
        if cuenta is None:
            return Response(
                {'detail': 'Credenciales inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            is_valid = bcrypt.checkpw(
                datos['password'].encode('utf-8'),
                cuenta.password.encode('ascii'),
            )
        except ValueError:
            is_valid = False
        if not is_valid:
            return Response(
                {'detail': 'Credenciales inválidas.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response({'access': str(AccessToken.for_user(cuenta))})


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

    authentication_classes = [CuentaJWTAuthentication]
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

    authentication_classes = [CuentaJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        cuenta = get_object_or_404(Cuenta, pk=pk, activo=True)
        cuenta.activo = False                                 # Borrado lógico
        cuenta.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
