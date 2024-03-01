from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from .models import Pedido, Producto

from django.contrib.auth.models import User

@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    print('IPN válido')
    ipn = sender
    if ipn.payment_status == 'Completed':
        try:
            # Intenta obtener un ID de usuario válido
            user_id = int(ipn.custom)
            # Intenta obtener el usuario correspondiente al ID
            cliente = User.objects.get(id=user_id)
            # Crea un pedido cuando el pago se completa
            pedido = Pedido.objects.create(cliente=cliente)

            # Recupera los productos asociados al carrito o boleta, 
            # y los agrega al pedido recién creado
            productos_en_carrito = Producto.objects.filter(carrito__usuario=cliente)
            pedido.productos.set(productos_en_carrito)

            print(f'Pedido creado con éxito: #{pedido.id}')
        except (ValueError, User.DoesNotExist):
            print('Error al obtener el usuario o el ID del usuario no es válido')


@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    print('IPN inválido')
    ipn = sender
    if ipn.payment_status == 'Completed':
        # Aquí puedes manejar casos específicos cuando el IPN es inválido
        print('Manejar casos específicos para IPN inválido')
