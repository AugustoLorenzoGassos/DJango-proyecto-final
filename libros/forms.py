from django import forms
from .models import Libro
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'descripcion', 'categoria', 'estado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario',  # <--- Aquí cambias la etiqueta
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu usuario'
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Ingresa tu contraseña'
        })
    )

class CustomerUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Usuario',
        help_text= 'Requerido. 150 caracteres o menos. Solo letras, dígitos y @/./+/-/_',
        widget=forms.TextInput(attrs={
            'class':'form-control'       
        })
    )
    password1 = forms.CharField(
        label="Contraseña",
        help_text='Mínimo 8 caracteres. No debe ser fácil de adivinar.',
        widget=forms.PasswordInput(attrs={
             'class':'form-control',
             'placeholder':'Crea tu contraseña segura'
        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        help_text='Mínimo 8 caracteres. No debe ser fácil de adivinar.',
        widget=forms.PasswordInput(attrs={
             'class':'form-control',
             'placeholder':'Repite tu contraseña segura'
        })
    )    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)
        # Sobrescribir el mensaje predeterminado cuando las contraseñas no coinciden
        error_messages = {
            'password_mismatch': 'Las contraseñas no coinciden. Por favor, verifica e inténtalo de nuevo.'
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Verificar si el usuario ya existe con mensaje en español
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está registrado. Elige otro.')
            
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        username = self.cleaned_data.get('username')

        if password1:
            user = User(username=username) if username else None
            try:
                validate_password(password1, user=user)
            except ValidationError as error:
                mensajes_espanol = {
                    'password_too_similar': 'La contraseña es demasiado similar al nombre de usuario.',
                    'password_too_short': 'La contraseña es demasiado corta. Debe tener al menos 8 caracteres.',
                    'password_too_common': 'Esta contraseña es muy común. Por favor elige una más segura.',
                    'password_entirely_numeric': 'La contraseña no puede estar compuesta solo por números.',
                }
                errores_traducidos = []
                for e in error.error_list:
                    mensaje = mensajes_espanol.get(e.code, e.message)
                    errores_traducidos.append(mensaje)

                # Elevar error asociado a password1
                raise forms.ValidationError(errores_traducidos)

        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')

        if password2:
            user = User(username=username) if username else None
            try:
                validate_password(password2, user=user)
            except ValidationError as error:
                mensajes_espanol = {
                    'password_too_similar': 'La contraseña es demasiado similar al nombre de usuario.',
                    'password_too_short': 'La contraseña es demasiado corta. Debe tener al menos 8 caracteres.',
                    'password_too_common': 'Esta contraseña es muy común. Por favor elige una más segura.',
                    'password_entirely_numeric': 'La contraseña no puede estar compuesta solo por números.',
                }
                errores_traducidos = []
                for e in error.error_list:
                    mensaje = mensajes_espanol.get(e.code, e.message)
                    errores_traducidos.append(mensaje)

                # Elevar error asociado a password1
                raise forms.ValidationError(errores_traducidos)

        return password2