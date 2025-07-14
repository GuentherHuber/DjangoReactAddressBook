from django.db import models

class Address(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    street_name=models.CharField(max_length=100)
    house_number=models.CharField(max_length=50)
    postcode=models.IntegerField()
    profile_picture=models.ImageField(upload_to='images/',blank=True,null=True)
    



