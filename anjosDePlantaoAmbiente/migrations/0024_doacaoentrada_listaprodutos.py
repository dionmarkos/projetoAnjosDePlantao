# Generated by Django 2.0.13 on 2019-08-28 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anjosDePlantaoAmbiente', '0023_auto_20190828_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='doacaoentrada',
            name='listaProdutos',
            field=models.ManyToManyField(to='anjosDePlantaoAmbiente.ProdutoDoado'),
        ),
    ]
