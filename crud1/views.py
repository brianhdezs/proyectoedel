# views.py
from django.shortcuts import get_object_or_404, render, redirect 
from .forms import UsuarioForm, PeliculaForm
from .models import Usuario, Pelicula, Horario
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q  # Importa Q para consultas de búsqueda complejas

def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = Usuario.objects.filter(nombre_usuario=username).first()

        if user and user.contraseña == password:
            if user.tipo_usuario == 'taquillero':
                request.session['user_id'] = user.id
                return redirect('interfaz_ta')
            else:
                request.session['user_id'] = user.id
                return redirect('menu')
        else:
            error_message = "Nombre de usuario o contraseña incorrectos."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def interfaz_sa(request):
    if 'user_id' not in request.session:
        return redirect('login')

    query = request.GET.get('q')
    if query:
        usuarios = Usuario.objects.filter(Q(nombre_usuario__icontains=query))
    else:
        usuarios = Usuario.objects.all()

    # Paginar la lista de usuarios
    paginator = Paginator(usuarios, 6)  # 6 usuarios por página
    page = request.GET.get('page')
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        usuarios = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, mostrar la última página de resultados
        usuarios = paginator.page(paginator.num_pages)
    
    return render(request, 'interfaz_sa.html', {'usuarios': usuarios, 'query': query})

def interfaz_ta(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'interfaz_ta.html', {'peliculas': peliculas})

def guardar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('interfaz_sa')  
    else:
        form = UsuarioForm()
    return render(request, 'guardar_usuario.html', {'form': form})

def eliminar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    usuario.delete()
    return redirect('interfaz_sa')

def editar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        tipo_usuario = request.POST.get('tipo_usuario')
        estado = request.POST.get('estado')
        usuario.nombre_usuario = nombre_usuario
        usuario.tipo_usuario = tipo_usuario
        usuario.estado = estado
        usuario.save()
        messages.success(request, 'Usuario editado exitosamente.')
        return redirect('interfaz_sa')

    return render(request, 'editar_usuario.html', {'usuario': usuario})

def peliculas(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        if Pelicula.objects.filter(titulo=titulo).exists():
            return JsonResponse({'error': 'Ya existe una película con este título.'}, status=400)
        
        sinopsis = request.POST.get('sinopsis')
        duracion = request.POST.get('duracion')
        genero = request.POST.get('genero')
        estado = request.POST.get('estado')
        imagen = request.FILES.get('imagen')
        precio = request.POST.get('precio')
        
        pelicula = Pelicula(titulo=titulo, sinopsis=sinopsis, duracion=duracion, genero=genero, estado=estado, imagen=imagen, precio=precio)
        pelicula.save()
        
        cantidad_boletos = request.POST.get('cantidad_boletos')
        horario = Horario(pelicula=pelicula, cantidad_boletos=cantidad_boletos)
        horario.save()
        
        return JsonResponse({'message': 'Película agregada exitosamente.'})
    
    elif request.method == 'GET':
        peliculas_list = Pelicula.objects.all()
        generos_comunes = ['Acción', 'Comedia', 'Drama', 'Ciencia Ficción', 'Fantasía', 'Terror', 'Romance', 'Animación', 'Aventura', 'Documental']
        paginator = Paginator(peliculas_list, 3)
        page = request.GET.get('page')
        try:
            peliculas = paginator.page(page)
        except PageNotAnInteger:
            peliculas = paginator.page(1)
        except EmptyPage:
            peliculas = paginator.page(paginator.num_pages)
        return render(request, 'peliculas.html', {'peliculas': peliculas, 'generos_comunes': generos_comunes})
    
    else:
        return HttpResponseNotFound()

def eliminar_pelicula(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        peliculas_a_eliminar = Pelicula.objects.filter(titulo=titulo)
        peliculas_a_eliminar.delete()
        return redirect('peliculas')
    else:
        return HttpResponseNotFound()

def editar_pelicula(request, pelicula_id):
    pelicula = Pelicula.objects.get(id=pelicula_id)
    if request.method == 'POST':
        form = PeliculaForm(request.POST, request.FILES, instance=pelicula)
        if form.is_valid():
            form.save()
            return redirect('peliculas')
    else:
        form = PeliculaForm(instance=pelicula)
    return render(request, 'editar_pelicula.html', {'form': form, 'pelicula': pelicula})

def home(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'home.html', {'peliculas': peliculas})

def menu(request):
    return render(request, 'menu.html')
