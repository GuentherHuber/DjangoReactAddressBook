from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Address
import os

class AddressApiTest(APITestCase):
    picturePath=[]
    initialData=None
    #Wird zu beginn einmal ausgeführt. Angelegte DB-Daten sind automatisch persistent
    def setUp(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            self.initialData={
                'first_name':'Max',
                'last_name':'Mustermann',
                'city':'Teststadt',
                'street_name':'Teststraße',
                'house_number':'1a',
                'postcode':12345,
                'profile_picture':imageFile
            }
            
            response=self.client.post('/addressbook/api/',self.initialData,format='multipart')
            

            splittedPictureUrl=response.data['profile_picture'].split('http://testserver/')[1]
            self.picturePath.append(os.path.abspath(os.path.join(base_dir,'..','..',splittedPictureUrl)))

    #Wird am Ende einmal ausgeführt. Hochgeladene Files werden gelöscht
    def tearDown(self):
        for file in self.picturePath:
            if os.path.exists(file):
                os.remove(file)
    
    #Teste ob GET-Methode für initialData funktioniert
    def test_get_initial_address(self):
        response=self.client.get('/addressbook/api/')
        self.assertEqual(len(response.data),1)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Address.objects.filter(id=response.data[0]['id']).exists(),True) #Prüfe ob DB-Eintrag überhaupt existiert; Müsste eigentlich im Test für Model/DB stattfiden
        self.assertEqual(response.data[0]['first_name'],self.initialData['first_name'])
        self.assertEqual(response.data[0]['last_name'],self.initialData['last_name'])
        self.assertEqual(response.data[0]['city'],self.initialData['city'])
        self.assertEqual(response.data[0]['street_name'],self.initialData['street_name'])
        self.assertEqual(response.data[0]['house_number'],self.initialData['house_number'])
        self.assertEqual(response.data[0]['postcode'],self.initialData['postcode'])
        self.assertTrue('/media/images/profilePicture' in response.data[0]['profile_picture'])
        self.assertTrue(response.data[0]['profile_picture'].endswith('.jpg'))

    def test_similar_address(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            self.initialData['profile_picture']=imageFile
            response=self.client.post('/addressbook/api/',self.initialData,format='multipart')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn('Eintrag im Adressbuch bereits vorhanden!',str(response.data))

    
    def test_new_address(self):
        #Prüfe ob Anlegen einer neuer Adresse funktioniert
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Lise',
                'last_name':'Huber',
                'city':'Hauptstadt',
                'street_name':'Hauptstraße',
                'house_number':'123',
                'postcode':54321,
                'profile_picture':imageFile
            }
            
            response=self.client.post('/addressbook/api/',data,format='multipart')
        
            splittedPictureUrl=response.data['profile_picture'].split('http://testserver/')[1]
            self.picturePath.append(os.path.abspath(os.path.join(base_dir,'..','..',splittedPictureUrl)))

            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertTrue(Address.objects.filter(id=response.data['id']).exists())
            self.assertEqual(response.data['first_name'],data['first_name'])
            self.assertEqual(response.data['last_name'],data['last_name'])
            self.assertEqual(response.data['city'],data['city'])
            self.assertEqual(response.data['street_name'],data['street_name'])
            self.assertEqual(response.data['house_number'],data['house_number'])
            self.assertEqual(response.data['postcode'],data['postcode'])
            self.assertTrue('/media/images/profilePicture' in response.data['profile_picture'])
            self.assertTrue(response.data['profile_picture'].endswith('.jpg'))

        #Prüfe ob Abrufen einer Adresse per ID funktioniert
        response=self.client.get('/addressbook/api/'+str(response.data['id'])+"/")
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'],data['first_name'])
        self.assertEqual(response.data['last_name'],data['last_name'])
        self.assertEqual(response.data['city'],data['city'])
        self.assertEqual(response.data['street_name'],data['street_name'])
        self.assertEqual(response.data['house_number'],data['house_number'])
        self.assertEqual(response.data['postcode'],data['postcode'])
        self.assertTrue('/media/images/profilePicture' in response.data['profile_picture'])
        self.assertTrue(response.data['profile_picture'].endswith('.jpg'))


#Test Update
#Test Löschen
  