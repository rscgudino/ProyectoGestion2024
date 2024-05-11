from re import template
from django.shortcuts import redirect, render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from django.views.generic import CreateView, TemplateView,ListView,UpdateView
from usuarios.forms import NuevoUsuarioForm,CustomPasswordChangeForm,CambioGrupoForm
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

# Create your views here.


class NuevoUsuario(PermissionRequiredMixin,CreateView):
    permission_required='auth.add_user'
    model = User
    form_class = NuevoUsuarioForm
    template_name="usuarios/nuevo_usuario.html"
    context_object_name='form'

    def form_valid(self, form):
        form.save()
        form.cleaned_data['grupo'].user_set.add(form.instance)
        return redirect('/usuarios')


class Mostrar(PermissionRequiredMixin,ListView):
    permission_required='auth.view_user'
    model = User
    template_name = 'usuarios/usuarios.html'
    context_object_name = 'usuarios'
    queryset = User.objects.filter(is_staff=False).order_by('username')


@permission_required('auth.change_user')
def editar_usuario(request, id_user):
    try:
        usuario = User.objects.get(pk=id_user)
    except User.DoesNotExist:
        return render(request, '404_admin.html')
    
    form_EditUser = CustomPasswordChangeForm(user=usuario)
    form_GrupoNuevo=CambioGrupoForm(prefix='nuevoGrupo')
    
    if request.method == 'POST':
        if 'nueva_pass' in request.POST:
            form_EditUser = CustomPasswordChangeForm(user=usuario, data=request.POST)
            if form_EditUser.is_valid():
                form_EditUser.save()
                return redirect('mostrar_usuarios')
        elif 'nuevo_grupo' in request.POST:
            form_GrupoNuevo=CambioGrupoForm(request.POST,prefix='nuevoGrupo')
            if form_GrupoNuevo.is_valid():
                grupo_actual=usuario.groups.get()
                grupo_actual.user_set.remove(usuario)
                form_GrupoNuevo.cleaned_data['grupo'].user_set.add(usuario)
            if request.user == usuario and form_GrupoNuevo.cleaned_data['grupo'].name != 'Administrador':
                return redirect('productos')
            else:
                return redirect('mostrar_usuarios')        

    template = 'usuarios/editar_usuario.html'
    context = {'id_user': id_user, 'form': form_EditUser,'formNuevoGrupo':form_GrupoNuevo,'usuario':usuario}
    return render(request, template, context)


@permission_required('auth.delete_user')
def eliminar_usuario(request,id_user):
    try:
        usuario =User.objects.get(pk=id_user)
    except User.DoesNotExist:
        return render(request, '404_admin.html')
    usuario.delete()
    return redirect('mostrar_usuarios')    


def inicio_sesion(request):
    if request.user.is_authenticated:
        return redirect('productos')
    
    if request.method == 'POST':
        # AuthenticationForm_can_also_be_used__
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            nxt = request.GET.get("next", None)
            if nxt is None:
                return redirect('productos')
            else:
                return redirect(nxt)
        else:
            messages.warning(request, f'Los datos ingresados son incorrectos.')
    form = AuthenticationForm()
    return render(request, 'usuarios/inicio_sesion.html', {'form': form, 'title': 'Log in'})
