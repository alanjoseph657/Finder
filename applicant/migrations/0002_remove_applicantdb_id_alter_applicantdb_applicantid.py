# Generated by Django 4.2 on 2023-09-01 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicantdb',
            name='id',
        ),
        migrations.AlterField(
            model_name='applicantdb',
            name='ApplicantID',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
