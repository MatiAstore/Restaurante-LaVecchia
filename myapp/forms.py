from django import forms
from django.contrib.auth.forms import UserCreationForm #form para registro
from django.contrib.auth.models import User 
from .models import MensajeContacto, Reserva, Resena
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime
from datetime import timedelta

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agregar clases de Bootstrap a los campos del formulario
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
        # Modificar las etiquetas de los campos del formulario
        self.fields['username'].label = "Usuario"
        self.fields['password'].label = "Contraseña"


class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto #modelo asociado al formulario
        fields = ["nombre", "correo", "mensaje"] #campos del mismo que se tomaran 

    nombre = forms.CharField(
        label="Nombre",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    correo = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    mensaje = forms.CharField(
        label="Mensaje", widget=forms.Textarea(attrs={"class": "form-control"})
    )

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo electronico", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Usuario", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirme su Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {k: "" for k in fields}  # remover los strings vacios

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['texto', 'clasificacion']

    CLASIFICACIONES = [
        ('1', '1 estrella'),
        ('2', '2 estrellas'),
        ('3', '3 estrellas'),
        ('4', '4 estrellas'),
        ('5', '5 estrellas'),
    ] 

    texto = forms.CharField(
        label="Tu reseña",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}),
    )

    clasificacion = forms.ChoiceField(
        label="Clasificación",
        choices=CLASIFICACIONES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ['cantidad_personas', 'fecha', 'hora']

    cantidad_personas = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 9)],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': timezone.now().strftime('%Y-%m-%d')}),
        input_formats=['%Y-%m-%d']
    )

    hora = forms.ChoiceField(
        choices=[(f"{i:02d}:00", f"{i:02d}:00") for i in range(10, 22)],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean(self):
        cleaned_data = super().clean()
        cantidad_personas = cleaned_data.get('cantidad_personas')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if Reserva.objects.filter(cantidad_personas=cantidad_personas, fecha=fecha, hora=hora).exists():
            error_msg = "Ya existe una reserva para esa cantidad de personas en esa fecha y hora."
            self.add_error(None, error_msg)

        if fecha and fecha < timezone.now().date():
            self.add_error('fecha', 'No puedes hacer reservas en fechas pasadas.')

        return cleaned_data

