from django.db import models
from django.contrib.auth.models import User

class Galeria(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to= "imagenes/", null = True)

    def __str__(self):
        return f"{self.nombre}" 

class Carta(models.Model):
    TIPO_CHOICES = [
        ('Bebidas', 'Bebidas'),
        ('Postres', 'Postres'),
        ('Comidas', 'Comidas'),
        ('Entradas', 'Entradas'),
    ]

    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre}" 
    
    
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
    

class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad_personas = models.PositiveIntegerField()  # Nuevo campo
    fecha = models.DateField()
    hora = models.TimeField()

    class Meta:
        unique_together = ['cantidad_personas', 'fecha', 'hora']

    def __str__(self):
        return f"{self.usuario}"
    
class Resena(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    clasificacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reseña de {self.usuario.username} - Clasificación: {self.clasificacion}'
