"""
Vistas de la app `videos`.

Subida, lista y detalle de videos mediante APIViews de DRF.
Los archivos NO tocan el disco del server: django-storages los sube
directamente al bucket AWS S3. No define `permission_classes`: por
defecto cualquier usuario puede leer y subir (AllowAny).
"""

from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import Video
from .serializers import VideoSerializer


class CrearVideoView(APIView):
    """POST (multipart/form-data): subir un video al bucket S3."""

    # DRF: los FileField requieren MultiPartParser (docs de DRF).
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()                        # INSERT + upload al bucket
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListVideoView(APIView):
    """GET: listar todos los videos, ordenados por fecha de creación."""

    def get(self, request):
        videos = Video.objects.all().order_by('-fecha_creacion')  # SELECT * ORDER BY
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return Response(serializer.data)


class ObtenerVideoView(APIView):
    """GET: ver un video específico por su UUID."""

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)  # SELECT ... WHERE id = pk
        serializer = VideoSerializer(video, context={'request': request})
        return Response(serializer.data)
