function Persona(url, target)
{
    this.url = url;
    this.location = target;
}

Persona.prototype.search_person = function (query, target)
{
  url = this.url;
  var consultorio = this.consultorio;
  var destination = this.location;
  $.get(this.url + 'api/mobile/persona/search/?&format=json&q='+query, function(data)
  {
    if(data.objects.length == 0)
    {
        var resultado = $('<p />');
        resultado.html("No se encontraron resultados");
        target.append(resultado);
    }
    var resultado = $('<table />');
    resultado.addClass('table-striped');
    resultado.addClass('table');
    $.each(data.objects, function (i, persona) {
        var fila = $('<tr />');

        var columna1 = $('<td />');
        columna1.html(persona.nombre + ' ' + persona.apellido);
        fila.append(columna1);

        var link = $('<a />');
        link.attr('href', destination + 'persona/' + persona.id);
        link.addClass('btn');
        link.addClass('btn-success');
        link.html('Agregar');
        var columna2 = $('<td />');
        columna2.append(link);
        fila.append(columna2);
        resultado.append(fila);
    });
    target.append(resultado);
  });
};
