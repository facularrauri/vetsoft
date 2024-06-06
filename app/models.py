from datetime import datetime

from django.db import models


def validate_fields(data, required_fields):
    errors = {}

    for key, value in required_fields.items():
        field_value = data.get(key, "")

        if field_value == "":
            errors[key] = f"Por favor ingrese un {value}"
        elif key == 'email':
            email_error = validate_vetsoft_email(field_value)
            if email_error:
                errors["email"] = email_error
        elif key == 'price' and  float(field_value) <0.0:
            errors["price"] = "El precio debe ser mayor a cero"
        elif key == 'weight' and int(field_value) < 0:
            errors["weight"] = "El peso de la mascota no puede ser negativo"
        elif key == 'birthday':
            birthday_error = validate_date_of_birthday(field_value)
            if birthday_error:
                errors["birthday"] = birthday_error
        elif key =='dose' and (int(field_value) < 1 or int(field_value) > 10):
            errors["dose"] = "La dosis debe estar entre 1 y 10"
    return errors

def validate_date_of_birthday(date_str):
    try:
        birth_date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.today()
        if birth_date > today:
            return "La fecha no puede ser mayor al dia de hoy"
        return None
    except ValueError:
        return "Formato de fecha incorrecto"

def validate_vetsoft_email(value):
    if value.count("@") == 0:
        return "Por favor ingrese un email valido"
    if not value.endswith('@vetsoft.com'):
        return "El email debe finalizar con @vetsoft.com"
    return None

class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_required_fields():
        return {
            "name": "nombre",
            "email": "email",
            "phone": "teléfono",
        }

    @classmethod
    def save_client(cls, client_data):
        errors = validate_fields(client_data, Client.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        errors = validate_fields(client_data, Client.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "")

        self.save()

        return True, None

class Pet(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50)
    birthday = models.DateField()
    weight = models.IntegerField()

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_required_fields():
        return {
            "name": "nombre",
            "breed": "raza", 
            "birthday": "fecha de nacimiento",
            "weight": "peso",
        }

    @classmethod
    def save_pet(cls, pet_data):
        errors = validate_fields(pet_data, Pet.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors


        Pet.objects.create(
            name=pet_data.get("name"),
            breed=pet_data.get("breed"),
            birthday=pet_data.get("birthday"),
            weight=pet_data.get("weight"),
        )

        return True, None
    
    def update_pet(self, pet_data):
        errors = validate_fields(pet_data, Pet.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        self.name = pet_data.get("name", "") or self.name
        self.breed = pet_data.get("breed", "") or self.breed
        self.birthday = pet_data.get("birthday", "") or self.birthday
        self.weight = pet_data.get("weight", "") or self.weight

        self.save()

        return True, None

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=50)
    dose = models.IntegerField()

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_required_fields():
        return {
            "name": "nombre",
            "description": "descripción", 
            "dose": "dosis",
        }
    
    @classmethod
    def save_medicine(cls, medicine_data):
        errors = validate_fields(medicine_data, Medicine.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        Medicine.objects.create(
            name=medicine_data.get("name"),
            description=medicine_data.get("description"),
            dose=medicine_data.get("dose"),
        ),
    
        return True, None

    def update_medicine(self, medicine_data):
        errors = validate_fields(medicine_data, Medicine.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        self.name = medicine_data.get("name", "") or self.name
        self.description = medicine_data.get("description", "") or self.description
        self.dose = medicine_data.get("dose", 1) or self.dose

        self.save()

        return True, None

class Vet(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_required_fields():
        return {
            "name": "nombre",
            "email": "email", 
            "phone": "phone",
        }
    
    @classmethod
    def save_vet(cls, vet_data):
        errors = validate_fields(vet_data, Vet.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            email=vet_data.get("email"),
            phone=vet_data.get("phone"),
        )

        return True, None
    
    
    def update_vet(self, vet_data):
        errors = validate_fields(vet_data, Vet.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone

        self.save()

        return True, None
class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15)
    price =models.FloatField()


    def __str__(self):
        return self.name
    
    @staticmethod
    def get_required_fields():
        return {
            "name": "nombre",
            "type": "tipo",
            "price": "precio",
        }

    @classmethod
    def save_product(prod, product_data):
        errors = validate_fields(product_data, Product.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
        )

        return True, None

    def update_product(self, product_data):
        errors = validate_fields(product_data, Product.get_required_fields())

        if len(errors.keys()) > 0:
            return False, errors

        self.name = product_data.get("name", "") or self.name
        self.type= product_data.get("type", "") or self.type
        self.price = product_data.get("price", 0.0) or self.price

        self.save()

        return True, None
