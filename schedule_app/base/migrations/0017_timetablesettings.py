# Generated by Django 4.2.6 on 2024-02-20 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_availability_availability_end_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimetableSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people', models.IntegerField(default=1)),
                ('start_time', models.TimeField()),
                ('end_date', models.TimeField()),
                ('work_days', models.JSONField(default=list)),
                ('justice', models.BooleanField(default=True)),
                ('min_length', models.IntegerField(default=4)),
            ],
        ),
    ]