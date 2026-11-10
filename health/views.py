"""
Vistas de la app `health`.

Endpoint único de comprobación del servidor (health-check).
"""

from rest_framework.response import Response
from rest_framework.views import APIView


class HealthView(APIView):
    """GET: health-check. Devuelve un JSON simple que confirma el estado del server."""

    def get(self, request):
        return Response({"servidor": "okay"})
