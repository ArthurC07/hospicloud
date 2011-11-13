function Spital(url)
{
  this.url = url;
}

Spital.prototype.search_person = function(query, target)
{
  $.get(this.url + 'api/mobile/persona/search/?&format=json&q='+query, function(data)
  {
    $.each(data.objects, function(i, persona)
    {
      var article = $('<article />');
      var link = $('<a />');
      link.attr('href', this.url + 'admision/persona/' + persona.id);
      link.html('Ingresar');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      target.append(article);
    })
  });
}
