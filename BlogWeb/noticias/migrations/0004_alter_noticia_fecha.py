# Generated by Django 4.1.4 on 2022-12-20 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noticias', '0003_alter_noticia_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
