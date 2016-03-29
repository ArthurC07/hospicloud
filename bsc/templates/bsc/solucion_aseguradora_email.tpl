{% extends "mail_templated/base.tpl" %}
{% load i10n %}{% load l10n %}

{% block subject %}
    {% trans 'Formato de Oportunidades de Mejora EPS Medical' %}
{% endblock %}

{% block body %}
    {% trans 'Formato de Oportunidades de Mejora EPS Medical' %}
    {{ aseguradora }}
    {% trans 'Número de Póliza' %}    {{ consulta.poliza.poliza }}
    {% trans 'Número de Certificado' %}    {{ consulta.contrato.certificado }}
    {% trans 'Nombre del Paciente:' %}    {{ consulta.persona }}
    {% trans 'Edad del Paciente' %}    {{ consulta.persona.obtener_edad }}
    {% trans 'Fecha de Atención' %}    {{ consulta.created.date }}
    {% trans 'Hora de Atención Preclínica:' %}
    {{ consulta.espera.created.time }}
    {% trans 'Hora de Atención en Clínica' %}    {{ consulta.created }}
    {% trans 'Tiempo Total de Atención:' %}    {{ consulta.total_time }}
    {% trans 'Diagnostico Clinico según expediente:' %}
    {% for diagnostico in consulta.diagnosticos_clinicos.all %}
        {{ diagnostico.afeccion.nombre }} {{ diagnostico.diagnostico }}
    {% endfor %}
    {% trans 'Diagnostico Enlistado en Emergencias' %}    {% trans 'No' %}
    {% trans 'Tratamiento Médico y Exámenes Indicado' %}
    {% for orden in consulta.ordenes_medicas.all %} {{ orden.orden }}
        {% for prescripcion in ordenes %} {% endfor %} {% endfor %}
    {% trans 'Días de Incapacidad Otorgados:' %}
    {{ consulta.total_incapacidad }}
    {% trans 'Queja Presentada' %}    {{ solucion.queja }}
    {% trans 'Comentario del Personal de EPS' %}    {{ solucion.solucion }}
{% endblock %}

{% block html %}
    <h1>{% trans 'Formato de Oportunidades de Mejora EPS Medical' %}</h1>
    <h2>{{ aseguradora }}</h2>
    <table>
        <tr>
            <td>{% trans 'N&uacute;mero de P&oacute;liza' %}</td>
            <td>{{ consulta.poliza.poliza }}</td>
        </tr>
        <tr>
            <td>{% trans 'Número de Certificado' %}</td>
            <td>{{ consulta.contrato.certificado }}</td>
        </tr>
        <tr>
            <td>{% trans 'Nombre del Paciente:' %}</td>
            <td>{{ consulta.persona }}</td>
        </tr>
        <tr>
            <td>{% trans 'Edad del Paciente' %}</td>
            <td>{{ consulta.persona.obtener_edad }}</td>
        </tr>
        <tr>
            <td>{% trans 'Fecha de Atención' %}</td>
            <td>{{ consulta.created.date }}</td>
        </tr>
        <tr>
            <td>{% trans 'Hora de Atención Preclínica:' %}</td>
            <td>{{ consulta.espera.created.time }}</td>
        </tr>
        <tr>
            <td>{% trans 'Hora de Atenci&oacute;n en Clínica' %}</td>
            <td>{{ consulta.created }}</td>
        </tr>
        <tr>
            <td>{% trans 'Tiempo Total de Atención:' %}</td>
            <!-- TODO: Implement this -->
            <td>{{ consulta.total_time }}</td>
        </tr>
        <tr>
            <td>{% trans 'Diagnostico Clinico según expediente:' %}</td>
            <td>
                {% for diagnostico in consulta.diagnosticos_clinicos.all %}
                    {{ diagnostico.afeccion.nombre }} {{ diagnostico.diagnostico }}<br>
                {% endfor %}
            </td>
        </tr>
        <tr>
            <td>{% trans 'Diagnostico Enlistado en Emergencias' %}</td>
            <!-- TODO: Track this -->
            <td>{% trans 'No' %}</td>
        </tr>
        <tr>
            <!-- TODO: Track this separately -->
            <td>{% trans 'Tratamiento Médico y Exámenes Indicado' %}</td>
            <td>
                {% for orden in consulta.ordenes_medicas.all %}
                    {{ orden.orden }}
                    {% for prescripcion in ordenes %}
                        {% endfor %}
                {% endfor %}
            </td>
        </tr>
        <tr>
            <td>{% trans 'Días de Incapacidad Otorgados:' %}</td>
            <td>{{ consulta.total_incapacidad }}</td>
        </tr>
        <tr>
            <td>{% trans 'Queja Presentada' %}</td>
            <td>{{ solucion.queja }}</td>
        </tr>
        <tr>
            <td>{% trans 'Comentario del Personal de EPS' %}</td>
            <td>{{ solucion.solucion }}</td>
        </tr>
    </table>
{% endblock %}