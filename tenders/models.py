from django.db import models

# Create your models here.
class client_table(models.Model):
    client_name=models.CharField(max_length=300)
    client_id=models.CharField(max_length=300)
    tender_location=models.CharField(max_length=300)
    client_mail=models.CharField(max_length=300)

class Tender(models.Model):
    tender_location=models.CharField(max_length=300)
    e_published_date = models.CharField(max_length=300)
    closing_date = models.CharField(max_length=300)
    opening_date = models.CharField(max_length=300)
    title_ref_no = models.CharField(max_length=255, verbose_name='Title and Ref.No./Tender ID')
    organisation_chain = models.CharField(max_length=255, verbose_name='Organisation Chain')
    insert_date = models.DateTimeField(auto_now_add=True, verbose_name='Insert Date')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Update Date')

    def __str__(self):
        return self.title_ref_no