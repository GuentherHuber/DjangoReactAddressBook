from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Address
import os

class AddressApiTest(APITestCase):
    

    def test_create_valid_address(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Max',
                'last_name':'Mustermann',
                'city':'Teststadt',
                'street_name':'Teststraße',
                'house_number':'1a',
                'postcode':12345,
                'profile_picture':imageFile
            }

            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertEqual(Address.objects.filter(id=response.data['id']).exists(),True) #Prüfe ob DB-Eintrag überhaupt existiert; Müsste eigentlich im Test für Model/DB stattfiden
            self.assertEqual(response.data['first_name'],data['first_name'])
            self.assertEqual(response.data['last_name'],data['last_name'])
            self.assertEqual(response.data['city'],data['city'])
            self.assertEqual(response.data['street_name'],data['street_name'])
            self.assertEqual(response.data['house_number'],data['house_number'])
            self.assertEqual(response.data['postcode'],data['postcode'])
            self.assertTrue('/media/images/profilePicture' in response.data['profile_picture'])
            self.assertTrue(response.data['profile_picture'].endswith('.jpg'))
            #Hier ist der Test zu Ende. Das für den Test hochgeladene ProfilePicture muss aber wieder gelöscht werden
            #Erst mal Pfad zur Datei ermitteln
            splittedPictureUrl=response.data['profile_picture'].split('http://testserver/')[1]
            picturePath=os.path.abspath(os.path.join(base_dir,'..','..',splittedPictureUrl))
            if os.path.exists(picturePath):
                os.remove(picturePath)
