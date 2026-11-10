"""
Vistas de la app `tasks`.

CRUD completo de tareas mediante APIViews de DRF.
No define `permission_classes`: por defecto cualquier usuario puede
leer y escribir (AllowAny).
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tarea
from .serializers import TareaSerializer


class CrearTareaView(APIView):
    """POST: crear una tarea."""

    def post(self, request):
        serializer = TareaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()                                   # INSERT
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListarTareasView(APIView):
    """GET: listar todas las tareas, ordenadas por fecha de creación."""

    def get(self, request):
        tareas = Tarea.objects.all().order_by('-fecha_creacion')  # SELECT * ORDER BY
        serializer = TareaSerializer(tareas, many=True)
        return Response(serializer.data)


class ActualizarTareaView(APIView):
    """GET: ver una tarea. PUT: reemplazo completo. PATCH: actualización parcial."""

    def get(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)               # SELECT ... WHERE id = pk
        serializer = TareaSerializer(tarea)
        return Response(serializer.data)

    def put(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        serializer = TareaSerializer(tarea, data=request.data)
        if serializer.is_valid():
            serializer.save()                                  # UPDATE
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        serializer = TareaSerializer(tarea, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()                                  # UPDATE parcial
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EliminarTareaView(APIView):
    """DELETE: eliminar una tarea."""

    def delete(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk)
        tarea.delete()                                         # DELETE
        return Response(status=status.HTTP_204_NO_CONTENT)
