from django.db import models

class Address(models.Model):
    first_name=models.CharField(max_length=100,blank=True)
    last_name=models.CharField(max_length=100,blank=True)
    city=models.CharField(max_length=100,blank=True)
    street_name=models.CharField(max_length=100,blank=True)
    house_number=models.CharField(max_length=50,blank=True)
    postcode=models.IntegerField(blank=True,null=True)
    profile_picture=models.ImageField(upload_to='images/',blank=True,null=True)
    



