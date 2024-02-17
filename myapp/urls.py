from django.urls import path
from . import views
from .views import CustomLoginView, custom_logout, confirmacion_reserva, CustomPasswordResetView, eliminar_reserva
from django.contrib.auth import views as auth_views 
 
urlpatterns = [
    path("", views.index, name="index"),
    path("contacto/", views.contacto, name="contacto"),
    path("galeria/", views.galeria, name="galeria"),
    path("nosotros/", views.nosotros, name="nosotros"),
    path('reserva/', views.reserva, name="reserva"),  
    path('confirmacion_reserva/<int:reserva_id>/', confirmacion_reserva, name='confirmacion_reserva'), 
    path('reserva/<int:reserva_id>/eliminar/', eliminar_reserva, name='eliminar_reserva'),
    path('carta/', views.carta, name='carta'),
    path('carta/<str:categoria>/', views.carta, name='carta_categoria'),
    path('register/', views.register, name="register"),
    path("login/", CustomLoginView.as_view(template_name="login.html"), name="login"),
    path('reset-password/', CustomPasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-password-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', custom_logout, name='logout'),
    path("reseñas/", views.reseñas, name="reseñas")
]
