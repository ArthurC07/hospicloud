{% extends "mail_templated/base.tpl" %}

{% block subject %}
    Atención al Cliente {{ company.nombre_comercial }}
{% endblock %}

{% block body %}
    Tegucigalpa M.D.C. {{ fecha }}

    Señor (a)
    {{ persona.nombre_completo }}
    Presente

    Estimado (a) {{ persona.nombre }}

    Por este medio {{ company.nombre_comercial }} le agradece por compartir con nosotros su
    sugerencia, por lo que queremos hacer de su conocimiento que hemos
    tomado acciones en base a sus comentarios ya que estamos en la mejora
    continua para darle el servicio que usted se merece, nuestra idea es
    tener relaciones duraderas con nuestros afiliados y por consiguiente
    solo se crean tomando acciones que permitan la satisfacción completa.

    A su vez queremos solicitarle las disculpas correspondientes por
    cualquier inconveniente que se le haya ocasionado en nuestras
    instalaciones basadas en la experiencia de Servicio recibido.
    ¡Nos despedimos con el compromiso de cuidar lo mejor de Honduras, su
    gente!

    Atentamente,
    {{ company.nombre_comercial }}
{% endblock %}

{% block html %}
    <p>Tegucigalpa M.D.C. {{ fecha }}</p>
    <p>
        Señor (a)<br>
        {{ persona.nombre_completo }} <br>
        Presente<br>
        Estimado (a) {{ persona.nombre }}<br>
    </p>
    <p>
        Por este medio {{ company.nombre_comercial }} le agradece por compartir con nosotros su
        sugerencia, por lo que queremos hacer de su conocimiento que hemos
        tomado acciones en base a sus comentarios ya que estamos en la mejora
        continua para darle el servicio que usted se merece, nuestra idea es
        tener relaciones duraderas con nuestros afiliados y por consiguiente
        solo se crean tomando acciones que permitan la satisfacción completa.
    </p>
    <p>
        A su vez queremos solicitarle las disculpas correspondientes por
        cualquier inconveniente que se le haya ocasionado en nuestras
        instalaciones basadas en la experiencia de Servicio recibido.
    </p>
    <p>
        ¡Nos despedimos con el compromiso de cuidar lo mejor de Honduras, su
        gente!
    <p>
    <p>
        Atentamente,<br>
        {{ company.nombre_comercial }}
    </p>
{% endblock %}
