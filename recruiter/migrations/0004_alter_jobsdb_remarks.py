# Generated by Django 4.2 on 2023-09-07 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0003_jobapplydb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobsdb',
            name='Remarks',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
