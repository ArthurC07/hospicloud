$.validator.addMethod('identificacion', function(value, element, param) {
    alert("validando");
    switch($('#id_tipo_identificacion').val()){
        case 'T':
            var regex = new RegExp("(d{13})");
            return regex.test(value);
        case 'L':
            var regex = new RegExp("(d{13})");
            return regex.test(value);
        case 'P':
            var regex = new RegExp("([A-Z]|[a-z]|[0-9])\\w+");
            return regex.test(value);
        case 'N':
            return this.optional(element);
    }
});
$("#persona_form").validate({rules : {id_identificacion: {identificacion:true}}});
