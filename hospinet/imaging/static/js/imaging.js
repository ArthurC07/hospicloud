function Laboratory(url)
{
  this.url = url;
}

Laboratory.prototype.search_person = function(query, target)
{
  url = this.url;
  $.get(this.url + 'api/mobile/persona/search/?&format=json&q='+query, function(data)
  {
    $.each(data.objects, function(i, persona)
    {
      var article = $('<article />');
      var link = $('<a />');
      link.attr('href', url + 'imaging/' + persona.id + '/agregar');
      link.html('Ingresar');
      article.append('<h1>' + persona.nombre + ' ' + persona.apellido + '</h1>');
      article.append(link);
      article.addClass('persona-resultado');
      target.append(article);
    })
  });
}
