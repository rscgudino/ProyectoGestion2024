from django.contrib import admin
from productos.models import Fabricante,Item,Comprobante,ComprobanteProducto
# Register your models here.

class ComprobanteProductoInline(admin.TabularInline):
    model=ComprobanteProducto
    extra=1


class ComprobanteAdmin(admin.ModelAdmin):
    inlines=[
        ComprobanteProductoInline
    ]
    exclude=('articulos',)

admin.site.register(Fabricante)
admin.site.register(Item)
admin.site.register(Comprobante,ComprobanteAdmin)