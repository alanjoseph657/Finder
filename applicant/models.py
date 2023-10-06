from django.db import models

# Create your models here.
class clientDB(models.Model):
    ClientID = models.AutoField(primary_key= True)
    Email = models.EmailField(max_length=50,null=True,blank=True)
    password = models.CharField(max_length=20,null=True,blank=True)

class applicantDB(models.Model):
    ApplicantID = models.CharField(primary_key=True,max_length=20)
    Image = models.ImageField(upload_to="Applicant_Photo", null=True,blank=True)
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
    Status = models.CharField(max_length=10,default="Pending")
    Remarks = models.CharField(max_length=200,blank=True,null=True)
    Resume = models.FileField(upload_to='resume/',blank=True,null=True)

class jobsaveDB(models.Model):
    ApplicantID = models.ForeignKey(applicantDB,on_delete=models.CASCADE)
    JobID = models.CharField(max_length=20,blank=True,null=True)