from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Producto, Categoria, CarritoArmarPC, Carrito, ItemCarrito, ListaDeseos
from .forms import ContactoForms, ProductoForms, CustomUserCreationForm, CustomUserCreationFormAdmin, PedidoForm, CarritoArmarPCForm, CarritoForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group

from django.shortcuts import render, redirect
from .models import CarritoArmarPC, Boleta, DetalleBoleta, Producto
# views.py

from django.shortcuts import render, redirect
from .models import CarritoArmarPC, Boleta, DetalleBoleta, Producto

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoArmarPC

from django.db import transaction

from django.db import transaction


from django.shortcuts import render
from .models import CarritoArmarPC, Producto, Version
from django.shortcuts import render
from .models import CarritoArmarPC, Producto, Version
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
import uuid


# Create your views here.


def es_bodeguero(user):
    return user.groups.filter(name='Bodeguero').exists()

def es_cliente(user):
    return user.groups.filter(name='Cliente').exists()

def es_Vendedor(user):
    return user.groups.filter(name='Vendedor').exists()

def es_Soporte(user):
    return user.groups.filter(name='Soporte').exists()



def es_Ensamblador(user):
    return user.groups.filter(name='Ensamblador').exists()
from django.urls import reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import render, redirect
from django.contrib import messages
import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BoletaForm
from .models import Boleta, DetalleBoleta

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import F  # Importa F para manejar decremento de stock
from .forms import BoletaForm
from .models import Boleta, DetalleBoleta, CarritoArmarPC
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from .models import CarritoArmarPC, DetalleBoleta, Boleta
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoArmarPC, Version
from django.contrib.auth.decorators import login_required




@login_required
def iniciar_pago(request):
    # Obtener detalles del carrito
    carrito_armar_pc, creado = CarritoArmarPC.objects.get_or_create(usuario=request.user)

    # Verificar si el carrito está completo
    if None in carrito_armar_pc.obtener_productos_dict().values():
        messages.error(request, "Faltan componentes para tu PC. Asegúrate de tener un producto por categoría.")
        return redirect('ver_carrito_armar_pc')

    for producto_nombre, producto in carrito_armar_pc.obtener_productos_dict().items():
        cantidad_en_carrito = 1  # Puedes ajustar esto según tus necesidades
        if cantidad_en_carrito > producto.stock:
            messages.error(request, f"No hay suficiente stock para {producto.nombre}. Actualmente hay {producto.stock} unidades disponibles.")
            return redirect('ver_carrito_armar_pc')

    # Verificar si todas las categorías tienen la misma versión en el carrito
    productos_dict = carrito_armar_pc.obtener_productos_dict()
    versiones_en_carrito = Version.objects.filter(id__in=[producto.version.id for producto in productos_dict.values() if producto])

    alert_message = None
    show_alert = False

    if len(set(versiones_en_carrito)) != 1:
        alert_message = 'Todos los productos en el carrito deben ser de la misma versión.'
        messages.warning(request, alert_message)
        show_alert = True

    




    host = request.get_host()

    # Calcular el total del carrito

    # Calcular el total del carrito
    total_carrito = carrito_armar_pc.calcular_total()

    equipo_armado = carrito_armar_pc.equipo_armado
    if equipo_armado:
        total_carrito += 20  # Agregar $20 al total

# Aplicar el IVA al total
    total_con_iva = total_carrito * 1.19

# Agregamos el carrito al contexto para que esté disponible en la plantilla
    context = {
    'productos_dict': productos_dict,
    'total_carrito': total_carrito,
    'total_con_iva': total_con_iva,  # Nuevo campo con IVA
    'alert_message': alert_message,
    'show_alert': show_alert,
}

    # Si hay alerta, regresa a la página del carrito
    if show_alert:
        return redirect('ver_carrito_armar_pc')

    # Crear un diccionario con los detalles del pago
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(total_con_iva),
        'item_name': 'Compra en tu tienda',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
        'items': [
            {
                'name': producto.nombre,
                'quantity': 1,
                'price': producto.precio,
                'currency_code': 'USD',
            }
            for producto in productos_dict.values() if producto
        ],
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context['form'] = form  # Agregamos el formulario al contexto

    return render(request, 'app/iniciar_pago.html', context)




# views.py


# views.py
from .models import DetallePedido

from django.shortcuts import render, redirect, get_object_or_404
from .models import Boleta, Pedido, DetallePedido, UserProfile
from django.db.models import F
from django.contrib import messages

def paypal_return(request):
    # Obtener el carrito de armar PC del usuario
    carrito, creado = CarritoArmarPC.objects.get_or_create(usuario=request.user)
    
    # Verificar si el carrito está vacío
    if carrito.calcular_total() == 0:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de proceder al pago.")
        return redirect('ver_carrito_armar_pc')  # Redirige al usuario a la vista del carrito

    # Crear una nueva boleta solo si hay productos en el carrito
    nueva_boleta = Boleta(usuario=request.user, valor_total=carrito.calcular_total())
    nueva_boleta.save()

    # Crear un nuevo pedido asociado a la boleta
    nuevo_pedido = Pedido(cliente=request.user, estado='preparacion', boleta=nueva_boleta)
    perfil_usuario = UserProfile.objects.get(user=request.user)
    nuevo_pedido.direccion_entrega = perfil_usuario.direccion  # Agregar la dirección al pedido
    nuevo_pedido.save()
  
    # Crear detalles del pedido para cada producto en el carrito
    for producto in carrito.obtener_productos_dict().values():
        cantidad = 1  # Puedes ajustar esto según tus necesidades

        # Crear el detalle del pedido con la cantidad
        DetallePedido.objects.create(
            pedido=nuevo_pedido,
            producto=producto,
            cantidad=cantidad,
        )

        # Actualizar el stock del producto utilizando F para manejar concurrencia
        producto.stock = F('stock') - cantidad
        producto.save()

    # Limpiar el carrito del usuario
    carrito.limpiar_carrito()

    messages.success(request, 'Pago aceptado. La boleta y el pedido han sido generados.')

    # Redirigir al usuario a la página de detalles del pedido recién creado
    return redirect('detalle_pedido', pedido_id=nuevo_pedido.id)




def paypal_cancel(request):
    messages.error(request,'No aceptado, intentalo denuevo')
    return redirect('ver_carrito_armar_pc')

#-------------------------------------------------------------------------------------------------------


from django.shortcuts import get_object_or_404
from .models import Carrito, ItemCarrito, Producto, Pedido
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
import uuid
from .models import Carrito

def iniciar_pago_componentes(request):
    # Obtener el carrito del usuario actual
    carrito = get_object_or_404(Carrito, usuario=request.user)

    # Verificar si el carrito está vacío
    if carrito.itemcarrito_set.count() == 0:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de proceder al pago.")
        return redirect('ver_carrito')  # Redirige al usuario a la vista del carrito

    # Verificar el stock de cada producto en el carrito
    for item in carrito.itemcarrito_set.all():
        if item.cantidad > item.producto.stock:
            messages.error(request, f"El producto '{item.producto.nombre}' no tiene suficiente stock.")
            return redirect('ver_carrito')  # Redirige al usuario a la vista del carrito

    # Calcular el total del carrito
    total_carrito = carrito.total
    total_con_iva = total_carrito * 1.19
    host = request.get_host()

    # Crear un diccionario con los detalles del pago
    paypal_dicts = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(total_con_iva),
        'item_name': 'Compra de productos',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("paypal-return-componentes")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel-componentes")}',
        'items': [
            {
                'name': item.producto.nombre,
                'quantity': item.cantidad,
                'price': item.producto.precio,
                'currency_code': 'USD',
            }
            for item in carrito.itemcarrito_set.all()
        ],
    }

    form = PayPalPaymentsForm(initial=paypal_dicts)
    context = {'form': form, 'total_carrito': total_carrito}
    return render(request, 'app/iniciar_pago_componentes.html', context)


from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import F
from .models import Carrito, Boleta, DetalleBoleta, Pedido, DetallePedido
from .models import DetalleBoleta

def paypal_return_componentes(request):
    # Obtener o crear el carrito del usuario
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    # Verificar si el carrito está vacío
    if carrito.itemcarrito_set.count() == 0:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de proceder al pago.")
        return redirect('ver_carrito')  # Redirige al usuario a la vista del carrito

    # Crear una nueva boleta
    nueva_boleta = Boleta(usuario=request.user, valor_total=carrito.calcular_total())
    nueva_boleta.save()

    # Crear un nuevo pedido asociado a la boleta
    nuevo_pedido = Pedido(cliente=request.user, estado='preparacion', boleta=nueva_boleta)

    # Acceder al perfil del usuario para obtener la dirección
    perfil_usuario = UserProfile.objects.get(user=request.user)
    nuevo_pedido.direccion_entrega = perfil_usuario.direccion  # Agregar la dirección al pedido
    nuevo_pedido.save()

    # Crear detalles de boleta para cada producto en el carrito
    for item in carrito.itemcarrito_set.all():
        cantidad = item.cantidad  # Puedes ajustar esto según tus necesidades
        precio_unitario = item.producto.precio  # Utiliza el precio del producto

        # Crear el detalle de la boleta con la cantidad y el precio unitario
        DetalleBoleta.objects.create(
            boleta=nueva_boleta,
            producto=item.producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
        )

        # Crear el detalle del pedido con la cantidad y la dirección
        DetallePedido.objects.create(
            pedido=nuevo_pedido,
            producto=item.producto,
            cantidad=cantidad,
        )

        # Actualizar el stock del producto utilizando F para manejar concurrencia
        item.producto.stock = F('stock') - cantidad
        item.producto.save()

    # Limpiar el carrito del usuario
    carrito.limpiar_carrito()

    messages.success(request, 'Pago aceptado. La boleta, el pedido y los detalles han sido generados.')
    return redirect('iniciar_pago_componentes')





def paypal_cancel_componentes(request):
    messages.error(request,'No aceptado, intentalo denuevo')
    return redirect('ver_carrito')







def home(request):

    is_cliente = request.user.groups.filter(name='Cliente').exists()
    is_soporte = request.user.groups.filter(name='Soporte').exists()
    is_vendedor = request.user.groups.filter(name='Vendedor').exists()
    is_bodeguero = request.user.groups.filter(name='Bodeguero').exists()
    is_ensamblador = request.user.groups.filter(name='Ensamblador').exists()
    

    context = {
        'is_cliente': is_cliente,
        'is_soporte': is_soporte,
        'is_vendedor': is_vendedor,
        'is_bodeguero': is_bodeguero,
        'is_ensamblador': is_ensamblador,
    }

    return  render(request, 'app/home.html', context)



from .forms import BusquedaProductosForm

def productos(request):
    is_cliente = request.user.groups.filter(name='Cliente').exists()
    is_soporte = request.user.groups.filter(name='Soporte').exists()
    is_vendedor = request.user.groups.filter(name='Vendedor').exists()
    is_bodeguero = request.user.groups.filter(name='Bodeguero').exists()
    is_ensamblador = request.user.groups.filter(name='Ensamblador').exists()

    if request.method == 'GET':
        form = BusquedaProductosForm(request.GET)
        if form.is_valid():
            version_seleccionada = form.cleaned_data.get('versiones')
            productos = Producto.objects.filter(version=version_seleccionada) if version_seleccionada else Producto.objects.all()
    else:
        form = BusquedaProductosForm()
        productos = Producto.objects.all()

    data = {
        'productos': productos,
        'is_cliente': is_cliente,
        'is_soporte': is_soporte,
        'is_vendedor': is_vendedor,
        'is_bodeguero': is_bodeguero,
        'is_ensamblador': is_ensamblador,
        'form': form,
    }

    return render(request, 'app/productos.html', data)



@login_required
def contacto(request):
    data ={
        'form': ContactoForms()
    }
    if request.method == 'POST':
        formulario = ContactoForms(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Mensaje Guardado"
        else:
            data["form"] = formulario

    return render(request, 'app/contacto.html', data)

@permission_required('app.add_producto')
def agregar_productos(request):

    data ={
        'form': ProductoForms()

    }
    if request.method == 'POST':
        formulario = ProductoForms(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Producto Registrado")
            return redirect(to="agregar_productos")
        else:
            data["form"] = formulario


    return render(request, 'app/productos/agregar_productos.html',data)

@permission_required('app.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos,10)
        productos = paginator.page(page)

    except:
        raise Http404
    
    data = {

        'productos': productos,
        'paginator': paginator

    }

    return render(request, 'app/productos/listar_productos.html', data)

@permission_required('app.change_producto')
def modificar_productos(request, id):

    producto = get_object_or_404(Producto, id=id)

    data ={

        'form': ProductoForms(instance=producto)

    }

    if request.method == 'POST':
        formulario = ProductoForms(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_productos")
        else:
            data["form"] = formulario

    return render(request, 'app/productos/modificar_productos.html', data)

@permission_required('app.delete_producto')
def eliminar_productos(request,id):
    
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_productos")
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import CustomUserCreationForm
from .models import UserProfile

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.save()

            # Crear un perfil asociado al usuario con los nuevos datos
            UserProfile.objects.create(
                user=usuario,
                direccion=formulario.cleaned_data["direccion"],
                nombre=formulario.cleaned_data["nombre"],
                apellido=formulario.cleaned_data["apellido"],
                fecha_nacimiento=formulario.cleaned_data["fecha_nacimiento"],
                genero=formulario.cleaned_data["genero"]
                # Puedes agregar más campos según sea necesario
            )

            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)

            # Agregar al usuario al grupo "Cliente" por defecto
            grupo_cliente = Group.objects.get(name='Cliente')
            usuario.groups.add(grupo_cliente)

            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")

        data['form'] = formulario

    return render(request, 'registration/registro.html', data)

def registro_admin(request):
    data = {
        'form': CustomUserCreationFormAdmin()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationFormAdmin(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.save()

            # Crear un perfil asociado al usuario con los nuevos datos
            UserProfile.objects.create(
                user=usuario,
                direccion=formulario.cleaned_data["direccion"],
                nombre=formulario.cleaned_data["nombre"],
                apellido=formulario.cleaned_data["apellido"],
                fecha_nacimiento=formulario.cleaned_data["fecha_nacimiento"],
                genero=formulario.cleaned_data["genero"]
                # Puedes agregar más campos según sea necesario
            )


            messages.success(request, "Te has registrado correctamente")
            return redirect(to="home")

        data['form'] = formulario

    return render(request, 'registration/registro_admin.html', data)


def exit(request):
    logout(request)
    return redirect('home')


# views.py

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ComentarioForm

# views.py

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Producto, Pedido
from .forms import ComentarioForm
# views.py

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Producto, Pedido
from .forms import ComentarioForm
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto, Pedido, Comentario
from .forms import ComentarioForm

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Verificar si el usuario tiene pedidos entregados que incluyen el producto
    tiene_pedidos_entregados = Pedido.objects.filter(
        cliente=request.user,
        estado='entregado',
        detallepedido__producto=producto
    ).exists()

    if not tiene_pedidos_entregados:
        return render(request, 'app/productos/detalle_producto.html', {'producto': producto})

    form = ComentarioForm()  # Mover la definición de form aquí

    if request.method == 'POST':
        # Verificar si el usuario ya ha dejado un comentario para este producto
        if not Comentario.objects.filter(producto=producto, cliente=request.user).exists():
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.producto = producto
                comentario.cliente = request.user
                comentario.save()

                messages.success(request, 'Comentario y evaluación agregados correctamente.')
                return redirect('detalle_producto', producto_id=producto.id)
            else:
                messages.error(request, 'Error al procesar el formulario de comentario.')
        else:
            messages.warning(request, 'Ya has dejado un comentario para este producto.')

    if producto.stock == 0:
        messages.warning(request, "Este Producto está Agotado")

    return render(request, 'app/productos/detalle_producto.html', {'producto': producto, 'form': form})





def lista_categorias(request):
    # Obtén todas las categorías únicas de productos
    categorias = Producto.objects.values('categoria').distinct()
    return render(request, 'app/productos/lista_categorias.html', {'categorias': categorias})

from .forms import BusquedaVersionForm

def productos_por_categoria(request, categoria_id):
    categoria_seleccionada = Categoria.objects.get(pk=categoria_id)

    # Obtén la categoría seleccionada para mostrarla en la plantilla
    productos = Producto.objects.filter(categoria=categoria_id)

    # Manejo de la búsqueda por versión
    form = BusquedaVersionForm(request.GET)
    if form.is_valid():
        version_seleccionada = form.cleaned_data.get('version')
        if version_seleccionada:
            productos = productos.filter(version=version_seleccionada)

    return render(request, 'app/productos/productos_por_categoria.html', {
        'productos': productos,
        'categoria_seleccionada': categoria_seleccionada,
        'form': form,  # Pasamos el formulario a la plantilla
        'categoria_id': categoria_id,  # Añadimos categoria_id al contexto
    })






# Otras importaciones aquí...



@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.itemcarrito_set.all()


    if request.method == 'POST':
        form = CarritoForm(request.POST, instance=carrito)
        if form.is_valid():
            # Guarda el valor del campo equipo_armado en la sesión o la base de datos
            form.save()
            messages.success(request, "Carrito actualizado correctamente.")
            return redirect('ver_carrito')
    else:
        form = CarritoForm(instance=carrito)

    # Agrega el código para obtener las variables is_cliente, is_soporte, is_vendedor e is_bodeguero
    is_cliente = request.user.groups.filter(name='Cliente').exists()
    is_soporte = request.user.groups.filter(name='Soporte').exists()
    is_vendedor = request.user.groups.filter(name='Vendedor').exists()
    is_bodeguero = request.user.groups.filter(name='Bodeguero').exists()
    is_ensamblador = request.user.groups.filter(name='Ensamblador').exists()

    context = {
        'carrito': carrito,
        'items': items,
        'is_cliente': is_cliente,
        'is_soporte': is_soporte,
        'is_vendedor': is_vendedor,
        'is_bodeguero': is_bodeguero,
        'is_ensamblador': is_ensamblador,
        'form': form,
    }

    # Verificar si el usuario intentó procesar el pago y el carrito está vacío
    if request.GET.get('pago_intentado') and not items:
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de procesar el pago.")
        return redirect('ver_carrito')

    return render(request, 'app/ver_carrito.html', context)



@login_required
def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, item_creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)

    if not item_creado:
        if item.cantidad + 1 > item.producto.stock:
            messages.error(request, f"No hay suficiente stock para {item.producto.nombre}. Actualmente hay {item.producto.stock} unidades disponibles.")
            return redirect('detalle_producto', producto_id=producto_id)
        item.cantidad += 1
        item.save()

    carrito.actualizar_total()

    return redirect('ver_carrito')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Carrito, Producto





from django.shortcuts import redirect
from .models import Carrito, CarritoArmarPC, ItemCarrito

from django.db import transaction

@login_required
def agregar_al_carrito_componentes(request):
    carrito_componentes, creado = Carrito.objects.get_or_create(usuario=request.user)

    # Obtener todos los productos del carrito de armar PC
    carrito_armar_pc, _ = CarritoArmarPC.objects.get_or_create(usuario=request.user)
    productos_en_carrito_armar_pc = carrito_armar_pc.obtener_productos_dict().values()

    # Agregar cada producto al carrito de componentes
    with transaction.atomic():
        for producto in productos_en_carrito_armar_pc:
            # Asegurarse de que el producto no sea None y tenga un id válido
            if producto and producto.id:
                # Crear un nuevo ItemCarrito en el carrito de componentes
                item, _ = ItemCarrito.objects.get_or_create(carrito=carrito_componentes, producto=producto)
                # Ajustar la cantidad según sea necesario
                # item.cantidad = ... 
                # item.save()

        # Limpiar el carrito de Armar PC después de agregar los productos al carrito de componentes
        carrito_armar_pc.limpiar_carrito()

    return redirect('ver_carrito')  # Ajusta el nombre de la URL según tu configuración






@login_required
def quitar_del_carrito(request, itemcarrito_id):
    item = ItemCarrito.objects.get(id=itemcarrito_id)
    item.delete()

    carrito = Carrito.objects.get(usuario=request.user)
    carrito.actualizar_total()

    return redirect('ver_carrito')


from django.contrib.auth.decorators import login_required
from .models import ListaDeseos

@login_required
def ver_wishlist(request):
    wishlist, created = ListaDeseos.objects.get_or_create(usuario=request.user)

    # Agrega el código para determinar los roles del usuario al contexto
    is_cliente = request.user.groups.filter(name='Cliente').exists()
    is_soporte = request.user.groups.filter(name='Soporte').exists()
    is_vendedor = request.user.groups.filter(name='Vendedor').exists()
    is_bodeguero = request.user.groups.filter(name='Bodeguero').exists()
    is_ensamblador = request.user.groups.filter(name='Ensamblador').exists()

    context = {
        'wishlist': wishlist,
        'is_cliente': is_cliente,
        'is_soporte': is_soporte,
        'is_vendedor': is_vendedor,
        'is_bodeguero': is_bodeguero,
        'is_ensamblador': is_ensamblador
    }

    return render(request, 'app/productos/ver_wishlist.html', context)


@login_required
def agregar_a_wishlist(request, producto_id):
    wishlist, created = ListaDeseos.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Producto, id=producto_id)
    wishlist.productos.add(producto)
    wishlist.save()
    return redirect('ver_wishlist')

@login_required
def quitar_de_wishlist(request, producto_id):
    wishlist, created = ListaDeseos.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Producto, id=producto_id)
    wishlist.productos.remove(producto)
    wishlist.save()
    return redirect('ver_wishlist')




@login_required
@transaction.atomic
def procesar_pago_carrito(request):
    # Obtener el carrito del usuario
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)

    # Verificar que el carrito no esté vacío
    if not carrito.itemcarrito_set.exists():
        messages.error(request, "Tu carrito está vacío. Agrega productos antes de procesar el pago.")
        return redirect('ver_carrito')

    # Verificar disponibilidad de stock antes de procesar el pago
    for item in carrito.itemcarrito_set.all():
        if item.cantidad > item.producto.stock:
            messages.error(request, f"No hay suficiente stock para {item.producto.nombre}. Actualmente hay {item.producto.stock} unidades disponibles.")
            return redirect('ver_carrito')

    # Calcular el total del carrito
    total_carrito = carrito.calcular_total()
    descuento = carrito.descuento
    total_con_iva = total_carrito * 1.19
    valor_total_con_descuento = max(0, total_con_iva - descuento)

    # Crear una boleta con los detalles de los productos en el carrito
    boleta = Boleta.objects.create(usuario=request.user, valor_total=valor_total_con_descuento)

    # Crear y asociar objetos DetalleBoleta para cada producto en el carrito
    detalles_boleta = []
    for item in carrito.itemcarrito_set.all():
        detalle = DetalleBoleta(
            boleta=boleta,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        detalles_boleta.append(detalle)

    # Guardar los objetos DetalleBoleta en la base de datos
    DetalleBoleta.objects.bulk_create(detalles_boleta)

    # Restar la cantidad comprada al stock de cada producto después de confirmar el pago
    for item in carrito.itemcarrito_set.all():
        item.producto.stock -= item.cantidad
        item.producto.save()

    # Limpiar el carrito después de procesar el pago
    carrito.itemcarrito_set.all().delete()
    carrito.actualizar_total()

    # Redirigir a la página de confirmación de pago
    messages.success(request, "Pago exitoso. Gracias por tu compra.")
    return render(request, 'app/confirmacion_pago_carrito.html', {'boleta': boleta})




from django.template.defaultfilters import slugify




#--------------------------------------------------------------------
def agregar_al_carrito_armar_pc(request, producto_id):
    # Obtén el producto y su categoría
    producto = get_object_or_404(Producto, id=producto_id)
    categoria = producto.categoria.nombre  # Aquí asumimos que el campo 'nombre' contiene el nombre de la categoría

    # Obtén el carrito de armar PC del usuario
    carrito, creado = CarritoArmarPC.objects.get_or_create(usuario=request.user)

    # Determina a qué campo del carrito de armar PC agregar el producto
    setattr(carrito, categoria.lower().replace(" ", "_"), producto)

    # Guarda los cambios en el carrito
    carrito.save()

    # Agrega un mensaje de éxito
    messages.success(request, f"Producto agregado al carrito de Armar PC ({categoria.capitalize()})")

    return redirect('detalle_producto', producto_id=producto_id)


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import CarritoArmarPC, Producto

from django.shortcuts import get_object_or_404

from django.shortcuts import get_object_or_404, redirect
from .models import CarritoArmarPC
from django.contrib import messages

# En views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import CarritoArmarPC
from django.contrib import messages



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CarritoArmarPC
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoArmarPC, Version
from django.contrib.auth.decorators import login_required

def ver_carrito_armar_pc(request):
    carrito_armar_pc, creado = CarritoArmarPC.objects.get_or_create(usuario=request.user)

    total = carrito_armar_pc.calcular_total()
    productos_dict = carrito_armar_pc.obtener_productos_dict()

    versiones_en_carrito = Version.objects.filter(id__in=[producto.version.id for producto in productos_dict.values() if producto])

    alert_message = None
    show_alert = False
    producto_id = None


    if request.method == 'POST':
        form = CarritoArmarPCForm(request.POST, instance=carrito_armar_pc)
        if form.is_valid():
            # Guarda el valor del campo equipo_armado en la sesión o la base de datos
            form.save()
            messages.success(request, "Carrito actualizado correctamente.")
            return redirect('ver_carrito_armar_pc')
    else:
        form = CarritoArmarPCForm(instance=carrito_armar_pc)

    # Verificar si el carrito está vacío
    if all(producto is None for producto in productos_dict.values()):
        messages.warning(request, "Tu carrito está vacío.")

    else:
        
        if len(set(versiones_en_carrito)) != 1:
            alert_message = 'Todos los productos en el carrito deben ser de la misma versión.'
            messages.warning(request, alert_message)
            show_alert = True
        else:
            alert_message = 'El carrito de Armar PC se ha verificado con éxito. Puedes proceder con el pago.'
            messages.success(request, alert_message)

        
        

    

    
    # Agrega el contexto adicional
    is_cliente = request.user.groups.filter(name='Cliente').exists()
    is_soporte = request.user.groups.filter(name='Soporte').exists()
    is_vendedor = request.user.groups.filter(name='Vendedor').exists()
    is_bodeguero = request.user.groups.filter(name='Bodeguero').exists()
    is_ensamblador = request.user.groups.filter(name='Ensamblador').exists()

    context = {
        'producto_id': producto_id,
        'carrito_armar_pc': carrito_armar_pc,
        'productos_dict': productos_dict,
        'versiones': versiones_en_carrito,
        'total': total,
        'is_cliente': is_cliente,
        'is_soporte': is_soporte,
        'is_vendedor': is_vendedor,
        'is_bodeguero': is_bodeguero,
        'is_ensamblador': is_ensamblador,
        'alert_message': alert_message,
        'show_alert': show_alert,
        'form':form
    }

    return render(request, 'app/carrito_armar_pc.html', context)




# views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import CarritoArmarPC, DetalleBoleta, Boleta

def calcular_valor_total(carrito):
    return sum([producto.precio for producto in carrito.obtener_productos_dict().values()])

from django.db import transaction


from .models import Version

from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoArmarPC, DetalleBoleta, Boleta


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CarritoArmarPC, Boleta, DetalleBoleta
from django.db import transaction

@login_required
@transaction.atomic
def procesar_pago(request):
    carrito_armar_pc, creado = CarritoArmarPC.objects.get_or_create(usuario=request.user)

    # Verificar si todas las categorías tienen un producto asignado en el carrito
    if None in carrito_armar_pc.obtener_productos_dict().values():
        messages.error(request, "Faltan componentes para tu PC. Asegúrate de tener un producto por categoría.")
        return redirect('ver_carrito_armar_pc')

    # Verificar disponibilidad de stock antes de procesar el pago
    for producto_nombre, producto in carrito_armar_pc.obtener_productos_dict().items():
        cantidad_en_carrito = 1  # Puedes ajustar esto según tus necesidades
        if cantidad_en_carrito > producto.stock:
            messages.error(request, f"No hay suficiente stock para {producto.nombre}. Actualmente hay {producto.stock} unidades disponibles.")
            return redirect('ver_carrito_armar_pc')

    # Verificar que todos los productos en el carrito tengan la misma versión
    versiones_en_carrito = Version.objects.filter(id__in=[producto.version.id for producto in carrito_armar_pc.obtener_productos_dict().values() if producto])

    if len(set(versiones_en_carrito)) != 1:
        messages.error(request, "Todos los productos en el carrito deben ser de la misma versión.")
        return redirect('ver_carrito_armar_pc')

    # Calcular el valor total del carrito y restar el descuento
    valor_total = calcular_valor_total(carrito_armar_pc)
    descuento = carrito_armar_pc.descuento
    valor_total_con_descuento = max(0, valor_total - descuento)

    # Aplicar el IVA al total
    total_con_iva = valor_total_con_descuento * 1.19

    # Agregar el carrito al contexto para que esté disponible en la plantilla
    context = {
        'total_carrito': valor_total,
        'total_con_iva': total_con_iva,  # Nuevo campo con IVA
    }

    # Crear una boleta con los detalles de los productos
    with transaction.atomic():
        boleta = Boleta.objects.create(usuario=request.user, valor_total=valor_total_con_descuento)

        # Crear y asociar objetos DetalleBoleta para cada producto en el carrito
        detalles_boleta = []
        for producto_nombre, producto in carrito_armar_pc.obtener_productos_dict().items():
            cantidad = 1  # Puedes ajustar esto según tus necesidades
            precio_unitario = producto.precio  # Utiliza el precio del producto
            detalles_boleta.append(DetalleBoleta(producto=producto, cantidad=cantidad, boleta=boleta, precio_unitario=precio_unitario))

            # Actualizar el stock del producto
            producto.stock -= cantidad
            producto.save()

        # Guardar los objetos DetalleBoleta en la base de datos
        DetalleBoleta.objects.bulk_create(detalles_boleta)

        # Limpiar el carrito del usuario
        carrito_armar_pc.limpiar_carrito()

    # Mostrar la alerta de pago exitoso
    messages.success(request, "Pago exitoso. Gracias por tu compra.")

    # Redirigir a una página de confirmación de pago
    return render(request, 'app/confirmacion_pago.html', {'boleta': boleta})




#-------------------------
# views.py

from django.shortcuts import render, redirect
from .forms import UserProfileUpdateForm  # Asegúrate de importar tu formulario


# views.py

from django.shortcuts import render
from .models import UserProfile

def ver_perfil(request):
    perfil_usuario = UserProfile.objects.get(user=request.user)


    is_cliente = request.user.groups.filter(name='Cliente').exists()
    is_soporte = request.user.groups.filter(name='Soporte').exists()
    is_vendedor = request.user.groups.filter(name='Vendedor').exists()
    is_bodeguero = request.user.groups.filter(name='Bodeguero').exists()
    is_ensamblador = request.user.groups.filter(name='Ensamblador').exists()
    

    context = {
        'perfil_usuario': perfil_usuario,
        'is_cliente': is_cliente,
        'is_soporte': is_soporte,
        'is_vendedor': is_vendedor,
        'is_bodeguero': is_bodeguero,
        'is_ensamblador': is_ensamblador,
    }
    return render(request, 'app/ver_perfil.html', context)





# views.py

from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserProfileUpdateForm

def modificar_perfil(request):
    perfil_usuario = request.user.userprofile

    if request.method == 'POST':
        formulario = UserProfileUpdateForm(request.POST, request.FILES, instance=perfil_usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Perfil modificado correctamente.")
            return redirect('ver_perfil')
    else:
        formulario = UserProfileUpdateForm(instance=perfil_usuario)

    return render(request, 'app/modificar_perfil.html', {'formulario': formulario})



# views.py
# views.py

from django.shortcuts import render
from .models import Pedido, DetallePedido
from django.contrib.auth.decorators import login_required

@login_required
def ver_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user)
    context = {'pedidos': pedidos}
    return render(request, 'app/ver_pedidos.html', context)


def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    context = {'pedido': pedido}
    return render(request, 'app/detalle_pedido.html', context)


def ver_pedidos_global(request):
    pedidos = Pedido.objects.all()
    return render(request, 'app/ver_pedidos_global.html', {'pedidos': pedidos})

from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Pedido
from .forms import PedidoForm

@login_required
def detalle_pedido_global(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Verificar si el usuario es vendedor o ensamblador
    if request.method == 'POST' and (request.user.groups.filter(name='Vendedor').exists() or request.user.groups.filter(name='Ensamblador').exists()):
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            # Actualizar la información del pedido
            pedido = form.save(commit=False)

            # Establecer el usuario que realizó la modificación
            pedido.modificado_por = request.user

            # Establecer la fecha de modificación
            pedido.fecha_modificacion = timezone.now()

            # Asegurarse de que el vendedor o ensamblador se establezca correctamente
            if request.user.groups.filter(name='Vendedor').exists():
                pedido.vendedor = request.user
            elif request.user.groups.filter(name='Ensamblador').exists():
                pedido.ensamblador = request.user

            pedido.save()

            messages.success(request, 'Estado del pedido actualizado correctamente.')
            return redirect('ver_pedidos_global')
    else:
        form = PedidoForm(instance=pedido)

    return render(request, 'app/detalle_pedido_global.html', {'pedido': pedido, 'form': form})


# views.py
from django.shortcuts import render, redirect
from .forms import VersionForm
from django.contrib import messages

def agregar_version(request):
    if request.method == 'POST':
        form = VersionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nueva versión agregada correctamente.')
            return redirect('lista_versiones')  # Puedes ajustar esto según tus URLs
    else:
        form = VersionForm()

    return render(request, 'app/gestion/agregar_version.html', {'form': form})



# views.py
from django.shortcuts import render
from .models import Version

def lista_versiones(request):
    versiones = Version.objects.all()
    return render(request, 'app/gestion/lista_versiones.html', {'versiones': versiones})

from django.shortcuts import render, get_object_or_404
from .models import Version
from .forms import VersionForm  # Asegúrate de importar el formulario correcto

def editar_version(request, version_id):
    version = get_object_or_404(Version, id=version_id)

    if request.method == 'POST':
        form = VersionForm(request.POST, instance=version)
        if form.is_valid():
            form.save()
    else:
        form = VersionForm(instance=version)

    return render(request, 'app/gestion/editar_version.html', {'version': version, 'form': form})

def guardar_edicion_version(request, version_id):
    version = get_object_or_404(Version, id=version_id)
    if request.method == 'POST':
        form = VersionForm(request.POST, instance=version)
        if form.is_valid():
            form.save()
            # Redirigir a la lista de versiones o a donde desees
            return redirect('lista_versiones')
    return render(request, 'app/gestion/editar_version.html', {'version': version, 'form': form})


from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from .models import Producto

@require_POST
def desactivar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Desactivar el producto
    producto.activo = False
    producto.save()

    # Puedes devolver una respuesta JSON indicando el éxito de la operación si es necesario
    return JsonResponse({'message': 'Producto desactivado correctamente'})

@require_POST
def activar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Activar el producto
    producto.activo = True
    producto.save()

    # Puedes devolver una respuesta JSON indicando el éxito de la operación si es necesario
    return JsonResponse({'message': 'Producto activado correctamente'})



# En tu archivo views.py

from django.shortcuts import render, redirect
from .forms import TarroForm
# views.py
def crear_tarro(request):
    if request.method == 'POST':
        form = TarroForm(request.POST)
        if form.is_valid():
            tarro = form.save(commit=False)
            # Asignar el usuario actual al tarro
            
            tarro.save()
            return redirect('lista_tarros')  # Redirigir a la página de lista de tarros o a donde desees
    else:
        form = TarroForm()

    return render(request, 'app/crear_tarro.html', {'form': form})



# En tu archivo views.py

from django.shortcuts import render
from .models import Tarro  # Asegúrate de importar el modelo Tarro

def lista_tarros(request):
    tarros = Tarro.objects.all()  # Obtener todos los tarros
    return render(request, 'app/lista_tarros.html', {'tarros': tarros})


# En tu archivo views.py

from django.shortcuts import render, get_object_or_404
from .models import Tarro  # Asegúrate de importar el modelo Tarro

def detalle_tarro(request, tarro_id):
    tarro = get_object_or_404(Tarro, id=tarro_id)
    return render(request, 'app/detalle_tarro.html', {'tarro': tarro})
