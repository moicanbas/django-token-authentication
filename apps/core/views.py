from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from django.core.exceptions import ValidationError

class BaseModelView(viewsets.ModelViewSet):
    model = None
    serializer_class = None
    
    def get(self, request, pk=None, *args, **kwargs):
        try:
            if pk:
                instance = get_object_or_404(self.model, pk=pk)
                serializer = self.serializer_class(instance)
            else:
                queryset = self.model.objects.filter(active = True)
                serializer = self.serializer_class(queryset, many=True)
            return Response({
                "success": True,
                "count": len(serializer.data),
                "results": serializer.data
            })
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Registro almacenado exitosamente"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk=None, *args, **kwargs):
        if not pk:
            return Response({"error": "Method PUT not allowed without a pk"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = get_object_or_404(self.model, pk=pk)
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Registro actualizado exitosamente"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None, *args, **kwargs):
        if not pk:
            return Response({"error": "Method DELETE not allowed without a pk"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        try:
            instance = get_object_or_404(self.model, pk=pk)
            if not instance.active:
                return Response({"error": "No se encontró registro con este ID"}, status=status.HTTP_400_BAD_REQUEST)
            instance.active = False
            instance.save()
            return Response( {"message": "Registro eliminado exitosamente"}, status=status.HTTP_204_NO_CONTENT)
        except self.model.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
