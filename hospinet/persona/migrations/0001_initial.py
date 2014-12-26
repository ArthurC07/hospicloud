# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone
import persona.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('nombre', models.CharField(max_length=200, blank=True)),
                ('direccion', models.TextField()),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Empleo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('numero_empleado', models.CharField(max_length=200, null=True, blank=True)),
                ('empleador', models.ForeignKey(related_name='empleos', blank=True, to='persona.Empleador', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_identificacion', models.CharField(blank=True, max_length=1, choices=[(b'T', 'Tarjeta de Identidad'), (b'P', 'Pasaporte'), (b'L', 'Licencia'), (b'N', 'Ninguno')])),
                ('identificacion', models.CharField(max_length=20, blank=True)),
                ('nombre', models.CharField(max_length=50, blank=True)),
                ('apellido', models.CharField(max_length=50, blank=True)),
                ('sexo', models.CharField(blank=True, max_length=1, choices=[(b'M', 'Masculino'), (b'F', 'Femenino')])),
                ('nacimiento', models.DateField(default=datetime.date.today)),
                ('estado_civil', models.CharField(blank=True, max_length=1, choices=[(b'S', 'Soltero/a'), (b'D', 'Divorciado/a'), (b'C', 'Casado/a'), (b'U', 'Union Libre')])),
                ('profesion', models.CharField(max_length=200, blank=True)),
                ('telefono', models.CharField(max_length=200, blank=True)),
                ('celular', models.CharField(max_length=200, blank=True)),
                ('domicilio', models.CharField(max_length=200, blank=True)),
                ('email', models.CharField(max_length=200, blank=True)),
                ('fax', models.CharField(max_length=200, blank=True)),
                ('fotografia', models.ImageField(null=True, upload_to=b'persona/foto//%Y/%m/%d', blank=True)),
                ('nacionalidad', persona.fields.OrderedCountryField(blank=True, max_length=2, choices=[('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo (the Democratic Republic of the)'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Cura\xe7ao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('CI', "C\xf4te d'Ivoire"), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands  [Malvinas]'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia (The)'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See  [Vatican City State]'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran (the Islamic Republic of)'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea (the Democratic People's Republic of)"), ('KR', 'Korea (the Republic of)'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia (the former Yugoslav Republic of)'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia (the Federated States of)'), ('MD', 'Moldova (the Republic of)'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('RE', 'R\xe9union'), ('BL', 'Saint Barth\xe9lemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan (Province of China)'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands (British)'), ('VI', 'Virgin Islands (U.S.)'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'), ('AX', '\xc5land Islands')])),
                ('duplicado', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('persona', 'Permite al usuario gestionar persona'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fisico',
            fields=[
                ('persona', models.OneToOneField(primary_key=True, serialize=False, to='persona.Persona')),
                ('peso', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('lateralidad', models.CharField(blank=True, max_length=1, choices=[(b'D', 'Derecha'), (b'I', 'Izquierda')])),
                ('altura', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('color_de_ojos', models.CharField(max_length=200, blank=True)),
                ('color_de_cabello', models.CharField(max_length=200, blank=True)),
                ('factor_rh', models.CharField(blank=True, max_length=1, choices=[(b'+', '+'), (b'-', '-')])),
                ('tipo_de_sangre', models.CharField(blank=True, max_length=2, choices=[(b'A', 'A'), (b'B', 'B'), (b'AB', 'AB'), (b'O', 'O')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstiloVida',
            fields=[
                ('persona', models.OneToOneField(related_name='estilo_vida', primary_key=True, serialize=False, to='persona.Persona')),
                ('consume_tabaco', models.BooleanField(default=False)),
                ('inicio_consumo_tabaco', models.CharField(max_length=30, blank=True)),
                ('tipo_de_tabaco', models.CharField(max_length=30, blank=True)),
                ('consumo_diario_tabaco', models.IntegerField(null=True)),
                ('vino', models.BooleanField(default=False)),
                ('cerveza', models.BooleanField(default=False)),
                ('licor', models.BooleanField(default=False)),
                ('cafe', models.BooleanField(default=False)),
                ('cantidad_cafe', models.CharField(max_length=200, blank=True)),
                ('dieta', models.CharField(max_length=200, blank=True)),
                ('cantidad', models.CharField(max_length=200, blank=True)),
                ('numero_comidas', models.IntegerField(null=True)),
                ('tipo_de_comidas', models.CharField(max_length=200, blank=True)),
                ('consume_drogas', models.BooleanField(default=False)),
                ('drogas', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AntecedenteQuirurgico',
            fields=[
                ('persona', models.ForeignKey(related_name='antecedentes_quirurgicos', primary_key=True, serialize=False, to='persona.Persona')),
                ('procedimiento', models.CharField(max_length=200, blank=True)),
                ('fecha', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AntecedenteObstetrico',
            fields=[
                ('persona', models.OneToOneField(related_name='antecedente_obstetrico', primary_key=True, serialize=False, to='persona.Persona')),
                ('menarca', models.DateField(default=datetime.date.today)),
                ('ultimo_periodo', models.DateField(null=True, blank=True)),
                ('displasia', models.BooleanField(default=False)),
                ('gestas', models.CharField(max_length=200, blank=True)),
                ('partos', models.CharField(max_length=200, blank=True)),
                ('anticoncepcion', models.CharField(max_length=200, blank=True)),
                ('cesareas', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AntecedenteFamiliar',
            fields=[
                ('persona', models.OneToOneField(related_name='antecedente_familiar', primary_key=True, serialize=False, to='persona.Persona')),
                ('sindrome_coronario_agudo', models.BooleanField(default=False)),
                ('hipertension', models.BooleanField(default=False)),
                ('tabaquismo', models.BooleanField(default=False)),
                ('epoc', models.NullBooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('tuberculosis', models.BooleanField(default=False)),
                ('asma', models.BooleanField(default=False)),
                ('colitis', models.BooleanField(default=False)),
                ('sinusitis', models.BooleanField(default=False)),
                ('colelitiasis', models.BooleanField(default=False)),
                ('migrana', models.BooleanField(default=False)),
                ('obesidad', models.BooleanField(default=False)),
                ('dislipidemias', models.BooleanField(default=False)),
                ('alcoholismo', models.BooleanField(default=False)),
                ('cancer', models.BooleanField(default=False)),
                ('alergias', models.CharField(max_length=200, null=True, blank=True)),
                ('congenital', models.CharField(max_length=200, blank=True)),
                ('general', models.CharField(max_length=200, blank=True)),
                ('nutricional', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Antecedente',
            fields=[
                ('persona', models.OneToOneField(primary_key=True, serialize=False, to='persona.Persona')),
                ('cardiopatia', models.BooleanField(default=False)),
                ('hipertension', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('hepatitis', models.BooleanField(default=False)),
                ('rinitis', models.BooleanField(default=False)),
                ('tuberculosis', models.BooleanField(default=False)),
                ('artritis', models.BooleanField(default=False)),
                ('asma', models.BooleanField(default=False)),
                ('colitis', models.BooleanField(default=False)),
                ('gastritis', models.BooleanField(default=False)),
                ('sinusitis', models.BooleanField(default=False)),
                ('hipertrigliceridemia', models.BooleanField(default=False)),
                ('colelitiasis', models.BooleanField(default=False)),
                ('migrana', models.NullBooleanField(default=False)),
                ('obesidad', models.NullBooleanField(default=False)),
                ('colesterol', models.NullBooleanField(default=False)),
                ('trigliceridos', models.NullBooleanField(default=False)),
                ('alcoholismo', models.NullBooleanField(default=False)),
                ('cancer', models.NullBooleanField(default=False)),
                ('alergias', models.CharField(max_length=200, null=True, blank=True)),
                ('congenital', models.CharField(max_length=200, blank=True)),
                ('general', models.CharField(max_length=200, blank=True)),
                ('nutricional', models.CharField(max_length=200, blank=True)),
                ('otros', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('lugar', models.CharField(max_length=200, blank=True)),
                ('direccion', models.TextField()),
                ('empleador', models.ForeignKey(related_name='sedes', blank=True, to='persona.Empleador', null=True)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='empleo',
            name='persona',
            field=models.ForeignKey(related_name='empleos', to='persona.Persona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='empleo',
            name='sede',
            field=models.ForeignKey(related_name='empleos', blank=True, to='persona.Sede', null=True),
            preserve_default=True,
        ),
    ]
