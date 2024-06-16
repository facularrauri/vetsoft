from datetime import date, datetime

from django.test import TestCase

from app.models import (
    Client,
    Medicine,
    Pet,
    Product,
    validate_date_of_birthday,
    validate_vetsoft_email,
    validate_phone
)


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "54221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({
            "name": client.name,
            "phone": "54221555233",
            "email": client.email
        })

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "54221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "54221555232")

    def test_not_valid_email(self):
        self.assertEqual(validate_vetsoft_email("email"), "Por favor ingrese un email valido")

    def test_not_valid_vetsoft_email(self):
        email = "test@non-vetsoft.com"
        self.assertEqual(validate_vetsoft_email(email), "El email debe finalizar con @vetsoft.com")

    def test_valid_vetsoft_email(self):
        email = "test@vetsoft.com"
        self.assertIsNone(validate_vetsoft_email(email))
        
    def test_not_phone_code(self):
        phone = "1234567890"
        self.assertEqual(validate_phone(phone), "El teléfono debe comenzar siempre con 54")
        
        

class PetModelTest(TestCase):
    def test_can_create_and_get_pet(self):
        Pet.save_pet(
            {
                "name": "Nami",
                "breed": "Siames",
                "birthday": '2020-05-22',
                "weight": 30,
            }
        )
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)

        self.assertEqual(pets[0].name, "Nami")
        self.assertEqual(pets[0].breed, "Siames")
        self.assertEqual(pets[0].birthday, date(2020, 5, 22))
        self.assertEqual(pets[0].weight, 30)

    def test_can_update_pet(self):
        Pet.save_pet(
            {
                "name": "Nami",
                "breed": "Siames",
                "birthday": "2020-05-22",
                "weight": 30,
            }
        )
        pet = Pet.objects.get(pk=1)

        self.assertEqual(pet.weight, 30)

        pet.update_pet({
            "name": pet.name,
            "birthday": pet.birthday.strftime('%Y-%m-%d'),
            "weight": 40,
            "breed": pet.breed
        })

        pet_updated = Pet.objects.get(pk=1)

        self.assertEqual(pet_updated.weight, 40)

    def test_update_pet_with_error(self):
        Pet.save_pet(
            {
                "name": "Nami",
                "breed": "Siames",
                "birthday": "2020-05-22",
                "weight": 50,
            }
        )

        pet = Pet.objects.get(pk=1)

        pet.update_pet({
            "name": pet.name,
            "birthday": pet.birthday.strftime('%Y-%m-%d'),
            "weight": -50,
            "breed": pet.breed,
        })

        pet_updated = Pet.objects.get(pk=1)

        self.assertEqual(pet_updated.weight, 50)

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
class ProductModelTest(TestCase):
    def test_can_create_and_get_product(self):
        Product.save_product(
            {
                "name": "Alimento Balanceado para perro +10 años",
                "type": "alimento",
                "price": "6.5",
            }
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Alimento Balanceado para perro +10 años")
        self.assertEqual(products[0].type, "alimento")
        self.assertEqual(products[0].price, 6.5)
