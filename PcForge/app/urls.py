from django.urls import path
from .views import home, productos,contacto, agregar_productos, listar_productos, \
      modificar_productos, eliminar_productos, registro, exit, registro_admin, detalle_producto,\
      lista_categorias, productos_por_categoria,agregar_al_carrito_armar_pc,\
      ver_carrito_armar_pc, ver_carrito, agregar_al_carrito, quitar_del_carrito, ver_wishlist, \
        agregar_a_wishlist, quitar_de_wishlist,procesar_pago,procesar_pago_carrito, iniciar_pago,\
        paypal_return,paypal_cancel,iniciar_pago_componentes, paypal_return_componentes, \
        paypal_cancel_componentes, ver_perfil,modificar_perfil, ver_pedidos, detalle_pedido,\
        ver_pedidos_global, detalle_pedido_global, agregar_version, lista_versiones, editar_version,\
        guardar_edicion_version,agregar_al_carrito_componentes, desactivar_producto, activar_producto, crear_tarro, lista_tarros, detalle_tarro
      
urlpatterns = [
    path('',home, name="home" ),
    path('productos/',productos, name="productos" ),
    path('contacto/',contacto, name="contacto" ),
    path('agregar-productos/',agregar_productos, name="agregar_productos" ),
    path('listar-productos/',listar_productos, name="listar_productos" ),
    path('modificar-productos/<id>/',modificar_productos, name="modificar_productos" ),
    path('eliminar-productos/<id>/',eliminar_productos, name="eliminar_productos" ),
    path('registro/',registro, name="registro" ),
    path('registro_admin/',registro_admin, name="registro_admin" ),
    path('Logout/', exit, name="exit"),
    path('productos/detalle/<int:producto_id>/', detalle_producto, name='detalle_producto'),
     path('categorias/', lista_categorias, name='lista_categorias'),
    path('productos_por_categoria/<int:categoria_id>/', productos_por_categoria, name='productos_por_categoria'),
    
    path('agregar_al_carrito_armar_pc/<int:producto_id>/', agregar_al_carrito_armar_pc, name='agregar_al_carrito_armar_pc'),
    
    
    path('ver_carrito_armar_pc/', ver_carrito_armar_pc, name='ver_carrito_armar_pc'),
    path('ver-pedidos/', ver_pedidos, name='ver_pedidos'),
    path('detalle-pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),

    

    path('ver-carrito/', ver_carrito, name='ver_carrito'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    

    path('quitar-del-carrito/<int:itemcarrito_id>/', quitar_del_carrito, name='quitar_del_carrito'),
    path('ver-wishlist/',ver_wishlist, name='ver_wishlist'),
    path('agregar-wishlist/<int:producto_id>/', agregar_a_wishlist, name='agregar_a_wishlist'),
    path('quitar-wishlist/<int:producto_id>/', quitar_de_wishlist, name='quitar_de_wishlist'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
    path('procesar_pago_carrito/', procesar_pago_carrito, name='procesar_pago_carrito'),


    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('paypal-reverse/', paypal_return, name='paypal-return'),
    path('paypal-cancel/', paypal_cancel, name='paypal-cancel'),


    path('iniciar_pago_componentes/', iniciar_pago_componentes, name='iniciar_pago_componentes'),
    path('paypal-return-componentes/', paypal_return_componentes, name='paypal-return-componentes'),
    path('paypal-cancel-componentes/', paypal_cancel_componentes, name='paypal-cancel-componentes'),
    path('ver-perfil/', ver_perfil, name='ver_perfil'),

    path('modificar-perfil/', modificar_perfil, name='modificar_perfil'),
    path('ver-pedidos-global/', ver_pedidos_global, name='ver_pedidos_global'),

    path('detalle-pedido-global/<int:pedido_id>/',detalle_pedido_global, name='detalle_pedido_global'),
    path('agregar_version/', agregar_version, name='agregar_version'),
    path('lista_versiones/', lista_versiones, name='lista_versiones'),
    path('editar_version/<int:version_id>/', editar_version, name='editar_version'),
    path('guardar_edicion_version/<int:version_id>/', guardar_edicion_version, name='guardar_edicion_version'),
    path('agregar_al_carrito_componentes/', agregar_al_carrito_componentes, name='agregar_al_carrito_componentes'),
    path('desactivar-producto/<int:producto_id>/', desactivar_producto, name='desactivar_producto'),
    path('activar-producto/<int:producto_id>/', activar_producto, name='activar_producto'),
    path('crear_tarro/', crear_tarro, name='crear_tarro'),
    path('lista_tarros/', lista_tarros, name='lista_tarros'),
    path('detalle_tarro/<int:tarro_id>/', detalle_tarro, name='detalle_tarro'),
    

]