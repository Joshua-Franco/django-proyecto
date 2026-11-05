"""
Vistas de la app `api`.

Endpoint único de comprobación del servidor.
"""

from rest_framework.response import Response
from rest_framework.views import APIView


class HomeView(APIView):
    """GET: health-check. Devuelve un JSON simple que confirma el estado del servidor."""

    def get(self, request):
        return Response({"servidor": "okay"})
