from django.test import TestCase
from app.models import Client, validate_date_of_birthday, Medicine
from datetime import datetime

class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({
            "name": client.name,
            "phone": "221555233",
            "email": client.email
        })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class PetModelTest(TestCase):
    def test_valid_date(self):
        date_str = '2020-05-22'
        self.assertIsNone(validate_date_of_birthday(date_str))

    def test_future_date(self):
        future_date = (datetime.today().year + 1, 5, 22)
        date_str = datetime(*future_date).strftime('%Y-%m-%d')
        self.assertEqual(validate_date_of_birthday(date_str), "La fecha no puede ser mayor al dia de hoy")

    def test_invalid_format(self):
        date_str = '22-05-2020'
        self.assertEqual(validate_date_of_birthday(date_str), "Formato de fecha incorrecto")

    def test_empty_string(self):
        date_str = ''
        self.assertEqual(validate_date_of_birthday(date_str), "Formato de fecha incorrecto")

    def test_non_date_string(self):
        date_str = 'not-a-date'
        self.assertEqual(validate_date_of_birthday(date_str), "Formato de fecha incorrecto")
class MedicineModelTest(TestCase):
    def test_dose_range_validation(self):
        
        response = Medicine.save_medicine(
            {
                "name": "Paracetamol",
                "description": "Analgesic and antipyretic",
                "dose": 15
            }
        )
        
        self.assertFalse(response[0])  
        self.assertIn("dose", response[1])  
        self.assertEqual(response[1]["dose"], "La dosis debe estar entre 1 y 10") 
