# Generated by Django 3.2.5 on 2021-08-11 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
