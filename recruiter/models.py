from django.db import models

# Create your models here.
class recruiterDB(models.Model):
    RecruiterID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Logo = models.ImageField(upload_to="recruiterlogos")


class recruiterprofileDB(models.Model):
    RecruiterID = models.ForeignKey(recruiterDB,on_delete=models.CASCADE)
    Logo = models.ImageField(upload_to="recruiterdocuments",null=True,blank=True)
    Name = models.CharField(max_length=100,blank=True,null=True)
    Email = models.EmailField(max_length=100,blank=True,null=True)
    Description = models.CharField(max_length=500,null=True,blank=True)
    Location = models.CharField(max_length=100,null=True,blank=True)
    Contact = models.CharField(max_length=100,null=True,blank=True)
    Website = models.CharField(max_length=100,null=True,blank=True)
    Doc1 = models.ImageField(upload_to="recruiterdocuments",null=True,blank=True)
    Doc2 = models.ImageField(upload_to="recruiterdocuments",null=True,blank=True)
    Doc3 = models.ImageField(upload_to="recruiterdocuments",null=True,blank=True)
    Remarks = models.CharField(max_length=100,null=True,blank=True)
    Status = models.CharField(max_length=20,default="Pending")

class jobsDB(models.Model):
    RecruiterID = models.CharField(max_length=20,null=True,blank=True)
    Company_Name = models.CharField(max_length=50,null=True)
    Logo = models.ImageField(upload_to="jobimages",null=True)
    JobID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50,null=True,blank=True)
    Location = models.CharField(max_length=50)
    Type = models.CharField(max_length=20)
    Published = models.DateField()
    Deadline = models.DateField(blank=True,null=True)
    Experience = models.CharField(max_length=100, default="Any")
    Gender = models.CharField(max_length=20,default="Any")
    Salary = models.CharField(max_length=50)
    Qualification = models.CharField(max_length=100)
    Description = models.CharField(max_length=1000,null=True,blank=True)
    Remarks = models.CharField(max_length=50, blank=True,null=True)
    Status = models.CharField(max_length=20,default="Pending")

class responsibilities(models.Model):
    JobID = models.ForeignKey(jobsDB,on_delete=models.CASCADE)
    res1 = models.CharField(max_length=100,null=True,blank=True)
    res2 = models.CharField(max_length=100,null=True,blank=True)
    res3 = models.CharField(max_length=100,null=True,blank=True)
    res4 = models.CharField(max_length=100,null=True,blank=True)
    res5 = models.CharField(max_length=100,null=True,blank=True)
    res6 = models.CharField(max_length=100,null=True,blank=True)
    res7 = models.CharField(max_length=100,null=True,blank=True)
    res8 = models.CharField(max_length=100,null=True,blank=True)
    res9 = models.CharField(max_length=100,null=True,blank=True)
    res10 = models.CharField(max_length=100,null=True,blank=True)

class benefits(models.Model):
    JobID = models.ForeignKey(jobsDB,on_delete=models.CASCADE)
    ben1 = models.CharField(max_length=100,null=True,blank=True)
    ben2 = models.CharField(max_length=100,null=True,blank=True)
    ben3 = models.CharField(max_length=100,null=True,blank=True)
    ben4 = models.CharField(max_length=100,null=True,blank=True)
    ben5 = models.CharField(max_length=100,null=True,blank=True)


class otherrequirements(models.Model):
    JobID = models.ForeignKey(jobsDB,on_delete=models.CASCADE)
    req1 = models.CharField(max_length=100,null=True,blank=True)
    req2 = models.CharField(max_length=100,null=True,blank=True)
    req3 = models.CharField(max_length=100,null=True,blank=True)
    req4 = models.CharField(max_length=100,null=True,blank=True)
    req5 = models.CharField(max_length=100,null=True,blank=True)

class jobapplyDB(models.Model):
    JobID = models.ForeignKey(jobsDB,on_delete=models.CASCADE)
    Title = models.CharField(max_length=50)
    ApplicantID = models.CharField(max_length=20)

class profilebookmarkDB(models.Model):
    RecruiterID = models.ForeignKey(recruiterDB,on_delete=models.CASCADE)
    ApplicantID = models.CharField(max_length=20)