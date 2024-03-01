from django import forms
from .models import Contacto, Producto, Pedido, CarritoArmarPC, Carrito
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .validators import MaxSizeFileValidator



class ContactoForms(forms.ModelForm):

    class Meta:
        model = Contacto
        fields = '__all__'



class ProductoForms(forms.ModelForm):

    imagen = forms.ImageField(required=True, validators=[MaxSizeFileValidator(max_file_size=4)])
    precio = forms.IntegerField(min_value=1, max_value=2000000)


    class Meta:
        model = Producto
        fields = '__all__'

        widgets = {
            'fecha_fabricacion': forms.TextInput(attrs={'type': 'date'}),
            # Otros widgets para otros campos si es necesario
        }



# forms.py

from .models import UserProfile

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su dirección'}))
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}))
    apellido = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}))
    #numero_telefono = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su número de teléfono'}))
    fecha_nacimiento = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    genero = forms.ChoiceField(choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], required=False, widget=forms.Select())
    #imagen_perfil = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))
    #biografia = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ingrese información sobre usted'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellido', 'email', 'direccion', 'fecha_nacimiento', 'genero',  'password1', 'password2']





class CustomUserCreationFormAdmin(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su dirección'}))
    nombre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su nombre'}))
    apellido = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ingrese sus apellidos'}))
    #numero_telefono = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'placeholder': 'Ingrese su número de teléfono'}))
    fecha_nacimiento = forms.DateField(required=False, widget=forms.TextInput(attrs={'type': 'date'}))
    genero = forms.ChoiceField(choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], required=False, widget=forms.Select())
    #imagen_perfil = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))
    #biografia = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ingrese información sobre usted'}), required=False)

    class Meta:
        model = User
        fields = ['username','nombre', 'apellido',"groups", "email",'direccion', 'fecha_nacimiento', 'genero', "password1","password2"]


# forms.py
from django import forms

class AgregarProductoForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), empty_label=None)
    cantidad = forms.IntegerField(min_value=1, initial=1)


# forms.py
from django import forms
from .models import Boleta

class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['usuario', 'valor_total']  # Puedes ajustar esto según tus necesidades


# forms.py
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django import forms
from .validators import validate_square_image


class UserProfileUpdateForm(forms.ModelForm):
    imagen_perfil = forms.ImageField(validators=[validate_square_image])

    class Meta:
        model = UserProfile
        fields = ['nombre', 'apellido','direccion', 'numero_telefono', 'fecha_nacimiento', 'genero', 'imagen_perfil', 'biografia']


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado', 'direccion_entrega']  # Añade otros campos si es necesario


from django import forms
from .models import Comentario

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido', 'evaluacion']



# forms.py
from django import forms
from .models import Version

class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['nombre']


from django import forms
from .models import Version

class BusquedaProductosForm(forms.Form):
    versiones = forms.ModelChoiceField(queryset=Version.objects.all(), required=False, label='Versión del producto')



# forms.py
from django import forms
from .models import Version

class BusquedaVersionForm(forms.Form):
    version = forms.ModelChoiceField(queryset=Version.objects.all(), empty_label='Todas las versiones', required=False)


# forms.py

from django import forms

class CarritoArmarPCForm(forms.ModelForm):
    equipo_armado = forms.BooleanField(required=False)
    descuento = forms.IntegerField(min_value=1, max_value=2000000)

    class Meta:
        model = CarritoArmarPC
        fields = ['descuento','equipo_armado']



# En tu archivo forms.py

from django import forms
from .models import Tarro

class TarroForm(forms.ModelForm):
    class Meta:
        model = Tarro
        fields = ['usuario', 'descripcion']  # Agrega aquí los campos que desees mostrar en el formulario


# forms.py


class CarritoForm(forms.ModelForm):

    descuento = forms.IntegerField(min_value=1, max_value=2000000)

    class Meta:
        model = Carrito
        fields = ['descuento']
