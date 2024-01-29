from django.shortcuts import render, redirect 
from .models import Galeria, Carta, Resena
from .forms import ContactoForm, UserRegisterForm, ReservaForm, ResenaForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages #necesario para las notifiaciones de inicio, cierre y registro exitoso.
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy #



def index(request):
    return render(request, "index.html")

def nosotros(request):
    return render(request, "nosotros.html")
.0

def galeria(request):
    galeria = Galeria.objects.all()
    return render(request, "galeria.html", {'galeria': galeria})

def contacto(request):
    if request.method == "POST": 
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reseña enviada exitosamente.')
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
            messages.success(request, f"Reserva realizada existosamente. Gracias {request.user}.")
            return redirect('reserva')
    else:
        form = ReservaForm()

    return render(request, 'reserva.html', {'form': form})


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


#heredamos la clase LoginView y modifico la vista entorno a esa clase (Tambien se puede hacer utilizando de otro libreria el "Login" pero como lo hice de esta forma y funciono lo deje asi)
class CustomLoginView(LoginView): 
    def form_valid(self, form):
        messages.success(self.request, "¡Inicio de sesión exitoso!")

        return super().form_valid(form)

    def get_success_url(self):
        # Utiliza el parámetro 'next' si está presente, de lo contrario, redirige a la página por defecto
        return self.request.GET.get('next', reverse_lazy('index'))

    
# Para esto lo habia hecho de la misma forma que el Login, sin embargo, saltaba error GET al cerrar sesion y no funcionaba, por ende le pedi al amigo y utilizamos otra libreria para el Logout
def custom_logout(request):
    logout(request)
    messages.success(request, "¡Has cerrado sesión exitosamente!")
    return redirect('login')  

