from rest_framework import viewsets
from .models import Address
from .serializers import AddressSerializer
from rest_framework.parsers import MultiPartParser, FormParser


class AddressViewSet(viewsets.ModelViewSet):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer
    parser_classes=(MultiPartParser,FormParser)
