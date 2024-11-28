from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class AdminUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.TextField()


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    password = models.TextField()
    appointments = models.ManyToManyField('MasterClass', through='Appointment')


class Style(models.Model):
    style_id = models.AutoField(primary_key=True)
    style_name = models.CharField(max_length=50, unique=True)


class Choreographer(models.Model):
    choreographer_id = models.AutoField(primary_key=True)
    style_id = models.ForeignKey(Style, on_delete=models.CASCADE)
    choreographer_name = models.CharField(max_length=20)


class DanceSchool(models.Model):
    dance_school_id = models.AutoField(primary_key=True)
    dance_school_name = models.CharField(max_length=20)
    dance_school_address = models.TextField()
    phone_number = models.CharField(max_length=20)


class Hall(models.Model):
    hall_id = models.AutoField(primary_key=True)
    dance_school_id = models.ForeignKey(DanceSchool, on_delete=models.CASCADE)
    hall_name = models.CharField(max_length=20)
    capacity = models.IntegerField()


class MasterClass(models.Model):
    master_class_id = models.AutoField(primary_key=True)
    choreographer_id = models.ForeignKey(Choreographer, on_delete=models.CASCADE)
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    time = models.DateTimeField()


class Appointment(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE, unique=False)
    master_class_id = models.ForeignKey(MasterClass, on_delete=models.CASCADE, unique=False)


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    dance_school_id = models.ForeignKey(DanceSchool, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=20)
    date = models.DateField()
    description = models.TextField()
