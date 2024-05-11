from re import template
from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from productos.forms import NuevoProductoForm, NuevoFabricanteForm,EditarProductoForm, EditarFabricanteForm,ModificarStockForm,ModificarStockArticulosForm
from django.contrib import messages
from django.views.generic import ListView
from productos.models import Fabricante,Item,Comprobante,ComprobanteProducto
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import formset_factory
from django.forms.models import modelformset_factory

#Create your views here.

class ProductosMostrar(PermissionRequiredMixin, ListView):
    permission_required='productos.view_item'
    model = Item
    template_name = 'productos/productos.html'
    context_object_name = 'productos'
    queryset = Item.objects.all().order_by('nombre')


@permission_required('add_item')
def producto_nuevo(request):
    if request.method == 'POST':
        form_ingresarProducto=NuevoProductoForm(request.POST)
        if form_ingresarProducto.is_valid():
            messages.success(request, 'Nuevo artículo agregado correctamente')
            form_ingresarProducto.save()
            form_ingresarProducto = NuevoProductoForm()
        else:
            messages.warning(request, 'Error en los datos cargados')
    elif request.method=='GET':
        form_ingresarProducto = NuevoProductoForm()
    
    template = loader.get_template('productos/producto_nuevo.html')
    context={'form_nuevoProd':form_ingresarProducto}
    return HttpResponse(template.render(context,request))

@permission_required('change_item')
def producto_editar(request,id_prod):
    try:
        producto =Item.objects.get(pk=id_prod)
    except Item.DoesNotExist:
        return render(request, '404_admin.html')

    if (request.method == 'POST'):
        form_EditProd = EditarProductoForm(request.POST, instance=producto)
        if form_EditProd.is_valid():
            form_EditProd.save()
            return redirect('productos')
    else:
        form_EditProd = EditarProductoForm(instance=producto)
    return render(request, 'productos/producto_editar.html', {'formEditarProd': form_EditProd})

@permission_required('delete_item')
def producto_eliminar(request,id_prod):
    try:
        producto =Item.objects.get(pk=id_prod)
    except Item.DoesNotExist:
        return render(request, '404_admin.html')
    producto.delete()
    return redirect('productos')   

 
class FabricantesL(PermissionRequiredMixin, ListView):
    permission_required='productos.view_fabricante'
    model = Fabricante
    template_name = 'productos/fabricantes.html'
    context_object_name = 'fabricantes'
    queryset = Fabricante.objects.all().order_by('nombre')

@permission_required('change_fabricante')
def fabricante_editar(request,id_fabr):
    try:
        fabricante =Fabricante.objects.get(pk=id_fabr)
    except Fabricante.DoesNotExist:
        return render(request, '404_admin.html')

    if (request.method == 'POST'):
        form_EditFabr = EditarFabricanteForm(request.POST, instance=fabricante)
        if form_EditFabr.is_valid():
            form_EditFabr.save()
            return redirect('fabricantes')
    else:
        form_EditFabr = EditarFabricanteForm(instance=fabricante)
    return render(request, 'productos/fabricante_editar.html', {'formEditarFabr': form_EditFabr})    

@permission_required('add_fabricante')
def fabricante_nuevo(request):
    if request.method =='POST':
        form_nuevo_fab=NuevoFabricanteForm(request.POST)
        if form_nuevo_fab.is_valid():
            messages.success(request, 'Nuevo fabricante agregado')
            form_nuevo_fab.save()
            form_nuevo_fab = NuevoFabricanteForm()

        else:
            messages.warning(request, 'Error en los datos del formulario')
    elif request.method=='GET':
        form_nuevo_fab = NuevoFabricanteForm()

    template = loader.get_template('productos/fabricante_nuevo.html')
    context={'form_nuevo_fab':form_nuevo_fab}
    return HttpResponse(template.render(context,request))

@permission_required('delete_fabricante')
def fabricante_eliminar(request,id_fabr):
    try:
        fabricante =Fabricante.objects.get(pk=id_fabr)
    except Fabricante.DoesNotExist:
        return render(request, '404_admin.html')
    fabricante.delete()
    return redirect('fabricantes')    
    
@login_required
def stock(request):
    if request.method =='POST':
        print(request.POST)
        form_stock_enc=ModificarStockForm(request.POST,prefix='encabezado')
        Form_stock_artic_formset= modelformset_factory(ComprobanteProducto, form=ModificarStockArticulosForm)
        formsets_stock_artic=Form_stock_artic_formset(request.POST or None)

        if form_stock_enc.is_valid() and formsets_stock_artic.is_valid() :
            comprobante=Comprobante()
            comprobante.tipo=form_stock_enc.cleaned_data['tipo']
            comprobante.fecha=form_stock_enc.cleaned_data['fecha']
            comprobante.numero=form_stock_enc.cleaned_data['numero']
            
            listaProductos=[]
            for form in formsets_stock_artic:
                tupla=(form.cleaned_data['articulo'],form.cleaned_data['cantidad'])
                listaProductos.append(tupla)
                
            if comprobante.comprobarStock(listaProductos):
                comprobante.save()
                for form in formsets_stock_artic:
                    comprobante.articulos.add(form.cleaned_data['articulo'],through_defaults={'cantidad': form.cleaned_data['cantidad']})
                messages.success(request, 'Modificacion de stock exitosa')
                form_stock_enc =ModificarStockForm(prefix='encabezado')
                formsets_stock_artic=formset_factory(ModificarStockArticulosForm,extra=1)  
            else:
                messages.warning(request, 'No hay suficiente stock para realizar el egreso de mercadería solicitado')
        else:
            messages.warning(request, 'Error en los datos del formulario')
    elif request.method=='GET':
        form_stock_enc =ModificarStockForm(prefix='encabezado')
        formsets_stock_artic=formset_factory(ModificarStockArticulosForm,extra=1)

    template = loader.get_template('productos/modificar_stock.html')
    context={'ModificarStockForm':form_stock_enc,'form':formsets_stock_artic}
    return HttpResponse(template.render(context,request))


class VerComprobantes(PermissionRequiredMixin, ListView):
    permission_required='productos.view_comprobante'
    model = Comprobante
    template_name = 'productos/comprobantes.html'
    context_object_name = 'comprobantes'
    queryset = Comprobante.objects.all().order_by('-fecha')

@login_required
def comprobante_detalle(request,id_compr):
    template = loader.get_template('productos/comprobante_detalle.html')   
    lista_Prod=ComprobanteProducto.objects.filter(comprobante_id=id_compr)
    comprobante=Comprobante.objects.get(pk=id_compr)
    context={'detalle_productos':lista_Prod,'comprobante':comprobante}
    return HttpResponse(template.render(context,request))


class SalirLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return redirect('bienvenida')    
