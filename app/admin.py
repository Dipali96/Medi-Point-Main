from django.contrib import admin
from .models import Contact, Day, Slot, Speciality, User_Details, Patient, Doctor, Appointment
# Register your models here.

admin.site.register(User_Details)
admin.site.register(Patient)
admin.site.register(Speciality)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Day)
admin.site.register(Slot)
admin.site.register(Contact)