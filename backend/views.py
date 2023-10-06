from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from applicant.models import applicantDB
from recruiter.models import jobsDB,recruiterDB,responsibilities,otherrequirements,benefits,recruiterprofileDB
from backend.models import applicantverifiedDB,contactDB,contactresponseDB,recruiterverifiedDB,jobsverifiedDB
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import FileResponse



# Create your views here.
def adminhome(request):
    data = applicantDB.objects.all().order_by('-ApplicantID')[:5]
    jobs = jobsDB.objects.all().order_by('-JobID')[:5]
    appcount = applicantDB.objects.count()
    appvcount = applicantverifiedDB.objects.count()
    mcount = contactDB.objects.count()
    rcount = recruiterverifiedDB.objects.count()
    jcount = jobsverifiedDB.objects.count()
    return render(request,"adminhome.html",{'data':data,'appcount':appcount,'mcount':mcount,'jobs':jobs,
                                            'appvcount':appvcount,'rcount':rcount,
                                            'jcount':jcount})

def adminlogin(request):
    return render(request,"adminlogin.html")

def logauth(request):
    if request.method=="POST":
        un = request.POST.get("username")
        pw = request.POST.get("password")

        if User.objects.filter(username__contains=un).exists():
            user = authenticate(username = un, password = pw)
            if user is not None:
                login(request,user)
                request.session["username"] = un
                request.session["password"] = pw
                messages.success(request, "Logged in")
                return redirect(adminhome)
            else:
                messages.error(request, "Wrong Username or Password")
                return redirect(adminlogin)
        else:
            messages.error(request, "Wrong Username or Password")
            return redirect(adminlogin)

def adminlogout(request):
    del request.session["username"]
    del request.session["password"]
    messages.success(request, "Logged Out")
    return redirect(adminlogin)

def applicantverify(request):
    data = applicantDB.objects.filter(Status="Pending")
    mcount = contactDB.objects.count()
    return render(request,"appllicantverify.html",{'data':data,'mcount':mcount})

def applicantsingle(request,id):
    data = applicantDB.objects.get(ApplicantID=id)
    mcount = contactDB.objects.count()
    return render(request,"applicantsingle.html",{'data':data,'mcount':mcount})

def applicantverified(request,id):
    d = applicantDB.objects.get(ApplicantID=id)
    if applicantverifiedDB.objects.filter(ApplicantID=id).exists():
        try:
            img = d.Image
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = applicantverifiedDB.objects.get(ApplicantID=id).Image
        try:
                doc = d.Resume
                fs = FileSystemStorage()
                res = fs.save(doc.name,doc)
        except MultiValueDictKeyError:
                res = applicantDB.objects.get(ApplicantID=id).Resume
        applicantverifiedDB.objects.filter(ApplicantID=id).update(Image=file, Salutation=d.Salutation, Name=d.Name, Email=d.Email, Mobile=d.Mobile,
                                                            Location=d.Location, Qualification=d.Qualification, Field=d.Field, University=d.University,
                                                            Duration=d.Duration, CGPA=d.CGPA, Company=d.Company, Designation=d.Designation,
                                                            Experience=d.Experience, Skills=d.Skills, Linkedin=d.Linkedin,Resume=res)
    else:
        img = d.Image
        if d.Resume is not None:
            res = d.Resume
        else:
            res=None
        obj = applicantverifiedDB(ApplicantID=id, Image=img, Salutation=d.Salutation, Name=d.Name, Email=d.Email, Mobile=d.Mobile,
                                                            Location=d.Location, Qualification=d.Qualification, Field=d.Field, University=d.University,
                                                            Duration=d.Duration, CGPA=d.CGPA, Company=d.Company, Designation=d.Designation,
                                                            Experience=d.Experience, Skills=d.Skills, Linkedin=d.Linkedin,Resume=res)
        obj.save()
    applicantDB.objects.filter(ApplicantID=id).update(Remarks=None,Status="Verified")
    messages.success(request, "Verified")
    return redirect(applicantverify)

def unverify(request,id):
    if request.method=="POST":
        rem = request.POST.get("remarks")
        applicantDB.objects.filter(ApplicantID=id).update(Remarks=rem)
        messages.success(request, "Remark Posted")
        return redirect(applicantverify)

def applicantslist(request):
    data = applicantDB.objects.all()
    mcount = contactDB.objects.count()
    return render(request,"applicantslist.html",{'data':data,'mcount':mcount})

def applicantslistsingle(request,dataid):
    data = applicantDB.objects.get(ApplicantID=dataid)
    mcount = contactDB.objects.count()
    return render(request,"applicantslistsingle.html",{'data':data,'mcount':mcount})

def applicantdelete(request,aid):
    data = applicantDB.objects.filter(ApplicantID=aid)
    vdata = applicantverifiedDB.objects.filter(ApplicantID=aid)
    data.delete()
    vdata.delete()
    messages.warning(request,"Data deleted")
    return redirect(applicantslist)

def contactmessages(request):
    data = contactDB.objects.all()
    mcount = contactDB.objects.count()
    return render(request,"contactmessages.html",{'data':data,'mcount':mcount})

def contactsingle(request,dataid):
    data = contactDB.objects.get(id=dataid)
    mcount = contactDB.objects.count()
    return render(request,"contactsingle.html",{'data':data,'mcount':mcount})

def contactresponse(request,dataid):
    if request.method=="POST":
        cdata = contactDB.objects.filter(id=dataid)
        c = cdata.get()
        img = request.FILES["image"]
        rem = request.POST.get("note")
        obj = contactresponseDB(Name=c.Name, Email=c.Email , Subject=c.Subject, Message=c.Message,Image=img, Remarks=rem, Admin_Name=request.session["username"])
        obj.save()
        cdata.delete()
        return redirect(contactmessages)

def responselist(request):
    data = contactresponseDB.objects.all()
    return render(request,"contactresponse.html",{'data':data})

def responsesingle(request,dataid):
    data = contactresponseDB.objects.get(id=dataid)
    return render(request,"responsesingle.html",{'data':data})

def jobverifylist(request):
    rd = jobsDB.objects.filter(Status="Pending")
    mcount = contactDB.objects.count()
    return render(request,"jobverify.html",{'rd':rd,'mcount':mcount})

def jobverifysingle(request,id):
    data = jobsDB.objects.get(JobID=id)
    resdata = responsibilities.objects.get(JobID=id)
    reqdata = otherrequirements.objects.get(JobID=id)
    bendata = benefits.objects.get(JobID=id)
    mcount = contactDB.objects.count()
    return render(request,"jobverifysingle.html",{'data':data,'resdata':resdata,
                                                  'reqdata':reqdata,'bendata':bendata,'mcount':mcount})

def jobverified(request,jid):
    recdata = jobsDB.objects.get(JobID=jid).RecruiterID
    jobsDB.objects.filter(JobID=jid).update(Status="Verified",Remarks=None)
    if jobsverifiedDB.objects.filter(JobID=jid).exists():
        jobsverifiedDB.objects.filter(JobID=jid).update(RecruiterID=recdata,JobID=jid)
    else:
        obj = jobsverifiedDB(RecruiterID=recdata,JobID=jid)
        obj.save()
    messages.success(request, "Verified")
    return redirect(jobverifylist)

def jobunverify(request,jid):
    if request.method=="POST":
        rem = request.POST.get("remarks")
        jobsDB.objects.filter(jobID=jid).update(Remarks=rem)
        messages.success(request, "Remark Posted")
        return redirect(jobverifylist)

def jobslist(request):
    data = jobsDB.objects.all().order_by('Deadline')
    mcount = contactDB.objects.count()
    return render(request,"jobslist.html",{'data':data,'mcount':mcount})

def jobslistsingle(request,jid):
    data = jobsDB.objects.get(JobID=jid)
    mcount = contactDB.objects.count()
    resdata = responsibilities.objects.get(JobID=jid)
    reqdata = otherrequirements.objects.get(JobID=jid)
    bendata = benefits.objects.get(JobID=jid)
    return render(request,"jobslistsingle.html",{'data':data,'mcount':mcount,'resdata':resdata,
                                                  'reqdata':reqdata,'bendata':bendata})

def jobdelete(request,jid):
    jdata = jobsDB.objects.filter(JobID=jid)
    vjobdata = jobsverifiedDB.objects.filter(JobID=jid)
    jdata.delete()
    vjobdata.delete()
    messages.success(request, "Job Deleted")
    return redirect(jobslist)

def recruiterverifylist(request):
    data = recruiterprofileDB.objects.filter(Status="Pending")
    mcount = contactDB.objects.count()
    return render(request,"recruiterverify.html",{'data':data,'mcount':mcount})

def recruiterverifysingle(request,rid):
    data = recruiterprofileDB.objects.get(RecruiterID_id=rid)
    mcount = contactDB.objects.count()
    return render(request,"recruiterverifysingle.html",{'data':data,'mcount':mcount})

def recruiterverify(request,rid):
    rdata = recruiterDB.objects.get(RecruiterID=rid)
    rpdata = recruiterprofileDB.objects.get(RecruiterID=rid)
    recruiterprofileDB.objects.filter(RecruiterID=rid).update(Status="Verified",Remarks=None)
    if recruiterverifiedDB.objects.filter(RecruiterID=rid).exists():
        recruiterverifiedDB.objects.filter(RecruiterID=rid).update(RecruiterID=rdata,Name=rpdata.Name)

    else:
        obj = recruiterverifiedDB(RecruiterID=rdata,Name=rpdata.Name)
        obj.save()
    messages.success(request, "Verified")
    return redirect(recruiterverifylist)

def recruiterunverify(request,rid):
    if request.method=="POST":
        rem = request.POST.get("remarks")
        rdata = recruiterprofileDB.objects.filter(RecruiterID=rid).update(Remarks=rem)
        messages.success(request,"Remark Posted")
        return redirect(recruiterverifylist)

def recruiterslist(request):
    data = recruiterprofileDB.objects.all()
    mcount = contactDB.objects.count()
    return render(request,"recruiterslist.html",{'data':data,'mcount':mcount})

def recruiterslistsingle(request,rid):
    data = recruiterprofileDB.objects.get(RecruiterID_id=rid)
    mcount = contactDB.objects.count()
    return render(request,"recruiterslistsingle.html",{'data':data,'mcount':mcount})

def recruitersprofiledelete(request,rid):
    data = recruiterprofileDB.objects.filter(RecruiterID_id=rid)
    vrdata = recruiterverifiedDB.objects.filter(RecruiterID_id=rid)
    data.delete()
    vrdata.delete()
    messages.warning(request,"Data Deleted")
    return redirect(recruiterslist)

def viewresume(request,aid):
    data = applicantDB.objects.get(ApplicantID=aid).Resume
    pdf_file = get_object_or_404(applicantDB,ApplicantID=aid)
    response = FileResponse(pdf_file.Resume,as_attachment=True)
    return response
