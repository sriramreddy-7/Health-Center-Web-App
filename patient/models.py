from django.db import models
from django.utils import timezone

class PatientPrimaryData(models.Model):
    patient_id = models.CharField(max_length=16, unique=True)
    patient_name = models.CharField(max_length=100)
    patient_age = models.PositiveIntegerField()
    patient_dob = models.DateField()
    patient_gender = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=17)
    guardian_name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    registration_date = models.DateField(default=timezone.now)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address=models.TextField(max_length=250, default='')

    def save(self, *args, **kwargs):
        if not self.patient_id:
            date_format = timezone.now().strftime('%Y%m%d')
            today_patient_count = PatientPrimaryData.objects.filter(
                registration_date__exact=timezone.now().date()
            ).count() + 1

            # Get the previous patient ID
            previous_patient = PatientPrimaryData.objects.filter(
                patient_id__startswith=f'cchc{date_format}'
            ).order_by('-patient_id').first()

            if previous_patient:
                previous_count = int(previous_patient.patient_id[-4:])
                today_patient_count = max(today_patient_count, previous_count + 1)

            self.patient_id = f'CCHC{date_format}{today_patient_count:04d}'

        super(PatientPrimaryData, self).save(*args, **kwargs)

    def __str__(self):
        return self.patient_id



class PHR(models.Model):
    patient = models.ForeignKey('PatientPrimaryData', on_delete=models.CASCADE)
    date_and_time = models.DateTimeField(auto_now_add=True)
    height = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    pulse = models.CharField(max_length=100)
    bp = models.CharField(max_length=100)
    is_diabetic = models.BooleanField(default=False)
    diabetic_level = models.CharField(max_length=100, blank=True, null=True)
    phi = models.TextField(max_length=1000)
    pov = models.TextField(max_length=300)
    remarks = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.patient}"

# class Appointment(models.Model):
#     appointment_date = models.DateField(default=timezone.now)
#     new_patient_count = models.PositiveIntegerField(default=0)
#     old_patient_count = models.PositiveIntegerField(default=0)
#     total_appointment_count = models.PositiveIntegerField(default=0)

#     def save(self, *args, **kwargs):
#         if self.appointment_date.date() == timezone.now().date():
#             self.new_patient_count += 1
#         else:
#             self.old_patient_count += 1
#         self.total_appointment_count = self.new_patient_count + self.old_patient_count
#         super(Appointment, self).save(*args, **kwargs)

# from django.db import models
# from django.utils import timezone

# class FT(models.Model):
#     patient_id = models.CharField(max_length=16)
#     appointment_date = models.DateField(default=timezone.now)
#     is_new_patient = models.BooleanField(default=True)
#     patient_token = models.IntegerField(default=0)

#     def save(self, *args, **kwargs):
#         if not self.pk:  # Only on creation of a new instance
#             today = timezone.now().date()
#             patient_count = FT.objects.filter(patient_id__contains=f'CCHC{today.strftime("%Y%m%d")}').count()
#             self.token_number = patient_count + 1

#             patient_id_date = self.patient_id[4:12]
#             patient_id_date = timezone.datetime.strptime(patient_id_date, "%Y%m%d").date()

#             if today == patient_id_date:
#                 self.is_new_patient = True
#             else:
#                 self.is_new_patient = False

#             self.patient_id = f'CCHC{self.appointment_date.strftime("%Y%m%d")}{str(self.token_number).zfill(4)}'
#             self.check_duplicate_appointment()

#         super(FT, self).save(*args, **kwargs)

#     def check_duplicate_appointment(self):
#         if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date).exists():
#             raise ValueError("Duplicate appointment for the same patient ID and date.")

#         if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date - timezone.timedelta(days=1)).exists():
#             raise ValueError("Appointment already booked for the same patient ID on the previous day.")

#     def __str__(self):
#         return self.patient_id

from django.db import models
from django.utils import timezone

class FT(models.Model):
    patient_id = models.CharField(max_length=16, unique=True,primary_key=True)
    appointment_date = models.DateField(default=timezone.now)
    is_new_patient = models.BooleanField(default=True)
    patient_token = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation of a new instance
            today = timezone.now().date()
            patient_count = FT.objects.filter(patient_id__contains=f'CCHC{today.strftime("%Y%m%d")}').count()
            self.patient_token = patient_count + 1

            patient_id_date = self.patient_id[4:12]
            patient_id_date = timezone.datetime.strptime(patient_id_date, "%Y%m%d").date()

            if today == patient_id_date:
                self.is_new_patient = True
            else:
                self.is_new_patient = False

            self.check_duplicate_appointment()

        super(FT, self).save(*args, **kwargs)

    def check_duplicate_appointment(self):
        if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date).exists():
            raise ValueError("Duplicate appointment for the same patient ID and date.")

        if FT.objects.filter(patient_id=self.patient_id, appointment_date=self.appointment_date - timezone.timedelta(days=1)).exists():
            raise ValueError("Appointment already booked for the same patient ID on the previous day.")

    def __str__(self):
        return self.patient_id

def get_report_upload_path(instance, filename):
        # Generate the new filename based on the patient_id
        new_filename = f"{instance.patient_id}.png"
        # Return the complete upload path
        return f"reports/{new_filename}"

class RP(models.Model):
    patient_id = models.CharField(max_length=16)
    report_file = models.FileField(upload_to=get_report_upload_path)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report for Patient ID: {self.patient_id}"

    # def get_report_upload_path(instance, filename):
    #     new_filename = f"{instance.patient_id}.pdf"
    #     return f"reports/{new_filename}"




# class PR(models.Model):
#     patient_id = models.CharField(max_length=16)
#     report_file = models.FileField(upload_to=get_report_upload_path)
#     uploaded_at = models.DateTimeField(default=timezone.now)
#     report_type = models.CharField(max_length=50)
#     doctor_name = models.CharField(max_length=100)
#     is_urgent = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Report for Patient ID: {self.patient_id}"





# class PatientCount(models.Model):
#     date = models.DateField(default=timezone.now)
#     male_count = models.PositiveIntegerField(default=0)
#     female_count = models.PositiveIntegerField(default=0)
#     total_count = models.PositiveIntegerField(default=0)
#     patient = models.ForeignKey(PatientPrimaryData, on_delete=models.CASCADE)

#     @classmethod
#     def update_counts(cls, patient):
#         date_format = timezone.now().date()
#         patient_count = cls.objects.filter(date=date_format).first()

#         if not patient_count:
#             patient_count = cls(date=date_format)

#         if patient.patient_gender == 'Male':
#             patient_count.male_count += 1
#         elif patient.patient_gender == 'Female':
#             patient_count.female_count += 1

#         patient_count.total_count += 1
#         patient_count.save()


# class PatientVisit(models.Model):
#     patient = models.ForeignKey(PatientPrimaryData, on_delete=models.CASCADE)
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     visit_date = models.DateField(auto_now_add=True)
#     visit_count = models.PositiveIntegerField(default=0)

#     def increment_visit_count(self):
#         self.visit_count += 1
#         self.save()
