from django.urls import path
from .views import (
    LibroListView, LibroDetailView, LibroCreateView,
    LibroUpdateView, LibroDeleteView, CustomLoginView,
    CustomLogoutView, RegistroView, CustomPasswordChangeView
)

urlpatterns = [
    # Ruta raíz
    path('', LibroListView.as_view(), name='libro_list'),

    # Usuarios
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('cambiar-password/', CustomPasswordChangeView.as_view(), name='cambiar_password'),

    # Libros
    path('libro/nuevo/', LibroCreateView.as_view(), name='libro_create'),
    path('libro/<int:pk>/', LibroDetailView.as_view(), name='libro_detail'),
    path('libro/<int:pk>/editar/', LibroUpdateView.as_view(), name='libro_update'),
    path('libro/<int:pk>/eliminar/', LibroDeleteView.as_view(), name='libro_delete'),
]
