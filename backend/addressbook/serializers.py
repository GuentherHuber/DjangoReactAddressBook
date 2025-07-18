from rest_framework import serializers
from .models import Address
import os
from django.db import IntegrityError

class AddressSerializer(serializers.ModelSerializer):
      class Meta:
            model=Address
            fields=['id','first_name','last_name','city','street_name','house_number','postcode','profile_picture']

      #Verhindere dopplete Einträge
      def create(self, validated_data):
            if Address.objects.filter(first_name=validated_data.get('first_name'),last_name=validated_data.get('last_name')).exists():
                  raise serializers.ValidationError("Adresse bereits vorhanden!")
            return super().create(validated_data)

      def validate_first_name(self,value):
            if not value.strip():
                  raise serializers.ValidationError("Vorname darf nicht leer sein!")
            return value

      def validate_last_name(self,value):
            if not value.strip():
                  raise serializers.ValidationError("Nachname darf nicht leer sein!")
            return value
      
      def validate_city(self,value):
            if not value.strip():
                  raise serializers.ValidationError("Stadt darf nicht leer sein!")
            return value
      
      def validate_street_name(self,value):
            if not value.strip():
                  raise serializers.ValidationError("Strasse darf nicht leer sein!")
            return value
      
      def validate_house_number(self,value):
            if not value.strip():
                  raise serializers.ValidationError("Hausnummer darf nicht leer sein!")
            return value
      
      def validate_postcode(self,value):
            if len(str(value))==0 or value==None:
                  raise serializers.ValidationError("PLZ darf nicht leer sein!")
            if len(str(value))!=5:
                  raise serializers.ValidationError("PLZ muss aus genau 5 Ziffern bestehen!")
            return value
      
      def validate_profile_picture(self,value):
            valid_extensions = ['.jpg','.jpeg','.png','.gif']
            extension=os.path.splitext(value.name)[1].lower()
            if extension not in valid_extensions:
                  raise serializers.ValidationError("Ungültiges Dateiformat!")
            return value    
    

            