import datetime
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from recruiter.models import recruiterDB,jobsDB,responsibilities,benefits,otherrequirements,recruiterprofileDB,jobapplyDB,profilebookmarkDB
from backend.models import applicantverifiedDB,contactDB,jobsverifiedDB
from applicant.models import jobsaveDB,applicantDB
from django.db.models import Q

# Create your views here.

def recruiterhome(request):
    data = applicantverifiedDB.objects.all().order_by('ApplicantID')[:9]
    if 'username' in request.session:
        em = request.session["username"]
        rdata = recruiterDB.objects.get(Email=em)
        if recruiterprofileDB.objects.filter(RecruiterID=rdata.RecruiterID).exists():
            if recruiterprofileDB.objects.get(RecruiterID=rdata.RecruiterID).Status=="Verified":
                rpdata = recruiterprofileDB.objects.filter(RecruiterID=rdata.RecruiterID)
                return render(request,"recruiterhome.html",{'data':data,'rdata':rdata,'rpdata':rpdata})
            else:
                return render(request, "recruiterhome.html", {'data': data, 'rdata': rdata})

        else:
            return render(request, "recruiterhome.html", {'data': data, 'rdata': rdata})
    else :
        return render(request, "recruiterhome.html", {'data': data})

def postjob(request):
    em = request.session["username"]
    data = recruiterDB.objects.get(Email=em)
    if recruiterprofileDB.objects.filter(Email=em).exists():
        status = recruiterprofileDB.objects.get(Email=em).Status
        if status=="Pending":
            messages.error(request,"Please wait until your profile completes verification")
            return redirect(recruiterprofile)
        else:
            return render(request, "postjob.html", {'data': data})
    else:
        messages.error(request,"Create a Profile to Post a Job")
        return redirect(recruiterprofile)

def recruiterloginpage(request):
    return render(request,"recruiterlogin.html")

def recruitersignup(request):
    if request.method == "POST":
        nm = request.POST.get("name")
        em = request.POST.get("email")
        pw = request.POST.get("password")
        cp = request.POST.get("cpassword")
        im = request.FILES["image"]
        if recruiterDB.objects.filter(Email = em).exists():
            messages.error(request,"Email ID already taken")
            return redirect(recruiterloginpage)
        else:
            if pw == cp:
                obj = recruiterDB(Name= nm, Email= em,Password = pw, Logo=im )
                obj.save()
                messages.success(request,"Sign Up Success. Log in now")
                return redirect(recruiterloginpage)
            else:
                messages.error(request, "Password Does not match")
                return redirect(recruiterloginpage)

def recruiterlogin(request):
    if request.method == "POST":
        em = request.POST.get("email")
        pw = request.POST.get("password")
        if recruiterDB.objects.filter(Email=em,Password=pw).exists():
            request.session["username"]=em
            request.session["password"]=pw
            return redirect(recruiterhome)
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect(recruiterloginpage)
    messages.error(request, "Enter Username and Password")
    return redirect(recruiterloginpage)

def recruiterlogout(request):
    del request.session["username"]
    del request.session["password"]
    messages.success(request, "Logged Out")
    return redirect(recruiterloginpage)

def savejob(request):
    if request.method=="POST":
        rid = request.POST.get("rid")
        rd = recruiterDB.objects.get(RecruiterID=rid)
        title = request.POST.get("title")
        email = request.POST.get("email")
        loc = request.POST.get("location")
        jt = request.POST.get("type")
        pd = datetime.datetime.now()
        ddate = request.POST.get("deadline")
        exp = request.POST.get("experience")
        gen = request.POST.get("gender")
        salary = request.POST.get("salary")
        qua = request.POST.get("qualification")
        desc = request.POST.get("description")
        res1 = request.POST.get("res1")
        res2 = request.POST.get("res2")
        res3 = request.POST.get("res3")
        res4 = request.POST.get("res4")
        res5 = request.POST.get("res5")
        res6 = request.POST.get("res6")
        res7 = request.POST.get("res7")
        res8 = request.POST.get("res8")
        res9 = request.POST.get("res9")
        res10 = request.POST.get("res10")
        req1 = request.POST.get("req1")
        req2 = request.POST.get("req2")
        req3 = request.POST.get("req3")
        req4 = request.POST.get("req4")
        req5 = request.POST.get("req5")
        ben1 = request.POST.get("ben1")
        ben2 = request.POST.get("ben2")
        ben3 = request.POST.get("ben3")
        ben4 = request.POST.get("ben4")
        ben5 = request.POST.get("ben5")
        obj = jobsDB(RecruiterID=rid, Company_Name=rd.Name, Logo=rd.Logo, Title=title , Email=email, Location=loc,
                     Type=jt, Published=pd.date(), Deadline=ddate, Experience=exp,
                     Gender=gen, Salary=salary, Qualification=qua, Description=desc)
        obj.save()
        resobj = responsibilities(JobID=obj,res1=res1,res2=res2,res3=res3,res4=res4,
                                  res5=res5,res6=res6,res7=res7,res8=res8,
                                  res9=res9,res10=res10)
        resobj.save()
        reqobj = otherrequirements(JobID=obj, req1=req1, req2=req2, req3=req3, req4=req4,
                                  req5=req5)
        reqobj.save()
        benobj = benefits(JobID=obj, ben1=ben1, ben2=ben2, ben3=ben3, ben4=ben4,
                                  ben5=ben5)
        benobj.save()
        messages.success(request,"Job Saved")
        return redirect(postjob)

def recruitercontactpage(request):
    if 'username' in request.session:
        em = request.session["username"]
        rdata = recruiterDB.objects.get(Email=em)
        return render(request,"recruitercontact.html",{'rdata':rdata})
    else:
        return render(request, "recruitercontact.html")

def recruitercontactsave(request):
    if request.method=="POST":
        na = request.POST.get("name")
        em = request.POST.get("email")
        su = request.POST.get("subject")
        ms = request.POST.get("message")
        obj = contactDB(Name=na , Email=em , Subject=su , Message=ms)
        obj.save()
        messages.success(request,"Message Sent. Our Admin will Reach You Soon")
        return redirect(recruitercontactpage)

def recruiterprofile(request):
    em = request.session["username"]
    data = recruiterDB.objects.get(Email=em)
    if recruiterprofileDB.objects.filter(Email=em).exists():
        rpdata = recruiterprofileDB.objects.get(RecruiterID_id=data.RecruiterID)
        return render(request,"recruiterprofile.html",{'data':data,'rpdata':rpdata})
    else:
        return render(request,"recruiterprofile.html",{'data':data})

def recruiterprofilesave(request,rid):
    if request.method=="POST":
        data = recruiterDB.objects.get(RecruiterID=rid)
        logo = data.Logo
        em = request.session["username"]
        desc = request.POST.get("description")
        loc = request.POST.get("location")
        mob = request.POST.get("contact")
        web = request.POST.get("website")
        doc1 = request.FILES["doc1"]
        doc2 = request.FILES["doc2"]
        doc3 = request.FILES["doc3"]
        if recruiterprofileDB.objects.filter(RecruiterID=rid).exists():
            try:
                fs = FileSystemStorage()
                d1 = fs.save(doc1.name,doc1)
                d2 = fs.save(doc2.name,doc2)
                d3 = fs.save(doc3.name,doc3)
            except MultiValueDictKeyError:
                d1 = recruiterprofileDB.objects.get(RecruiterID=rid).Doc1
                d2 = recruiterprofileDB.objects.get(RecruiterID=rid).Doc2
                d3 = recruiterprofileDB.objects.get(RecruiterID=rid).Doc3
            recruiterprofileDB.objects.filter(RecruiterID=data).update(Email=em,Description=desc,
                                                                      Location=loc,Contact=mob,
                                                                       Website=web,
                                                                      Doc1=d1,Doc2=d2,Doc3=d3,
                                                                      Status="Pending")
        else:
            obj = recruiterprofileDB(RecruiterID=data,Logo=logo,Name=data.Name,Email=em,Description=desc,
                                     Location=loc,Contact=mob,Website=web,Doc1=doc1,Doc2=doc2,Doc3=doc3)
            obj.save()
        messages.success(request,"Profile Updated. Please Wait for Verification")
        return redirect(recruiterprofile)

def profilepage(request,rid):
    if recruiterprofileDB.objects.filter(RecruiterID=rid).exists():
        data = recruiterprofileDB.objects.get(RecruiterID=rid)
        jdata = jobsDB.objects.filter(RecruiterID=rid).order_by('JobID')[:5]
        return render(request,"recruiterprofilepage.html",{'data':data,'jdata':jdata})
    else:
        return redirect(recruiterprofile)

def recruiteraboutpage(request):
    if 'username' in request.session:
        em = request.session["username"]
        rdata = recruiterDB.objects.get(Email=em)
        return render(request, "recruiterabout.html", {'rdata': rdata})
    else:
        return render(request, "recruiterabout.html")

def postedjobs(request):
    if 'username' in request.session:
        em = request.session["username"]
        rdata = recruiterDB.objects.get(Email=em)
        jdata = jobsDB.objects.filter(RecruiterID=rdata.RecruiterID)
        return render(request,"jobs.html",{'rdata':rdata,'jdata':jdata})
    else:
        messages.error(request,"Log in to view more")
        return redirect(recruiterloginpage)

def postedjobsingle(request,jid):
    em = request.session["username"]
    rdata = recruiterprofileDB.objects.get(Email=em)
    job = jobsDB.objects.get(JobID=jid)
    res = responsibilities.objects.get(JobID=jid)
    req = otherrequirements.objects.get(JobID=jid)
    ben = benefits.objects.get(JobID=jid)
    appcount = jobapplyDB.objects.filter(JobID=jid).count()
    return render(request,"postedjobsingle.html",{'job':job,'appcount':appcount,
                                                'res':res,'req':req,'ben':ben,
                                                'rdata':rdata})

def candidatelist(request):
    data = applicantverifiedDB.objects.all()
    if 'username' in request.session:
        em = request.session["username"]
        rdata = recruiterDB.objects.get(Email=em)
        if recruiterprofileDB.objects.get(RecruiterID=rdata.RecruiterID).Status == "Verified":
            rpdata = recruiterprofileDB.objects.filter(RecruiterID=rdata.RecruiterID)
            return render(request, "candidates.html", {'data': data, 'rdata': rdata, 'rpdata': rpdata})
        else:
            return render(request, "candidates.html", {'data': data, 'rdata': rdata})
    else:
        return render(request, "candidates.html", {'data': data})

def changepasswordrecruiter(request):
    em = request.session["username"]
    rdata = recruiterDB.objects.get(Email=em)
    return render(request, "changepasswordrecruiter.html", {'rdata': rdata})

def passwordchange(request,rid):
    if request.method == "POST":
        data = recruiterDB.objects.get(RecruiterID=rid)
        op = request.POST.get("current")
        nw = request.POST.get("new")
        cn = request.POST.get("confirmnew")
    if data.Password != op:
        messages.error(request, "Current Password is Wrong")
        return redirect(changepasswordrecruiter)
    elif nw != cn:
        messages.error(request, "Could not Confirm New Password")
        return redirect(changepasswordrecruiter)
    else:
        em = request.session["username"]
        recruiterDB.objects.filter(Email=em).update(Password=nw)
        messages.success(request, "Password Changed")
        return redirect(changepasswordrecruiter)

def candidatesingle(request,aid):
    if 'username' in request.session:
        em= request.session["username"]
        if recruiterprofileDB.objects.filter(Email=em).exists():
            rdata = recruiterprofileDB.objects.get(Email=em)
            if rdata.Status=="Verified":
                appdata = applicantverifiedDB.objects.get(ApplicantID=aid)
                bmdata = profilebookmarkDB.objects.filter(RecruiterID=rdata.RecruiterID,ApplicantID=aid)
                return render(request,"candidatesingle.html",{'appdata':appdata,'rdata':rdata,'bmdata':bmdata})
            else:
                messages.error(request, "Pease wait for Profile Verification")
                return redirect(recruiterprofile)
        else:
            messages.error(request,"Create a Profile First")
            return redirect(recruiterprofile)
    else:
        messages.error(request,"Log in to View")
        return redirect(recruiterloginpage)

def deletejob(request,jid):
    data = jobsDB.objects.filter(JobID=jid)
    data1 = jobsaveDB.objects.filter(JobID=jid)
    data2 = jobsverifiedDB.objects.filter(JobID=jid)
    data.delete()
    data1.delete()
    data2.delete()
    messages.success(request,"Data Deleted")
    return redirect(postedjobs)

def applications(request,jid):
    em = request.session["username"]
    rdata = recruiterDB.objects.get(Email=em)
    condition = Q()
    jdata = jobapplyDB.objects.filter(JobID=jid)
    values = jdata.values_list('ApplicantID',flat=True)
    for i in values:
        condition |= Q(ApplicantID=i)
    appdata = applicantverifiedDB.objects.filter(condition)
    return render(request,"applications.html",{'rdata':rdata,'appdata':appdata})

def deleterecruiter(request,rid):
    data = recruiterprofileDB.objects.filter(RecruiterID=rid)
    data1 = recruiterDB.objects.filter(RecruiterID=rid)
    job = jobsDB.objects.filter(RecruiterID=rid)
    condition= Q()
    values = job.values_list('JobID',flat=True)
    for i in values:
        condition |=Q(JobID=i)
    jdata = jobsaveDB.objects.filter(condition)
    jdata1 = jobsverifiedDB.objects.filter(condition)
    data.delete()
    data1.delete()
    job.delete()
    jdata.delete()
    jdata1.delete()
    messages.success(request,"Data Deleted")
    return redirect(recruiterloginpage)

def recruitersearchresult(request):
    if request.method=="POST":
        keyword = request.POST.get("query")
        if 'username' in request.session:
            em = request.session["username"]
            rdata = recruiterDB.objects.get(Email=em)
        else:
            rdata=None
        queries = keyword.split( )
        q_object = Q()
        for query in queries:
            q_object |= Q(Field__icontains=query) | Q(Name__icontains=query) | Q(Qualification__icontains=query)
        data = applicantverifiedDB.objects.filter(q_object)
        if data is None:
            return render(request, "recruitersearchresult.html", { 'rdata': rdata})
        else:
            return render(request, "recruitersearchresult.html", {'data': data, 'rdata': rdata})

def bookmarkprofile(request,aid):
    em = request.session["username"]
    rdata = recruiterDB.objects.get(Email=em)
    obj = profilebookmarkDB(RecruiterID=rdata,ApplicantID=aid)
    obj.save()
    messages.success(request,"Profile Saved to Bookmarks")
    return redirect(candidatelist)

def bookmarklist(request):
    if 'username' in request.session:
        em = request.session["username"]
        rdata = recruiterDB.objects.get(Email=em)
        condition = Q()
        bmdata = profilebookmarkDB.objects.filter(RecruiterID=rdata.RecruiterID)
        if bmdata.count()==0:
            return render(request, "bookmarks.html", {'rdata': rdata})
        else:
            values = bmdata.values_list('ApplicantID',flat=True)
            for i in values:
                condition |= Q(ApplicantID=i)
            data = applicantverifiedDB.objects.filter(condition)
            return render(request,"bookmarks.html",{'rdata':rdata,'data':data})
    else:
        messages.error(request,"Log in to View")
        return redirect(recruiterloginpage)

def bookmarkremove(request,aid):
    em = request.session["username"]
    rdata = recruiterDB.objects.get(Email=em)
    data = profilebookmarkDB.objects.filter(RecruiterID=rdata.RecruiterID,ApplicantID=aid)
    data.delete()
    messages.success(request,"Bookmark Removed")
    return redirect(bookmarklist)

def resumedownload(request,aid):
    data = applicantDB.objects.get(ApplicantID=aid).Resume
    pdf_file = get_object_or_404(applicantDB,ApplicantID=aid)
    response = FileResponse(pdf_file.Resume,as_attachment=True)
    return response
