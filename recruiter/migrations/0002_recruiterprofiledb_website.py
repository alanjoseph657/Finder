# Generated by Django 4.2 on 2023-08-31 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiterprofiledb',
            name='Website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
