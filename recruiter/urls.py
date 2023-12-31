from django.urls import path,include
from recruiter import views

urlpatterns = [
    path('recruiterhome/',views.recruiterhome,name="recruiterhome"),
    path('postjob/',views.postjob,name="postjob"),
    path('recruiterloginpage/',views.recruiterloginpage,name="recruiterloginpage"),
    path('recruitersignup/',views.recruitersignup,name="recruitersignup"),
    path('recruiterlogin/',views.recruiterlogin,name="recruiterlogin"),
    path('recruiterlogout/',views.recruiterlogout,name="recruiterlogout"),
    path('savejob/',views.savejob,name="savejob"),
    path('recruitercontactpage/',views.recruitercontactpage,name="recruitercontactpage"),
    path('recruitercontactsave/',views.recruitercontactsave,name="recruitercontactsave"),
    path('recruiterprofile/',views.recruiterprofile,name="recruiterprofile"),
    path('recruiterprofilesave/<int:rid>/',views.recruiterprofilesave,name="recruiterprofilesave"),
    path('profilepage/<int:rid>/',views.profilepage,name="profilepage"),
    path('recruiteraboutpage/',views.recruiteraboutpage,name="recruiteraboutpage"),
    path('postedjobs/',views.postedjobs,name="postedjobs"),
    path('postedjobsingle/<int:jid>/',views.postedjobsingle,name="postedjobsingle"),
    path('candidatelist/',views.candidatelist,name="candidatelist"),
    path('changepasswordrecruiter/',views.changepasswordrecruiter,name="changepasswordrecruiter"),
    path('passwordchange/<int:rid>/',views.passwordchange,name="passwordchange"),
    path('candidatesingle/<int:aid>/',views.candidatesingle,name="candidatesingle"),
    path('deletejob/<int:jid>/',views.deletejob,name="deletejob"),
    path('applications/<int:jid>/',views.applications,name="applications"),
    path('deleterecruiter/<int:rid>/',views.deleterecruiter,name="deleterecruiter"),
    path('recruitersearchresult/',views.recruitersearchresult,name="recruitersearchresult"),
    path('bookmarkprofile/<int:aid>/',views.bookmarkprofile,name="bookmarkprofile"),
    path('bookmarklist/',views.bookmarklist,name="bookmarklist"),
    path('bookmarkremove/<int:aid>/',views.bookmarkremove,name="bookmarkremove"),
    path('resumedownload/<int:aid>/download/',views.resumedownload,name="resumedownload"),
]