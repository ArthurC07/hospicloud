function Consultorio(url, consultorio)
{
  this.url = url;
  this.consultorio = consultorio;
}

Consultorio.prototype.search_person = function(query, target)
{
  url = this.url;
  consultorio = this.consultorio
  $.get(this.url + 'api/mobile/persona/search/?&format=json&q='+query, function(data)
  {
    $.each(data.objects, function(i, persona)
    {
      var article = $('<article />');
      var link = $('<a />');
      link.attr('href', url + 'consultorio/' + consultorio + '/paciente/' + persona.id + '/agregar');
      link.addClass('button');
      link.html('Agregar Paciente');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      article.addClass('persona-resultado');
      target.append(article);
    })
  });
}
