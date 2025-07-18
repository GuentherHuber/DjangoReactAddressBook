from rest_framework import status
from rest_framework.test import APITestCase
from ..models import Address
import os

class AddressApiTest(APITestCase):
    picturePath=[]
    initialData=None
    #Wird vor jedem Testfall einmal ausgeführt
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
            #Speichere id aus der POST-Anfrage in initialData
            self.initialData['id']=response.data['id']
            splittedPictureUrl=response.data['profile_picture'].split('http://testserver/')[1]
            self.picturePath.append(os.path.abspath(os.path.join(base_dir,'..','..',splittedPictureUrl)))

    #Wird nach jedem Testfall einmal ausgeführt
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

    #Teste ob anlegen 2 gleicher Adressen nicht funktioniert
    def test_similar_address(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':self.initialData['first_name'],
                'last_name':self.initialData['last_name'],
                'city':'Hauptstadt',
                'street_name':'Hauptstraße',
                'house_number':'123',
                'postcode':54321,
                'profile_picture':imageFile
            }
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('Adresse bereits vorhanden!',str(response.data))

    #Test ob anlegen einer neuen Adresse funktioniert
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

        #Teste ob Abrufen einer Adresse per ID funktioniert
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

    def test_new_adress_without_profile_picutre(self):
        data={
                'first_name':'Hans',
                'last_name':'Maier',
                'city':'Nebenstadt',
                'street_name':'Nebenstraße',
                'house_number':'1 1/2',
                'postcode':43210,
            }
        
        response=self.client.post('/addressbook/api/',data,format='multipart')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertTrue(Address.objects.filter(id=response.data['id']).exists())
        self.assertEqual(response.data['first_name'],data['first_name'])
        self.assertEqual(response.data['last_name'],data['last_name'])
        self.assertEqual(response.data['city'],data['city'])
        self.assertEqual(response.data['street_name'],data['street_name'])
        self.assertEqual(response.data['house_number'],data['house_number'])
        self.assertEqual(response.data['postcode'],data['postcode'])

    #Teste ob ändern einer Adresse mit anderen Daten funtkioniert
    def test_update_address_with_other_data(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            self.initialData['profile_picture']=imageFile
            self.initialData['first_name']='Erika'
            self.initialData['postcode']=67890
            
            response=self.client.patch('/addressbook/api/'+str(self.initialData['id'])+"/",self.initialData,format='multipart')

            splittedPictureUrl=response.data['profile_picture'].split('http://testserver/')[1]
            self.picturePath.append(os.path.abspath(os.path.join(base_dir,'..','..',splittedPictureUrl)))

            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(response.data['first_name'],self.initialData['first_name'])
            self.assertEqual(response.data['last_name'],self.initialData['last_name'])
            self.assertEqual(response.data['city'],self.initialData['city'])
            self.assertEqual(response.data['street_name'],self.initialData['street_name'])
            self.assertEqual(response.data['house_number'],self.initialData['house_number'])
            self.assertEqual(response.data['postcode'],self.initialData['postcode'])
            self.assertTrue('/media/images/profilePicture' in response.data['profile_picture'])
            self.assertTrue(response.data['profile_picture'].endswith('.jpg'))

    #Test ob ändern einer Adresse mit gleichen daten funktioniert
    def test_upate_address_with_same_data(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                    'first_name':self.initialData['first_name'],
                    'last_name':self.initialData['last_name'],
                    'city':self.initialData['city'],
                    'street_name':self.initialData['street_name'],
                    'house_number':self.initialData['house_number'],
                    'postcode':self.initialData['postcode'],
                    'profile_picture':imageFile
                }
            response=self.client.patch('/addressbook/api/'+str(self.initialData['id'])+"/",data,format='multipart')

            splittedPictureUrl=response.data['profile_picture'].split('http://testserver/')[1]
            self.picturePath.append(os.path.abspath(os.path.join(base_dir,'..','..',splittedPictureUrl)))

            self.assertEqual(response.status_code,status.HTTP_200_OK)
            self.assertEqual(response.data['first_name'],data['first_name'])
            self.assertEqual(response.data['last_name'],data['last_name'])
            self.assertEqual(response.data['city'],data['city'])
            self.assertEqual(response.data['street_name'],data['street_name'])
            self.assertEqual(response.data['house_number'],data['house_number'])
            self.assertEqual(response.data['postcode'],data['postcode'])
            self.assertTrue('/media/images/profilePicture' in response.data['profile_picture'])
            self.assertTrue(response.data['profile_picture'].endswith('.jpg'))

    def test_empty_first_name(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'',
                'last_name':'Mustermann',
                'city':'Teststadt',
                'street_name':'Teststraße',
                'house_number':'1a',
                'postcode':12345,
                'profile_picture':imageFile
            }
            
            #Get amount of address entries before post
            response=self.client.get('/addressbook/api/')
            entriesBefore=len(response.data)
            #Post http request with invalid/empty first_name
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('Vorname darf nicht leer sein!',str(response.data['first_name']))
            #Get amount of address entries after post
            response=self.client.get('/addressbook/api/')
            entriesAfter=entriesBefore=len(response.data)
            #Prüfe ob durch die ungültige Anfrage ein neuer DB-Eintrag entstanden ist
            if entriesBefore!=entriesAfter:
                self.fail('Anzahl der Adressbucheinträge unterschiedlich')

    def test_empty_last_name(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Max',
                'last_name':'',
                'city':'Teststadt',
                'street_name':'Teststraße',
                'house_number':'1a',
                'postcode':12345,
                'profile_picture':imageFile
            }
            
            #Get amount of address entries before post
            response=self.client.get('/addressbook/api/')
            entriesBefore=len(response.data)
            #Post http request with invalid/empty last_name
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('Nachname darf nicht leer sein!',str(response.data['last_name']))
            #Get amount of address entries after post
            response=self.client.get('/addressbook/api/')
            entriesAfter=entriesBefore=len(response.data)
            #Prüfe ob durch die ungültige Anfrage ein neuer DB-Eintrag entstanden ist
            if entriesBefore!=entriesAfter:
                self.fail('Anzahl der Adressbucheinträge unterschiedlich')

    def test_empty_city(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Max',
                'last_name':'Mustermann',
                'city':'',
                'street_name':'Teststraße',
                'house_number':'1a',
                'postcode':12345,
                'profile_picture':imageFile
            }
            
            #Get amount of address entries before post
            response=self.client.get('/addressbook/api/')
            entriesBefore=len(response.data)
            #Post http request with invalid/empty city
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('Stadt darf nicht leer sein!',str(response.data['city']))
            #Get amount of address entries after post
            response=self.client.get('/addressbook/api/')
            entriesAfter=entriesBefore=len(response.data)
            #Prüfe ob durch die ungültige Anfrage ein neuer DB-Eintrag entstanden ist
            if entriesBefore!=entriesAfter:
                self.fail('Anzahl der Adressbucheinträge unterschiedlich')

    def test_empty_street_name(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Max',
                'last_name':'Mustermann',
                'city':'Teststadt',
                'street_name':'',
                'house_number':'1a',
                'postcode':12345,
                'profile_picture':imageFile
            }
            
            #Get amount of address entries before post
            response=self.client.get('/addressbook/api/')
            entriesBefore=len(response.data)
            #Post http request with invalid/empty street_name
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('Strasse darf nicht leer sein!',str(response.data['street_name']))
            #Get amount of address entries after post
            response=self.client.get('/addressbook/api/')
            entriesAfter=entriesBefore=len(response.data)
            #Prüfe ob durch die ungültige Anfrage ein neuer DB-Eintrag entstanden ist
            if entriesBefore!=entriesAfter:
                self.fail('Anzahl der Adressbucheinträge unterschiedlich')

    def test_empty_house_number(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Max',
                'last_name':'Mustermann',
                'city':'Teststadt',
                'street_name':'Teststraße',
                'house_number':'',
                'postcode':12345,
                'profile_picture':imageFile
            }
            
            #Get amount of address entries before post
            response=self.client.get('/addressbook/api/')
            entriesBefore=len(response.data)
            #Post http request with invalid/empty house_number
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('Hausnummer darf nicht leer sein!',str(response.data['house_number']))
            #Get amount of address entries after post
            response=self.client.get('/addressbook/api/')
            entriesAfter=entriesBefore=len(response.data)
            #Prüfe ob durch die ungültige Anfrage ein neuer DB-Eintrag entstanden ist
            if entriesBefore!=entriesAfter:
                self.fail('Anzahl der Adressbucheinträge unterschiedlich')

    def test_empty_postcode(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Max',
                'last_name':'Mustermann',
                'city':'Teststadt',
                'street_name':'Teststraße',
                'house_number':'1a',
                'postcode':'',
                'profile_picture':imageFile
            }
            
            #Get amount of address entries before post
            response=self.client.get('/addressbook/api/')
            entriesBefore=len(response.data)
            #Post http request with invalid/empty postcode
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('PLZ darf nicht leer sein!',str(response.data['postcode']))
            #Get amount of address entries after post
            response=self.client.get('/addressbook/api/')
            entriesAfter=entriesBefore=len(response.data)
            #Prüfe ob durch die ungültige Anfrage ein neuer DB-Eintrag entstanden ist
            if entriesBefore!=entriesAfter:
                self.fail('Anzahl der Adressbucheinträge unterschiedlich')
            
    def test_malformed_postcode(self):
        base_dir=(os.path.dirname(os.path.abspath(__file__)))
        with open (os.path.join(base_dir,'artifacts','profilePicture.jpg'),'rb') as imageFile:
            data={
                'first_name':'Max',
                'last_name':'Mustermann',
                'city':'Teststadt',
                'street_name':'Teststraße',
                'house_number':'1a',
                'postcode':'1',
                'profile_picture':imageFile
            }
            
            #Get amount of address entries before post
            response=self.client.get('/addressbook/api/')
            entriesBefore=len(response.data)
            #Post http request with invalid/empty postcode
            response=self.client.post('/addressbook/api/',data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
            self.assertIn('PLZ muss aus genau 5 Ziffern bestehen!',str(response.data['postcode']))
            #Get amount of address entries after post
            response=self.client.get('/addressbook/api/')
            entriesAfter=entriesBefore=len(response.data)
            #Prüfe ob durch die ungültige Anfrage ein neuer DB-Eintrag entstanden ist
            if entriesBefore!=entriesAfter:
                self.fail('Anzahl der Adressbucheinträge unterschiedlich')

    def test_delete_address_by_id(self):
        response=self.client.delete('/addressbook/api/'+str(self.initialData['id'])+"/")
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        #Check amount of address entries (should be 0)
        response=self.client.get('/addressbook/api/')
        if(len(response.data)!=0):
            self.fail('Löschen der Adresse nicht erfolgreich!')