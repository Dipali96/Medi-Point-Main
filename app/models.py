from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
import geocoder


class User_Details(models.Model):
    
	username = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
	aadhaar = models.CharField(max_length=16,unique=True)
	f_name = models.CharField(max_length=25, blank=True)
	l_name = models.CharField(max_length=25, blank=True)
	phone_no = models.IntegerField(blank=True,unique=True)
	gender = models.CharField(max_length=1)
	is_doctor = models.BooleanField(default = False)
	is_patient = models.BooleanField(default = False)
	g = geocoder.ip('me')
	lat = models.FloatField(default=g.latlng[0])
	lng = models.FloatField(default=g.latlng[1])

	def __str__(self):
		return self.username.username

class Patient(models.Model):
	patient = models.OneToOneField(User_Details, on_delete=models.CASCADE, primary_key=True)
	mrn = models.CharField(max_length=25, blank=True,unique=True)

	def __str__(self):
		return self.patient.username.username


class Speciality(models.Model):
	field = models.CharField(max_length=25)

	def __str__(self):
		return self.field

class Day(models.Model):
	day = models.CharField(max_length=25)
	def __str__(self):
		return self.day

class Doctor(models.Model):
	doctor = models.OneToOneField(User_Details, on_delete=models.CASCADE, primary_key=True)
	field = models.ForeignKey(Speciality, on_delete=models.CASCADE)
	is_sos = models.BooleanField(default = False)
	min_fee = models.IntegerField(default=0)
	yoe = models.IntegerField(default=0)
	license_no = models.TextField(max_length=100, blank=True,unique=True)
	is_approved = models.BooleanField(default = False)
	qualification = models.CharField(max_length=100, blank=True)
	def __str__(self):
		return (self.doctor.username.username+" - "+ self.field.field)
class address(models.Model):
	doctor = models.ForeignKey(User_Details, on_delete=models.CASCADE, primary_key=True)
	address_1 = models.TextField(max_length=100, blank=True)
	address_2 = models.TextField(max_length=100, blank=True)
	city = models.TextField(max_length=100, blank=True)
	name = models.TextField(max_length=100, blank=True)
	type = models.TextField(max_length=100,default="HOSPITAL")
	pincode = models.IntegerField(max_length=6,default = False)
	def __str__(self):
		return (self.doctor.username.username+" - "+ self.field.field)
class Slot(models.Model):
	id = models.AutoField(primary_key=True)
	doctor = models.ForeignKey(User_Details, on_delete=models.CASCADE)
	day = models.ForeignKey(Day, on_delete=models.CASCADE)
	time = models.CharField(max_length=60, blank=True)
	max_appointment = models.IntegerField(max_length=60, default=0) # 0 FOR NO LIMIT ON APPOINTMENT BOOKING 
	address = models.ForeignKey(Address, on_delete=models.CASCADE)
	def __str__(self):
		return (self.doctor.username.username+" - "+ self.day.day+"-"+self.time)

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    msg = models.TextField(max_length=300)
    name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return (self.subject+"-"+self.name)

class Appointment(models.Model):
	a_id = models.AutoField(primary_key=True)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	date = models.CharField(max_length=10, blank=True)
	schedule = models.CharField(max_length=500, blank=True)
	day = models.CharField(max_length=500, blank=True)
	status = models.CharField(default="PENDING",max_length=500)
	pay_status = models.CharField(default="PENDING",max_length=500)

	def __str__(self):
		return (self.doctor.doctor.username.username+"-"+self.patient.patient.username.username+"-"+self.date)