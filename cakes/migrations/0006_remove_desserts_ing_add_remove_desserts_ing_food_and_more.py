# Generated by Django 4.1.1 on 2022-09-26 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0005_alter_desserts_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='desserts',
            name='ing_add',
        ),
        migrations.RemoveField(
            model_name='desserts',
            name='ing_food',
        ),
        migrations.AddField(
            model_name='desserts',
            name='decor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cakes.decor', verbose_name='Декор'),
        ),
    ]
