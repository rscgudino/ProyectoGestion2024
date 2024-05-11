function agregarProducto() {
    
    var total_forms = document.querySelector('#id_form-TOTAL_FORMS');

    var articulo = document.getElementsByClassName('articulo0')[0].cloneNode(true);

    articulo.getElementsByTagName('select')[0].name = 'form-' + total_forms.value + '-articulo';
    articulo.getElementsByTagName('select')[0].id = 'id_form-' + total_forms.value + '-articulo';

    articulo.getElementsByTagName('input')[0].name = 'form-' + total_forms.value + '-cantidad';
    articulo.getElementsByTagName('input')[0].id = 'id_form-' + total_forms.value + '-cantidad';
    articulo.getElementsByTagName('input')[0].value="";
    
    for(var i=0;i < articulo.getElementsByTagName('ul').length;i++) {
        articulo.getElementsByTagName('ul')[i].remove();
    };

    for(var i=0;i < articulo.getElementsByTagName('ul').length;i++) {
        articulo.getElementsByTagName('ul')[i].remove();
    };

    document.getElementsByClassName('row')[2].appendChild(articulo);

    total_forms.value = parseInt(total_forms.value) + 1;

    var btnEliminar = document.getElementsByClassName('eliminarProd')[0].classList.remove('invisible');
};


function eliminarUltimoProducto() {

    var total_forms = document.querySelector('#id_form-TOTAL_FORMS');

    if (total_forms.value > 1) {
        var articulo = document.getElementsByClassName('row')[2].lastElementChild;
        articulo.remove();
        total_forms.value = parseInt(total_forms.value) - 1;
        if (total_forms.value == 1) {
            var btnEliminar = document.getElementsByClassName('eliminarProd')[0].classList.add('invisible');
        };
    };
};