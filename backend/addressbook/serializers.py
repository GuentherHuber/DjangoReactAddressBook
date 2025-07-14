from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
            model=Address
            fields=['id','first_name','last_name','city','street_name','house_number','postcode','profile_picture']

            