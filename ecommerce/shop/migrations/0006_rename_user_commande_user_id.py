# Generated by Django 4.2 on 2023-04-24 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_commande_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commande',
            old_name='user',
            new_name='user_id',
        ),
    ]