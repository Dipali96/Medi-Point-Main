"""medipoint1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views

admin.site.site_header = 'Admin Panel'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage,name='homepage'),
    path('about/', views.about,name='about'),
    path('contact', views.contact,name='contact'),
    path('register/',views.register,name="register"),
    path('patient-register/',views.pregister,name="pregister"),
    path('doctor-register/',views.dregister,name="dregister"),
    path('login/',views.ulogin, name="login"),
    path('logout/',views.ulogout, name="logout"),
    path('patient-profile/',views.pprofile,name="pprofile"),
    path('doctor-profile/',views.dprofile,name="dprofile"),
    #path('doctor-bookings/',views.dbookings,name="dbookings"),
    path('schedule-booking/',views.sbookings,name="sbookings"),
    path('patient-bookings/',views.pbookings,name="pbookings"),
    path('doctor/<str:name>/',views.doctor,name="doctor"),
    path('manage-slots/',views.dmslots,name="doctor_manage_slots"),
    path('add-slots/',views.add_slot,name="doctor_add_slots"),
    path('emergency/',views.emergency,name="emergency"),
    path('Emergency Doctors/<str:name>',views.emergency_doctor,name="emergency_doctor"),
    path('delete-slot/<str:id>',views.delete_slot,name="delete_slot"),
]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)