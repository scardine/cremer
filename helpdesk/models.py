from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    STATUS = (
        (1, u'Active'),
        (0, u'Inactive'),
        (2, u'Blocked'),
    )
    name = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS)
    account_manager = models.ForeignKey(User)
    notify = models.BooleanField(u'Notify account manager on activity?', default=True)

    def __unicode__(self):
        return self.name


class Incident(models.Model):
    STATUS = (
        (0, u'Support'),
        (1, u'Billing'),
        (2, u'Closed'),
    )
    CHARGE = (
        (0, 'Client'),
        (1, 'Pax'),
        (2, 'Agency'),
        (3, 'Other'),
    )
    client = models.ForeignKey(Client)
    status = models.IntegerField(choices=STATUS, default=0)
    date = models.DateTimeField(auto_now_add=True)
    locator = models.CharField(max_length=30, blank=True, null=True)
    pcc = models.CharField(max_length=30, blank=True, null=True)
    pax_name = models.CharField(max_length=40)
    pax_email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200)
    responsible = models.ForeignKey(User)
    charge = models.IntegerField(choices=CHARGE, default=0)
    bill_to = models.CharField(max_length=100, blank=True, null=True)
    bill_address = models.TextField(blank=True, null=True)
    tax_number = models.CharField(max_length=30, blank=True, null=True)
    invoice_number = models.CharField(max_length=30, null=True, blank=True)

    def __unicode__(self):
        return "#{s.id} ({s.client})".format(s=self)


class IncidentLog(models.Model):
    incident = models.ForeignKey(Incident)
    date = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey(User)
    description = models.TextField()


#class Aerial(models.Model):
#    TYPE = (
#        (0, 'Other'),
#        (1, 'Reservation'),
#        (2, )
#    )
#    incident = models.ForeignKey(Incident)
#    date = models.DateTimeField(auto_now_add=True)
#    type = models.IntegerField(choices=TYPE)
#    description = models.TextField()

