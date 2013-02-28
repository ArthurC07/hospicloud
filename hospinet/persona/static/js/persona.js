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
    $.each(data.objects, function(i, persona)
    {
      var article = $('<article />');
      var link = $('<a />');
      link.attr('href', destination + 'persona/' + persona.id);
      link.addClass('button');
      link.html('Mostrar Paciente');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      article.addClass('persona-resultado');
      target.append(article);
    })
  });
}
