from django.shortcuts import render,redirect
from applicant.models import clientDB,applicantDB,jobsaveDB
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from backend.models import contactDB,jobsverifiedDB,applicantverifiedDB
from recruiter.models import jobsDB,responsibilities,benefits,otherrequirements,jobapplyDB,profilebookmarkDB,recruiterprofileDB
from django.db.models import Q
from django.http import FileResponse

# Create your views here.
def applicanthomepage(request):
    jdata = jobsDB.objects.filter(Status="Verified").order_by('-JobID')[:5]
    if 'username' in request.session:
        em = request.session["username"]
        if applicantDB.objects.filter(Email=em).exists():
            appdata = applicantDB.objects.get(Email=em)
            return render(request,"applicanthome.html",{'appdata':appdata,'jdata':jdata})
        else:
            return render(request, "applicanthome.html",{'jdata':jdata})
    else :
        return render(request,"applicanthome.html",{'jdata':jdata})


def applicantloginpage(request):
    return render(request,"applicantlogin.html")

def signup(request):
    if request.method == "POST":
        em = request.POST.get("email")
        pw = request.POST.get("password")
        cp = request.POST.get("cpassword")
        if clientDB.objects.filter(Email = em).exists():
            messages.error(request,"Email ID already taken")
            return redirect(applicantloginpage)
        else:
            if pw == cp:
                obj = clientDB(Email= em,password = pw)
                obj.save()
                messages.success(request,"Sign Up Success. Log in now")
                return redirect(applicantloginpage)
            else:
                messages.error(request, "Password Does not match")
                return redirect(applicantloginpage)

def clientlogin(request):
    if request.method == "POST":
        em = request.POST.get("email")
        pw = request.POST.get("password")
        if clientDB.objects.filter(Email=em,password=pw).exists():
            request.session["username"]=em
            request.session["password"]=pw
            return redirect(applicanthomepage)
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(applicantloginpage)
    messages.error(request, "Enter Username and Password")
    return redirect(applicantloginpage)

def clientlogout(request):
    del request.session["username"]
    del request.session["password"]
    messages.success(request, "Logged Out")
    return redirect(applicantloginpage)

def profile(request):
    em = request.session["username"]
    cd = clientDB.objects.get(Email=em)
    aid = cd.ClientID
    if applicantDB.objects.filter(ApplicantID=aid).exists():
        data = applicantDB.objects.get(ApplicantID=aid)
        return render(request,"profile.html",{'cd':cd,'data':data})
    else:
        return render(request, "profile.html", {'cd': cd})


def saveprofile(request):
    if request.method=="POST":
        sal = request.POST.get("salutation")
        nam = request.POST.get("name")
        apid = request.POST.get("id")
        eml = request.POST.get("email")
        mob = request.POST.get("mobile")
        loc = request.POST.get("location")
        qua = request.POST.get("qualification")
        fld = request.POST.get("field")
        uni = request.POST.get("university")
        dur = request.POST.get("duration")
        cgp = request.POST.get("cgpa")
        com = request.POST.get("company")
        des = request.POST.get("designation")
        exp = request.POST.get("experience")
        skl = request.POST.get("skills")
        lin = request.POST.get("linkedin")
        if applicantDB.objects.filter(ApplicantID=apid).exists():
            try:
                img = request.FILES["image"]
                fs = FileSystemStorage()
                file = fs.save(img.name,img)
            except MultiValueDictKeyError:
                file = applicantDB.objects.get(ApplicantID=apid).Image
            try:
                doc = request.FILES["resume"]
                fs = FileSystemStorage()
                res = fs.save(doc.name,doc)
            except MultiValueDictKeyError:
                res = applicantDB.objects.get(ApplicantID=apid).Resume
            applicantDB.objects.filter(ApplicantID=apid).update(Image= file, Salutation= sal,
                                                                Name= nam, Email = eml,
                                                                Mobile= mob,Location= loc,
                                                                Qualification= qua,
                                                                Field= fld, University= uni,
                                                                Duration= dur, CGPA= cgp,
                                                                Company= com, Designation= des,
                                                                Experience= exp, Skills= skl,
                                                                Linkedin = lin, Resume=res, Remarks = "Updated", Status = "Pending")
        else:
            try:
                doc = request.FILES["resume"]
                fs = FileSystemStorage()
                res = fs.save(doc.name,doc)
            except MultiValueDictKeyError:
                res = None
            img = request.FILES["image"]
            obj = applicantDB(ApplicantID= apid, Image= img, Salutation= sal,
                              Name= nam, Email = eml, Mobile= mob,Location= loc,
                              Qualification= qua, Field= fld, University= uni,
                              Duration= dur, CGPA= cgp, Company= com,
                              Designation= des, Experience= exp, Skills= skl, Linkedin = lin,Resume=res)
            obj.save()
        messages.success(request,"Profile Updated")
        return redirect(profile)


def applicantcontact(request):
    if 'username' in request.session:
        em = request.session["username"]
        if applicantDB.objects.filter(Email=em).exists():
            appdata = applicantDB.objects.get(Email=em)
            return render(request, "applicantcontact.html", {'appdata': appdata})
        else:
            return render(request, "applicantcontact.html")
    else:
        return render(request, "applicantcontact.html")

def contactsave(request):
    if request.method=="POST":
        na = request.POST.get("name")
        em = request.POST.get("email")
        su = request.POST.get("subject")
        ms = request.POST.get("message")
        obj = contactDB(Name=na , Email=em , Subject=su , Message=ms)
        obj.save()
        return redirect(applicanthomepage)

def userprofile(request,aid):
    data = applicantDB.objects.get(ApplicantID=aid)
    if jobsaveDB.objects.filter(ApplicantID_id=data.ApplicantID).exists():
        condition = Q()
        jsdata = jobsaveDB.objects.filter(ApplicantID_id=data.ApplicantID)
        jscount = jobsaveDB.objects.filter(ApplicantID_id=data.ApplicantID).count()
        jsvalues = jsdata.values_list('JobID',flat=True)
        for i in jsvalues:
            condition |= Q(JobID=i)
        jdata = jobsDB.objects.filter(condition).order_by('JobID')[:4]
    else:
        jscount = 0
        jdata = None
    if jobapplyDB.objects.filter(ApplicantID=data.ApplicantID).exists():
        condition = Q()
        jadata = jobapplyDB.objects.filter(ApplicantID=data.ApplicantID)
        javalues = jadata.values_list('JobID', flat=True)
        for i in javalues:
            condition |= Q(JobID=i)
        japplied = jobsDB.objects.filter(condition).order_by('JobID')[:4]
        jacount = jobapplyDB.objects.filter(ApplicantID=data.ApplicantID).count()
    else:
        jacount = 0
        japplied = None
    return render(request,"userprofile.html",{'data':data,'jdata':jdata,'jscount':jscount,'japplied':japplied,
                                              'jacount':jacount})

def jobsingle(request,jid):
    if 'username' in request.session:
        em = request.session["username"]
        jsaved = None
        if applicantDB.objects.filter(Email=em).exists():
            appdata = applicantDB.objects.get(Email=em)
            if jobsaveDB.objects.filter(ApplicantID=appdata.ApplicantID, JobID=jid).exists():
                jsaved = "Saved"
        else:
            appdata = None
        jdata = jobsDB.objects.filter(Status="Verified").order_by('-JobID')[:5]
        job = jobsDB.objects.get(JobID=jid)
        res = responsibilities.objects.get(JobID=jid)
        req = otherrequirements.objects.get(JobID=jid)
        ben = benefits.objects.get(JobID=jid)
        rdata = recruiterprofileDB.objects.get(RecruiterID=job.RecruiterID)


        return render(request,"jobsingle.html",{'jdata':jdata,'job':job,
                                                'res':res,'req':req,'ben':ben,
                                                'appdata':appdata,'jsaved':jsaved,'rdata':rdata})
    else:
        messages.error(request,"Log in to view more")
        return redirect(applicantloginpage)

def jobsave(request,jobid):
    em = request.session["username"]
    if applicantDB.objects.filter(Email=em).exists():
        appdata = applicantDB.objects.get(Email=em)
        obj = jobsaveDB(ApplicantID=appdata,JobID=jobid)
        obj.save()
        messages.success(request,"Job Saved to Wishlist")
    else:
        messages.error(request,"Create a Profile")
    return redirect(joblisting)

def joblisting(request):
    if 'username' in request.session:
        em= request.session["username"]
        if applicantDB.objects.filter(Email=em).exists():
            appdata = applicantDB.objects.get(Email=em)
            jdata = jobsDB.objects.filter(Status="Verified")
            return render(request,"joblisting.html",{'appdata':appdata,'jdata':jdata})
        else :
            jdata = jobsDB.objects.filter(Status="Verified")
            return render(request, "joblisting.html", {'jdata': jdata})
    else:
        jdata = jobsDB.objects.filter(Status="Verified")
        return render(request,"joblisting.html",{'jdata':jdata})

def jobsavedlist(request):
    if 'username' in request.session:
        em = request.session["username"]
        appdata = applicantDB.objects.get(Email=em)
        condition = Q()
        jsdata = jobsaveDB.objects.filter(ApplicantID=appdata.ApplicantID)
        values = jsdata.values_list('JobID',flat=True)
        for i in values:
            condition |= Q(JobID=i)
        jdata = jobsDB.objects.filter(condition)
        return render(request,"savedjobs.html",{'appdata':appdata,'jdata':jdata})
    else:
        messages.error(request,"Log in to view")
        return redirect(applicantloginpage)

def savedjobremove(request,jid,apid):
    sjdata = jobsaveDB.objects.filter(ApplicantID=apid,JobID=jid)
    sjdata.delete()
    messages.success(request,"Removed from Wishlist")
    return redirect(joblisting)

def jobapply(request,jid):
    jdata = jobsDB.objects.get(JobID=jid)
    em = request.session["username"]
    if applicantDB.objects.filter(Email=em).exists():
        data = applicantDB.objects.get(Email=em)
        if data.Status=="Verified":
            if jobapplyDB.objects.filter(ApplicantID=data.ApplicantID,JobID=jid).exists():
                messages.error(request,"You have already applied for this Job")
            else:
                obj = jobapplyDB(JobID=jdata,Title=jdata.Title,ApplicantID=data.ApplicantID)
                obj.save()
                messages.success(request,"Application Success. Please wait for the Recruiter to contact you via Email")
        else:
            messages.error(request,"Please wait for Profile Verification")
    else:
        messages.error(request,"Create a Profile")
    return redirect(joblisting)

def appliedjobs(request):
    if 'username' in request.session:
        em = request.session["username"]
        appdata = applicantDB.objects.get(Email=em)
        condition = Q()
        jadata = jobapplyDB.objects.filter(ApplicantID=appdata.ApplicantID)
        values = jadata.values_list('JobID', flat=True)
        for i in values:
            condition |= Q(JobID=i)
        jdata = jobsDB.objects.filter(condition)
        return render(request,"appliedjobs.html",{'appdata':appdata,'jdata':jdata})
    else:
        messages.error(request,"Log in to view")
        return redirect(applicantloginpage)

def deleteaccount(request,aid):
    d1 = applicantDB.objects.filter(ApplicantID=aid)
    d2 = clientDB.objects.filter(ClientID=aid)
    d3 = applicantverifiedDB.objects.filter(ApplicantID=aid)
    d4 = jobapplyDB.objects.filter(ApplicantID=aid)
    d5 = profilebookmarkDB.objects.filter(ApplicantID=aid)
    d1.delete()
    d2.delete()
    d3.delete()
    d4.delete()
    d5.delete()
    messages.success(request,"Account Deleted")
    return redirect(clientlogout)

def changepasswordpage(request):
    em = request.session["username"]
    appdata = applicantDB.objects.get(Email=em)
    return render(request,"changepassword.html",{'appdata':appdata})

def changepassword(request,aid):
    if request.method=="POST":
        data = clientDB.objects.get(ClientID=aid)
        op = request.POST.get("current")
        nw = request.POST.get("new")
        cn = request.POST.get("confirmnew")
        if data.password != op:
            messages.error(request,"Current Password is Wrong")
            return redirect(changepasswordpage)
        elif nw != cn:
            messages.error(request,"Could not Confirm New Password")
            return redirect(changepasswordpage)
        else:
            em = request.session["username"]
            clientDB.objects.filter(Email=em).update(password=nw)
            messages.success(request,"Password Changed")
            return redirect(changepasswordpage)

def aboutpage(request):
    if 'username' in request.session:
        em = request.session["username"]
        if applicantDB.objects.filter(Email=em).exists():
            appdata = applicantDB.objects.get(Email=em)
            return render(request,"about.html",{'appdata':appdata})
        else:
            return render(request, "about.html")
    else :
        return render(request, "about.html")

def searchresult(request):
    if request.method=="POST":
        keyword = request.POST.get("query")
        typ = request.POST.get("type")
        if 'username' in request.session:
            em = request.session["username"]
            appdata = applicantDB.objects.get(Email=em)
        else:
            appdata=None
        queries = keyword.split()
        q_object = Q()
        for query in queries:
            q_object |= Q(Title__icontains=query) | Q(Company_Name__icontains=query) | Q(Location__icontains=query) | Q(Qualification__icontains=query)
        if typ!="Full Time" and typ!="Part Time":
            jdata = jobsDB.objects.filter(q_object,Status="Verified")
        else:
            jdata = jobsDB.objects.filter(q_object,Status="Verified",Type=typ)
        return render(request,"searchresult.html",{'jdata':jdata,'appdata':appdata})
