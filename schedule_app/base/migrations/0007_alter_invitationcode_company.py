# Generated by Django 5.0.1 on 2024-01-29 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_invitationcode_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitationcode',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.company'),
        ),
    ]