from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

import datetime
from django.utils import timezone
from django.db.models.query import QuerySet
#from registration.signals import user_registered
#user_registered.connect()


class ProduktManager(models.Manager):
    def get_by_natural_key(self, okrajsava):
        return self.get(okajsava=okrajsava)
    
class Novimanager(models.Manager):
    def get_queryset(self):
        print('dasdsadsa')
        return models.Manager.get_queryset(self).filter(okrajsava__icontains='X')
    def kkk(self):
        return self.get_queryset().filter(ime__endswith='x')
    def ggg(self):
        return self.get_queryset().filter(ime__startswith='C')
 
class kveri(QuerySet):
    def zacne(self, x):
        return self.filter(ime__startswith=x)
    def konca(self, x):
        return self.filter(ime__endswith=x)
       
class Stranka(models.Model):
    podjetje = models.CharField(max_length=100)
    naslov = models.CharField(max_length=100, blank=True, default= "")
    kraj = models.CharField(max_length=30)
    oseba = models.CharField(max_length=100, blank=True, default= "")
    skupaj_prodano = models.DecimalField(max_digits=9, decimal_places=2)
    uporabnik = models.ForeignKey(User)
    def speak(self):
        return 'To je podjetje ' + self.podjetje
    
class Produkt(models.Model):
    #objectss = Novimanager()
    objectsss = kveri().as_manager()
    objects = ProduktManager()
    ime = models.CharField(max_length=32)
    okrajsava = models.CharField(max_length=5)
    skladisce = models.ManyToManyField(Stranka)
    
    def natural_key(self):
        return self.okrajsava
    
    def __str__(self):
        return self.okrajsava
       
class Obisk(models.Model):
    datum = models.DateField()
    demo = models.ManyToManyField(Produkt, related_name='demo')
    prodaja = models.ManyToManyField(Produkt, related_name='prodaja')
    stranka = models.ForeignKey(Stranka)
    znesek = models.DecimalField(max_digits=8, decimal_places=2, default = '0')
    #demo = models.CharField(max_length=3, choices=PRODUKTI)
    #prodaja = models.CharField(max_length=3, choices=PRODUKTI)
    
  
  