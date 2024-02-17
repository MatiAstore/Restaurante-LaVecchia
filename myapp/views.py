from django.shortcuts import render, redirect, get_object_or_404
from .models import Galeria, Carta, Resena, Reserva
from .forms import ContactoForm, UserRegisterForm, ReservaForm, ResenaForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth import logout
from django.contrib import messages #necesario para las notifiaciones de inicio, cierre y registro exitoso.
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy 
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")

def nosotros(request):
    return render(request, "nosotros.html")


def galeria(request):
    galeria = Galeria.objects.all()
    return render(request, "galeria.html", {'galeria': galeria})

def contacto(request):
    if request.method == "POST": 
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto enviado exitosamente.')
            return redirect(
                "contacto"
            ) 
    else:
        form = ContactoForm()

    return render(request, "contacto.html", {"form": form})

def carta(request, categoria=None):
    if categoria: #verifica si se proporciono una categoria a la URL
        carta = Carta.objects.filter(tipo=categoria)#si no se proporciono una caterogia, trae todas las instancias de carta
    else:
        carta = Carta.objects.all()

    galeria = Galeria.objects.all()

    # Obtener tipos únicos de comidas y contar cuántas comidas hay de cada tipo
    tipos_comida = Carta.objects.values('tipo').annotate(count=Count('tipo'))

    return render(request, "carta.html", {"carta": carta, "galeria": galeria, "tipos_comida": tipos_comida, "categoria_seleccionada": categoria})


def reseñas(request):
    # Recupera todas las reseñas de la base de datos
    reseñas = Resena.objects.all()

    if request.method == 'POST':
        # Procesa el formulario si se envía
        form = ResenaForm(request.POST)
        if form.is_valid():
            # Guarda la reseña en la base de datos
            nueva_resena = form.save(commit=False)
            nueva_resena.usuario = request.user
            nueva_resena.save()
            messages.success(request, 'Reseña enviada exitosamente.')
            return redirect('reseñas')
    else:
        # Muestra el formulario vacío si la solicitud es GET
        form = ResenaForm()

    return render(request, 'reseñas.html', {'reseñas': reseñas, 'form': form})


def reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            send_mail(
                'Confirmación de Reserva',
                'Gracias por reservar en nuestro restaurante. Detalles de la reserva:\nCantidad de personas: {}\nFecha: {}\nHora: {}'.format(reserva.cantidad_personas, reserva.fecha, reserva.hora),
                'tu@email.com',
                [request.user.email],
                fail_silently=False,
            )
            # Redirige a la página de confirmación con los detalles de la reserva
            return redirect('confirmacion_reserva', reserva_id=reserva.id)
    else:
        form = ReservaForm()
    reservas_usuario = None
    if request.user.is_authenticated:
        reservas_usuario = Reserva.objects.filter(usuario=request.user)
    return render(request, 'reserva.html', {'form': form, 'reservas_usuario': reservas_usuario}) 


def confirmacion_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'confirmacion_reserva.html', {'reserva': reserva})

def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    # Verifica si el usuario es el propietario de la reserva
    if reserva.usuario == request.user:
        if request.method == 'POST':
            reserva.delete()
            return redirect('reserva')
    # Si la solicitud no es POST, redirige nuevamente a la página de reservas
    return redirect('reserva')

# El registro se hizo manuelmente, no utilizamos librerias como para Logout y Login
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Usuario {username} registrado exitosamente.")
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "register.html", {'form': form})


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, "¡Inicio de sesión exitoso!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('reserva'))

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'  
    email_template_name = 'registration/password_reset_email.html'  


# Para esto lo habia hecho de la misma forma que el Login, sin embargo, saltaba error GET al cerrar sesion y no funcionaba, por ende le pedi al amigo y utilizamos otra libreria para el Logout
def custom_logout(request):
    logout(request)
    messages.success(request, "¡Has cerrado sesión exitosamente!")
    return redirect('login')  

