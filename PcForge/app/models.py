from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User



from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    numero_telefono = models.CharField(max_length=15, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=10, choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], blank=True)
    imagen_perfil = models.ImageField(upload_to="perfil", null=True, blank=True)
    biografia = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"




class Marca(models.Model):
    nombre = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Version(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
class Tarro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=255)
    

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.IntegerField()
    nuevo = models.BooleanField()
    stock = models.IntegerField()
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    fecha_fabricacion = models.DateField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    imagen = models.ImageField(upload_to="productos", null=True, blank=True)
    version = models.ForeignKey(Version, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)  
    tarro = models.ForeignKey(Tarro, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre


    

opciones_consultas = [
[0, "Consulta"],
[1, "Reclamo"],
[2, "Sugerencia"],
[3, "Felicitaciones"],

]

class ListaDeseos(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField('Producto', related_name='wishlist')

    def __str__(self):
        return f'Wishlist de {self.usuario.username}'

class Contacto(models.Model):
    nombre = models.CharField(max_length=250)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre
    



class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')
    descuento =models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def calcular_total(self):
        return sum(item.subtotal() for item in self.itemcarrito_set.all())

    def actualizar_total(self):
        self.total = self.calcular_total()
        self.save()


    def limpiar_carrito(self):
        # Lógica para limpiar el carrito, si es necesario
        # Por ejemplo, puedes eliminar todos los elementos del carrito
        self.productos.clear()
        self.actualizar_total()

    def __str__(self):
        return f"Carrito de {self.usuario.username}"
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.carrito}"




from django.db import models
from .models import Producto

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class CarritoArmarPC(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    placa_base = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_placa_base')
    procesador = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_procesador')
    ram = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_ram')
    tarjeta_grafica = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_tarjeta_grafica')
    disco = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_disco')
    fuente_poder = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_fuente_poder')
    gabinete = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_gabinete')
    disipador = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='carrito_armar_pc_disipador')
    descuento =models.IntegerField(default=0)
    equipo_armado = models.BooleanField(default=False)
    total = models.IntegerField(default=0)

    def calcular_total(self):
        total = sum(producto.precio for producto in self.obtener_productos_dict().values() if producto)
        self.total = total
        self.save()
        return total

    def obtener_productos_dict(self):
        return {
            'Placa Base': self.placa_base,
            'Procesador': self.procesador,
            'RAM': self.ram,
            'Disco': self.disco,
            'Tarjeta Gráfica': self.tarjeta_grafica,
            'Disipador': self.disipador,
            'Gabinete': self.gabinete,
            'Fuente de Poder': self.fuente_poder,
        }



    def limpiar_carrito(self):
        for field_name in self._meta.get_fields():
            if field_name.name.startswith('carrito_armar_pc_') and isinstance(getattr(self, field_name.name), Producto):
                # Eliminar la referencia ForeignKey
                setattr(self, field_name.name, None)

        # Establecer todos los campos en None
        self.placa_base = None
        self.procesador = None
        self.ram = None
        self.tarjeta_grafica = None
        self.disco = None
        self.fuente_poder = None
        self.gabinete = None
        self.disipador = None

        self.total = 0
        self.save()
    


class Boleta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor_total = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Boleta ID {self.id} de {self.usuario.username}"

    

class DetalleBoleta(models.Model):
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, related_name='detalles_boleta')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()

    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario
    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Boleta {self.boleta.id}"
    

from django.db import models
from django.contrib.auth.models import User

# models.py

from django.db import models
from django.contrib.auth.models import User

class Comentario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    evaluacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Del 1 al 5
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.cliente.username} en {self.producto.nombre}"



class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('preparacion', 'En preparación'),
        ('ensamblaje', 'En Ensamblaje'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado'),
        # Agrega más estados según sea necesario
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_vendedor')
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='preparacion')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE)
    direccion_entrega = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.get_estado_display()}"
    

    def permitir_comentarios(self):
        # Lógica para determinar si se deben permitir comentarios basados en el estado del pedido
        return self.estado == 'entregado'


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad
    
    def __str__(self):
        return f"Detalle Pedido #{self.pedido.id}"