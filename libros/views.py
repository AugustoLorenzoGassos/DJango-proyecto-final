from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render,redirect
from .models import Libro
from .forms import LibroForm, CustomLoginForm, CustomerUserCreationForm

# --- VISTAS DE AUTENTICACIÓN Y USUARIOS ---

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'login'

class RegistroView(CreateView):
    form_class = CustomerUserCreationForm
    template_name = 'registration/registro.html'
    success_url = reverse_lazy('login')

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/cambiar_password.html'
    success_url = reverse_lazy('libro_list')

# --- VISTAS CRUD DE LIBROS ---

class LibroListView(LoginRequiredMixin, ListView):
    model = Libro
    template_name = 'libros/libro_list.html'
    context_object_name = 'libros'
    paginate_by = 6

    def get_queryset(self):
        # Muestra únicamente los libros del usuario autenticado
        return Libro.objects.filter(usuario=self.request.user)

class LibroDetailView(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = 'libros/libro_detail.html'
    context_object_name = 'libro'

    def get_queryset(self):
        return Libro.objects.filter(usuario=self.request.user)

class LibroCreateView(LoginRequiredMixin, CreateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'
    success_url = reverse_lazy('libro_list')

    def form_valid(self, form):
        # Asigna el usuario autenticado al libro antes de guardar
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class LibroUpdateView(LoginRequiredMixin, UpdateView):
    model = Libro
    form_class = LibroForm
    template_name = 'libros/libro_form.html'

    def get_queryset(self):
        return Libro.objects.filter(usuario=self.request.user)

    def get_success_url(self):
        return reverse_lazy('libro_detail', kwargs={'pk': self.object.pk})

class LibroDeleteView(LoginRequiredMixin, DeleteView):
    model = Libro
    template_name = 'libros/libro_confirm_delete.html'
    success_url = reverse_lazy('libro_list')

    def get_queryset(self):
        return Libro.objects.filter(usuario=self.request.user)
    