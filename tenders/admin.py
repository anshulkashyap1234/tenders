from django.contrib import admin

from .models import client_table,Tender
# Register your models here.

class client_table_view(admin.ModelAdmin):
    list_display=['client_id','client_name','tender_location']

class tender_table_view(admin.ModelAdmin):
    list_display=['tender_location','e_published_date','closing_date','opening_date','title_ref_no','organisation_chain','insert_date','update_date']
    
admin.site.register(client_table,client_table_view)
admin.site.register(Tender,tender_table_view)