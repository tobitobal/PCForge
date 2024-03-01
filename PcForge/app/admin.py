from django.contrib import admin

from .models import Marca, Categoria, Producto, Version, Contacto, Carrito,CarritoArmarPC, ItemCarrito, Boleta, DetalleBoleta, ListaDeseos, Pedido,DetallePedido,\
                    UserProfile, Comentario, Tarro
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "precio","stock", "nuevo", "marca", "categoria"]
    list_filter = ["version"]  # Agrega el filtro para modelos

class DetalleBoletaAdmin(admin.ModelAdmin):
    list_filter = ["boleta"]  # Agrega el filtro para modelos
    



# Registra los modelos para que aparezcan en el panel de administración
admin.site.register(Marca)
admin.site.register(Categoria)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Version)
admin.site.register(Contacto)
admin.site.register(Carrito)
admin.site.register(CarritoArmarPC)
admin.site.register(ItemCarrito)
admin.site.register(Boleta)
admin.site.register(DetalleBoleta, DetalleBoletaAdmin)
admin.site.register(ListaDeseos)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(UserProfile)
admin.site.register(Comentario)
admin.site.register(Tarro)