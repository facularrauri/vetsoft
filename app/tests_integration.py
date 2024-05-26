from datetime import date, datetime
from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client, Pet, Medicine


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
                "phone": client.phone,
                "email": client.email,
                "address": client.address
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)

class PetsTest(TestCase):
    def test_use_pets_repo_template(self):
        response = self.client.get(reverse("pets_repo"))
        self.assertTemplateUsed(response, "pets/repository.html")
    
    def test_can_create_pet(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Manolo",
                "breed": "golden",
                "birthday": "2019-03-14",
            },
        )
        pets = Pet.objects.all()
        self.assertEqual(len(pets), 1)

        self.assertEqual(pets[0].name, "Manolo")
        self.assertEqual(pets[0].breed, "golden")
        self.assertEqual(pets[0].birthday, date(2019, 3, 14))

        self.assertRedirects(response, reverse("pets_repo"))
    
    def test_validate_date_of_birthday(self):
        future_date = (datetime.today().year + 1, 5, 22)
        date_str = datetime(*future_date).strftime('%Y-%m-%d')
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Manolo",
                "breed": "golden",
                "birthday": date_str,
            },
        )

        self.assertContains(response, "La fecha no puede ser mayor al dia de hoy")

    def test_validate_invalid_date_of_birthday(self):
        response = self.client.post(
            reverse("pets_form"),
            data={
                "name": "Manolo",
                "breed": "golden",
                "birthday": 'not-a-date',
            },
        )

        self.assertContains(response, "Formato de fecha incorrecto")
        
class MedicinesTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("medicines_repo"))
        self.assertTemplateUsed(response, "medicines/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("medicines_form"))
        self.assertTemplateUsed(response, "medicines/form.html")

    def test_can_create_medicine(self):
        response = self.client.post(
            reverse("medicines_form"),
            data={
                "name": "Paracetamol",
                "description": "Analgesic and antipyretic",
                "dose": "5",
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Paracetamol")
        self.assertEqual(medicines[0].description, "Analgesic and antipyretic")
        self.assertEqual(medicines[0].dose, 5)

        self.assertRedirects(response, reverse("medicines_repo"))

    def test_validation_errors_create_medicine(self):
        response = self.client.post(
            reverse("medicines_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un descripción")
        self.assertContains(response, "Por favor ingrese un dosis")

    def test_edit_medicine_with_valid_data(self):
        medicine = Medicine.objects.create(
            name="Paracetamol",
            description="Analgesic and antipyretic",
            dose=5,
        )

        response = self.client.post(
            reverse("medicines_form"),
            data={
                "id": medicine.id,
                "name": "Ibuprofen",
                "description": "Analgesic and anti-inflammatory",
                "dose": "4",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        edited_medicine = Medicine.objects.get(pk=medicine.id)
        self.assertEqual(edited_medicine.name, "Ibuprofen")
        self.assertEqual(edited_medicine.description, "Analgesic and anti-inflammatory")
        self.assertEqual(edited_medicine.dose, 4)