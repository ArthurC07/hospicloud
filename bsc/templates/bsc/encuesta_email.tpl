{% extends "mail_templated/base.tpl" %}

{% block subject %}
    Informacion EPS Medical
{% endblock %}

{% block body %}
    Tegucigalpa M.D.C. {{ fecha }}

    Estimado (a) {{ persona.nombre }}

    Por este medio EPS Medical le informa que se ha respondido una encuesta de uno de sus pacientes en seguimiento

    Atentamente,
    EPS Medical
{% endblock %}

{% block html %}
    <p>Tegucigalpa M.D.C. {{ fecha }}</p>
    <p>
        Estimado (a) {{ persona.nombre }}<br>
    </p>
    <p>
        Por este medio EPS Medical le informa que se ha respondido una encuesta de uno de sus pacientes en seguimiento
    </p>
    <p>
        Atentamente,<br>
        EPS Medical
    </p>
{% endblock %}