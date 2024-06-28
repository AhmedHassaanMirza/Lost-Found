#from msilib.schema import Class
from django.db import models

# Create your models 
class ImageData(models.Model):
    user=models.TextField(max_length=100)
    person_name=models.TextField(max_length=100)
    police_station=models.TextField(max_length=100,null=True)
    district_name=models.TextField(max_length=100,null=True)
    person_contact=models.IntegerField(max_length=100,null=True)
    GD_case_no=models.IntegerField(max_length=100, null=True)
    GD_case_date  =models.TextField(max_length=100, null=True)
    officer_no=models.IntegerField(max_length=100, null=True)
    photo=models.ImageField(upload_to='photos/')
    upload_date=models.TextField(null=True,blank=True)
    lost_found=models.BooleanField(default=False, null=True,blank=True)
    is_matched=models.BooleanField(default=False, null=True,blank=True)
    matched_id=models.IntegerField(default=None, null=True,blank=True)
    feats=models.BinaryField(default=None, null=True,blank=True)
    
