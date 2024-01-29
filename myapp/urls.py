from django.urls import path
from . import views
from .views import CustomLoginView, custom_logout
 
urlpatterns = [
    path("", views.index, name="index"),
    path("contacto/", views.contacto, name="contacto"),
    path("galeria/", views.galeria, name = "galeria"),
    path("nosotros/", views.nosotros, name = "nosotros"),
    path('reserva/', views.reserva, name="reserva"),  
    path('carta/', views.carta, name='carta'),
    path('carta/<str:categoria>/', views.carta, name='carta_categoria'),
    path('register/', views.register, name="register"),
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', custom_logout, name='logout'),
    path("reseñas/", views.reseñas, name = "reseñas")
]
