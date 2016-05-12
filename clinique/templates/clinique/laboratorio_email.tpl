{% extends "mail_templated/base.tpl" %}

{% block subject %}
    Hospinet - Examenes de Laboratorio
{% endblock %}

{% block body %}
    Nombre del Paciente: {{ persona.nombre_completo }}
    Edad: {{ persona.obtener_edad }}
    Doctor: {{ doctor }}
    Fecha: {{ fecha }}
    Examenes:
    {% for examen in examenes %}
        {{ examen.item.descripcion }}
    {% endfor %}
{% endblock %}
