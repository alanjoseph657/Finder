# Generated by Django 4.2 on 2023-09-01 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0002_remove_applicantdb_id_alter_applicantdb_applicantid'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobsaveDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('JobID', models.CharField(blank=True, max_length=20, null=True)),
                ('ApplicantID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.applicantdb')),
            ],
        ),
    ]