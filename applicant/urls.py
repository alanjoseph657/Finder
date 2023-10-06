from django.urls import path
from applicant import views

urlpatterns = [
    path('applicanthomepage/',views.applicanthomepage,name="applicanthomepage"),
    path('applicantloginpage/',views.applicantloginpage,name="applicantloginpage"),
    path('signup/',views.signup,name="signup"),
    path('clientlogin/',views.clientlogin,name="clientlogin"),
    path('clientlogout/',views.clientlogout,name="clientlogout"),
    path('profile/',views.profile,name="profile"),
    path('saveprofile/',views.saveprofile,name="saveprofile"),
    path('applicantcontact/',views.applicantcontact,name="applicantcontact"),
    path('contactsave/',views.contactsave,name="contactsave"),
    path('userprofile/<int:aid>/',views.userprofile,name="userprofile"),
    path('jobsingle/<int:jid>/', views.jobsingle, name="jobsingle"),
    path('jobsave/<int:jobid>/', views.jobsave, name="jobsave"),
    path('joblisting/', views.joblisting, name="joblisting"),
    path('jobsavedlist/', views.jobsavedlist, name="jobsavedlist"),
    path('savedjobremove/<int:jid>/<int:apid>/', views.savedjobremove, name="savedjobremove"),
    path('jobapply/<int:jid>/', views.jobapply, name="jobapply"),
    path('appliedjobs/', views.appliedjobs,name="appliedjobs"),
    path('deleteaccount/<int:aid>/', views.deleteaccount,name="deleteaccount"),
    path('changepasswordpage/', views.changepasswordpage,name="changepasswordpage"),
    path('changepassword/<int:aid>/', views.changepassword,name="changepassword"),
    path('aboutpage/', views.aboutpage,name="aboutpage"),
    path('searchresult/', views.searchresult,name="searchresult"),

]