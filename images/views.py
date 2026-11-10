"""
Vistas de la app `images`.

Subida, lista y detalle de imágenes mediante APIViews de DRF.
Los archivos NO tocan el disco del server: django-storages los sube
directamente al bucket AWS S3. No define `permission_classes`: por
defecto cualquier usuario puede leer y subir (AllowAny).
"""

from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import Imagen
from .serializers import ImagenSerializer


class CrearImagenView(APIView):
    """POST (multipart/form-data): subir una imagen al bucket S3."""

    # DRF: los FileField/ImageField requieren MultiPartParser (docs de DRF).
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = ImagenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()                        # INSERT + upload al bucket
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class ListarImagenesView(APIView):
    """GET: listar todas las imágenes, ordenadas por fecha de creación."""

    def get(self, request):
        imagenes = Imagen.objects.all().order_by('-fecha_creacion')  # SELECT * ORDER BY
        serializer = ImagenSerializer(imagenes, many=True, context={'request': request})
        return Response(serializer.data)


class ObtenerImagenView(APIView):
    """GET: ver una imagen específica por su UUID."""

    def get(self, request, pk):
        imagen = get_object_or_404(Imagen, pk=pk)  # SELECT ... WHERE id = pk
        serializer = ImagenSerializer(imagen, context={'request': request})
        return Response(serializer.data)
