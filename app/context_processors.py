from django.urls import reverse

links = [
    {"label": "Home", "href": reverse("home"), "icon": "bi bi-house-door"},
    {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
    {"label": "Animales", "href": reverse("pets_repo"), "icon": "fas fa-dog"},
    {"label": "Medicamentes", "href": reverse("medicines_repo"), "icon": "fas fa-pills"},
    {"label": "Veterinarios", "href": reverse("vets_repo"), "icon": "fas fa-user-md"},
    {"label": "Productos", "href": reverse("products_repo"), "icon": "fas fa-paw"},
]

def navbar(request):
    """Genera los enlaces de la barra de navegación activos basados en la solicitud.
    """
    def add_active(link):
        copy = link.copy()

        if copy["href"] == "/":
            copy["active"] = request.path == "/"
        else:
            copy["active"] = request.path.startswith(copy.get("href", ""))

        return copy

    return {"links": map(add_active, links)}

def home_items(request):
    """ Genera los elementos para mostrar en la página de inicio.
    """
    items = [
        {"label": "Clientes", "href": reverse("clients_repo"), "icon": "bi bi-people"},
        {"label": "Animales", "href": reverse("pets_repo"), "icon": "fas fa-dog"},
        {"label": "Medicamentos", "href": reverse("medicines_repo"), "icon": "fas fa-pills"},
        {"label": "Veterinarios", "href": reverse("vets_repo"), "icon": "fas fa-user-md"},
        {"label": "Productos", "href": reverse("products_repo"), "icon": "fas fa-paw"},
    ]
    return {"home_items": items}
