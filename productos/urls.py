from django.urls import path
from productos import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.ProductosMostrar.as_view(), name='productos'),
    path('nuevo/', views.producto_nuevo, name='nuevo_producto'),
    path('editar/<int:id_prod>/', views.producto_editar, name='editar_producto'),
    path('eliminar/<int:id_prod>/', views.producto_eliminar, name='eliminar_producto'),
    path('fabricantes/', views.FabricantesL.as_view(), name='fabricantes'),
    path('fabricantes/nuevo/', views.fabricante_nuevo, name='nuevo_fabricante'),
    path('fabricantes/editar/<int:id_fabr>', views.fabricante_editar, name='editar_fabricante'),
    path('fabricantes/eliminar/<int:id_fabr>', views.fabricante_eliminar, name='eliminar_fabricante'),
    path('modificar_stock/', views.stock, name='modificar_stock'),
    path('comprobantes/', views.VerComprobantes.as_view(), name='comprobantes'),
    path('comprobantes/<int:id_compr>/', views.comprobante_detalle, name='comprobante_detalle'),
    path('logout/', views.SalirLogoutView.as_view(), name='logout'),

]
    