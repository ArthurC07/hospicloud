function Imaging(url)
{
  this.url = url;
}

Imaging.prototype.search_person = function (query, target)
{
  url = this.url;
  consultorio = this.consultorio
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
      link.attr('href', url + '/persona/' + persona.id);
      link.addClass('button');
      link.html('Mostrar Paciente');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      article.addClass('persona-resultado');
      target.append(article);
    })
  });
}
