from django.urls import path
from usuarios import views


urlpatterns = [
    path('', views.Mostrar.as_view(),name="mostrar_usuarios"),
    path('nuevo/', views.NuevoUsuario.as_view(), name='nuevo_usuario'),
    path('editar/<int:id_user>', views.editar_usuario, name='editar_usuario'),
    path('eliminar/<int:id_user>', views.eliminar_usuario,name='eliminar_usuario'),
    
]
