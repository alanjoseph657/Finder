# Generated by Django 4.2 on 2023-08-30 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobsverifiedDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RecruiterID', models.CharField(blank=True, max_length=50, null=True)),
                ('JobID', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]