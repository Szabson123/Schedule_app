# Generated by Django 4.2.6 on 2024-02-21 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_alter_timetablesettings_people'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timetablesettings',
            old_name='end_date',
            new_name='end_time',
        ),
    ]
