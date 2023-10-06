from django.db import models
from recruiter.models import recruiterDB

# Create your models here.
class applicantverifiedDB(models.Model):
    ApplicantID = models.CharField(max_length=50,null=True,blank=True)
    Image = models.ImageField(upload_to="Applicant_Photo", null=True)
    Salutation = models.CharField(max_length=10,null=True,blank=True)
    Name = models.CharField(max_length=50,null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)
    Mobile = models.IntegerField(null=True,blank=True)
    Location = models.CharField(max_length=100,null=True,blank=True)
    Qualification = models.CharField(max_length=100,null=True,blank=True)
    Field = models.CharField(max_length=100,null=True,blank=True)
    University = models.CharField(max_length=100,null=True,blank=True)
    Duration = models.CharField(max_length=100,null=True,blank=True)
    CGPA = models.FloatField(null=True,blank=True)
    Company = models.CharField(max_length=100)
    Designation = models.CharField(max_length=100)
    Experience = models.CharField(max_length=20)
    Skills = models.CharField(max_length=50)
    Linkedin = models.CharField(max_length=50,null=True,blank=True)
    Resume = models.FileField(upload_to="Resume",blank=True,null=True)


class contactDB(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=100)
    Subject = models.CharField(max_length=50)
    Message = models.CharField(max_length=1000)


class contactresponseDB(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=100)
    Subject = models.CharField(max_length=50)
    Message = models.CharField(max_length=1000)
    Admin_Name = models.CharField(max_length=50)
    Image = models.ImageField(upload_to="Response")
    Remarks = models.CharField(max_length=1000)

class jobsverifiedDB(models.Model):
    RecruiterID = models.CharField(max_length=50,null=True,blank=True)
    JobID = models.CharField(max_length=50,null=True,blank=True)

class recruiterverifiedDB(models.Model):
    RecruiterID = models.ForeignKey(recruiterDB,on_delete=models.CASCADE)
    Name = models.CharField(max_length=100,null=True,blank=True)