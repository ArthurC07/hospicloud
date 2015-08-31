function Spital(url)
{
  this.url = url;
}

Spital.prototype.search_person = function(query, target)
{
  url = this.url;
  $.get(this.url + 'api/mobile/persona/search/?&format=json&q='+query, function(data)
  {
    $.each(data.objects, function(i, persona)
    {
      var article = $('<article />');
      var link = $('<a />');
      link.attr('href', url + 'admision/persona/' + persona.id);
      link.html('Ingresar');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      article.addClass('persona-resultado');
      target.append(article);
    })
  });
};

Spital.prototype.fiadores = function(query, target, admision)
{
  url = this.url;
  $.get(this.url + 'api/mobile/persona/search/?&format=json&q='+query, function(data)
  {
    $.each(data.objects, function(i, persona)
    {
      var article = $('<article />');
      var link = $('<a />');
      link.attr('href', url + 'admision/' + admision + '/fiadores/agregar/' + persona.id);
      link.html('Ingresar');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      article.addClass('persona-resultado');
      target.append(article);
    })
  });
};

Spital.prototype.referencias = function(query, target, admision)
{
  url = this.url;
  $.get(this.url + 'api/mobile/persona/search/?&format=json&q='+query, function(data)
  {
    $.each(data.objects, function(i, persona)
    {
      var article = $('<article />');
      var link = $('<a />');
      link.attr('href', url + 'admision/' + admision + '/referencias/agregar/' + persona.id);
      link.html('Ingresar');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      article.addClass('persona-resultado');
      target.append(article);
    })
  });
};
