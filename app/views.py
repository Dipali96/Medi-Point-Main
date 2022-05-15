import email
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from matplotlib.pyplot import get
from numpy import False_
from requests import request
import geocoder
from math import sin, cos, sqrt, atan2, radians
from .models import User_Details, Patient, Speciality, Doctor, Appointment,Day,Slot,Contact
import uuid 
from django.contrib import messages
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError 
# Create your views here.
def loc(a,b,lat,lag):
	R = 6373.0
	lat1 = radians(a)
	lon1 = radians(b)
	lat2 = radians(lat)
	lon2 = radians(lag)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	print(distance)
	return distance

def homepage(request):
	return render(request, "index.html")

def pregister(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		if validate_mobile(request):
			return render(request, "pregister.html",{'error_message':'Enter valid mobile number '})
		if validate_aadhaar(request):
			return render(request, "pregister.html",{'error_message':'Enter valid Aadhaar number '})
		try:
			with transaction.atomic():
				user = User.objects.create_user(username=username, password=password)
				profile = User_Details()
				profile.username = user
			profile.is_patient = True
			profile.aadhaar = request.POST['aadhaar']
			profile.f_name = request.POST['f_name']
			profile.l_name = request.POST['l_name']
			profile.address = request.POST['address']
			profile.gender = request.POST['gender']
			profile.phone_no = request.POST['phone_no']
			profile.save()
			pat = Patient()
			pat.mrn = uuid.uuid4().hex[:10].upper()
			pat.patient = profile
			pat.save()
			return redirect("login")
		except Exception as ex:
			print(ex)
			if ex ==" UNIQUE constraint failed: app_user_details.phone_no ":
				msg = "Mobile Number Already Exists"
			elif ex == " UNIQUE constraint failed: app_user_details.aadhaar ":
				msg = "Aadhaar Number Already Exists"
			elif ex == ' UNIQUE constraint failed: auth_user.username ':
				msg = "User Name Already Exists"
			else:
				msg = ex
			return render(request, "pregister.html",{'error_message':msg})
	else:
		return render(request, "pregister.html")

    
def validate_mobile(request):
    if len(request.POST['phone_no']) == 10:
        return False
    else:
        return True        
    
def validate_aadhaar(request):
    if len(request.POST['aadhaar']) == 16:
        return False
    else:
        return True	
      
def dregister(request):
	f = Speciality.objects.all()
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		if validate_mobile(request):
			return render(request, "dregister.html",{'error_message':'Enter valid mobile number ', "f":f})
		if validate_aadhaar(request):
			return render(request, "dregister.html",{'error_message':'Enter valid Aadhaar number ', "f":f})
		try:
			with transaction.atomic():
				user = User.objects.create_user(username=username, password=password)
				profile = User_Details()
				profile.username = user
				profile.is_doctor = True
				profile.aadhaar = request.POST['aadhaar']
				profile.f_name = request.POST['f_name']
				profile.l_name = request.POST['l_name']
				profile.address = request.POST['address']
				profile.gender = request.POST['gender']
				profile.phone_no = request.POST['phone_no']
				profile.save()
				doc = Doctor()
				doc.doctor = profile
				field = request.POST['field']
				if doc.is_sos :
					doc.is_sos  =  request.POST['is_sos']
				doc.min_fee = request.POST['min_fee']
				doc.license_no = request.POST['license_no']
				doc.yoe = request.POST['yoe']
				fi = Speciality.objects.get(field=field)
				doc.field = fi
				doc.save()
				return redirect("login")
		except Exception as ex:
			if ex == "UNIQUE constraint failed: app_user_details.phone_no":
				msg = "Mobile Number Already Exists"
			elif ex == "UNIQUE constraint failed: app_user_details.aadhaar":
				msg = "Aadhaar Number Already Exists"
			elif ex == "UNIQUE constraint failed: auth_user.username":
				msg = "User Name Already Exists"
			else:
				msg = ex
			return render(request, "dregister.html",{'error_message':msg, "f":f})
	else:
		return render(request, "dregister.html", {"f":f})

def ulogin(request):
	if request.method=="POST":
		username = request.POST['username']
		password = request.POST['password']
		if username is None:
				return render(request,'login.html',{'message':'Please Enter  Username','is_message':True})
			
		user     = authenticate(username=username,password=password)
		try:
			if user is not None:
				if user.is_active:
					login(request,user)
					details = User_Details.objects.get(username=user)
					if details.is_patient:
							return redirect("pprofile")
					else:
							return redirect("dprofile")
				else:
					return render(request,'login.html',{'message':'Your account is disabled','is_message':True})
			else:
				return render(request,'login.html',{'message': 'Invalid Login','is_message':True})
		except Exception as ex:
				return render(request,'login.html',{'message': 'Invalid Login','is_message':True})
	else: return render(request,'login.html',{'is_message':False})
	
    		

@login_required
def ulogout(request):
	logout(request)
	return redirect('homepage')

@login_required
def pprofile(request):
	user = request.user
	print(user)
	user_profile = User_Details.objects.get(username=user)
	if request.method=="POST":
		user_profile.aadhaar = request.POST['aadhaar']
		user_profile.f_name = request.POST['f_name']
		user_profile.l_name = request.POST['l_name']
		user_profile.address = request.POST['address']
		user_profile.gender = request.POST['gender']
		user_profile.phone_no = request.POST['phone_no']
		user_profile.save()

	return render(request, "pprofile.html",{"profile": user_profile})

@login_required
def dprofile(request):
	user = request.user
	print(user)
	user_profile = User_Details.objects.get(username=user)
	doc = Doctor.objects.get(doctor=user_profile)
	if request.method=="POST":
		user_profile.aadhaar = request.POST['aadhaar']
		user_profile.f_name = request.POST['f_name']
		user_profile.l_name = request.POST['l_name']
		user_profile.address = request.POST['address']
		user_profile.gender = request.POST['gender']
		user_profile.phone_no = request.POST['phone_no']
		user_profile.save()

	return render(request, "dprofile.html",{"profile": user_profile, "doc":doc})

@login_required
def pbookings(request):
	current_user = request.user
	slot = Appointment.objects.filter(doctor = current_user.id)
	return render(request, "appointments.html",{"slot":slot})

@login_required
def sbookings(request):
	fields = Speciality.objects.all()
	g = geocoder.ip('me')
	lat = g.latlng[0]
	lag = g.latlng[1]
	r = []
	if request.method=="POST":
		field = Speciality.objects.get(field=request.POST["field"])
		docs = Doctor.objects.filter(field=field)
		for i in docs:
			det =  User_Details.objects.get(username=i.doctor)
			a = det.lat
			b = det.lng
			if loc(a,b,lat,lag)<1.5:
				r.append(i)
		return render(request, "sbookings.html", {"field":field,"docs":r, "a":True})
	return render(request, "sbookings.html",{"fields":fields, "a":False})

@login_required
def doctor(request,name):
	user1 = User.objects.get(username=name)
	profile = User_Details.objects.get(username=user1)
	doc = Doctor.objects.get(doctor=profile)
	appointment = Appointment.objects.filter(doctor=doc).first()
	if not appointment:
		return HttpResponse("No appointments booked")
	return HttpResponse(appointment.schedule)
	pass

@login_required
def  dmslots(request):
	user = request.user
	user_profile = User_Details.objects.get(username=user)
	if user_profile.is_doctor:
		slot = Slot.objects.filter(doctor=user_profile)
		return render(request, "dslots.html", {"slot":slot})
      
	else:
		return redirect("Be a doctor first")

def  emergency(request):
	fi = Speciality.objects.all()
	return render(request, "emergency.html",{'f':fi}) 

def  register(request):
	return render(request, "register.html")  

def  about(request):
	return render(request, "about.html")  

def  contact(request):
    if request.method=="POST":
        try:validate_email(request.POST['email'])
        except ValidationError as e:return render(request,'contact.html',{'message': 'Enter Valid Email Id','iserror':True})
        else:
           c = Contact()
           c.msg = request.POST['msg']
           c.name = request.POST['name']
           c.email= request.POST['email']
           c.subject=request.POST['subject']
           c.save()
           return render(request,'contact.html',{'message': 'We have Received your Query!We will Get Back to you soon','iserror':False})
    else:
        return render(request, "contact.html")    
# time =  time_from time_from_day - time_to time_to_day


@login_required   
def add_slot(request):
	if request.method=="POST":
		try:
			slot = Slot()
   
			field_day = request.POST['day']
			day = Day.objects.get(day = field_day)
			if day:
				name = request.user
				user1 = User.objects.get(username=name)
				profile = User_Details.objects.get(username=user1)
				slot.day = day
				slot.doctor = profile
				slot.time = request.POST['time_from'] + " "+request.POST['time_from_day'] + " - "+request.POST['time_to'] + " "+request.POST['time_to_day']
				slot.save()
			else:
				messages.error(request,'Select Valid day','alert-danger')
				return redirect('doctor_add_slots')
           
			messages.success(request,'Slot Added Succesfully','alert-success')
			return redirect("doctor_manage_slots")
		except Exception as ex:
			print(ex)
			messages.error(request,'Try again later','alert-danger')
			return redirect('doctor_manage_slots')
	else:
		day = Day.objects.all()
		return render(request, "addslot.html", {"day":day})

def  emergency_doctor(request,name):
	fi = Speciality.objects.get(field=name)
	doc = Doctor.objects.filter(field=fi).select_related('doctor','field') & Doctor.objects.filter(is_sos=True).select_related('doctor','field')
	#user_details = User_Details.objects.filter(username = doc)
	#return HttpResponse(doc)
	title = "Doctor "+name
	msg = "No Doctor Found"
	if doc:
		return render(request, "doctor_list.html", {"doc":doc,"title":title})
	else:
		return render(request, "msg.html", {"title":title,'msg':msg})

def delete_slot(request, id):
	try:
		emp = Slot.objects.get(id = id)
		emp.delete()
		messages.success(request,'Slot Deleted Succesfully','alert-success')
		return redirect("doctor_manage_slots")
	except Exception as ex:
			messages.error(request,'Try again later','alert-danger')
			return redirect('doctor_manage_slots')