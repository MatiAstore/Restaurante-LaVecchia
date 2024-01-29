from django.contrib import admin
from .models import Galeria, Carta, Reserva, MensajeContacto, Resena

# Register your models here.
admin.site.register(Galeria)
admin.site.register(Carta)    
admin.site.register(Reserva)
admin.site.register(MensajeContacto)
admin.site.register(Resena)

