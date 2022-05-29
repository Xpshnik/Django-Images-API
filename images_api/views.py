from rest_framework import generics, permissions
from .serializers import ImageSerializer
from .models import Image

# Create your views here.
class ImageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)