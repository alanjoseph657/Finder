# Generated by Django 4.2 on 2023-09-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0004_alter_applicantdb_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicantdb',
            name='Resume',
            field=models.FileField(blank=True, null=True, upload_to='resume'),
        ),
    ]