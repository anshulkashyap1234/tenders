from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from datetime import date, datetime
import traceback
from etenders.settings import EMAIL_HOST_USER
from .models import client_table,Tender
from .etenders import main
def send_templated_email(subject,email,msg, **kwargs):
    try:

        from_email = EMAIL_HOST_USER
        msgtoUser = EmailMultiAlternatives(subject=subject, body=msg, from_email=from_email,
                                            to=email)
        try:
            attachment = kwargs['attachment_path']
            if type(attachment) is list:
                for files in attachment:
                    msgtoUser.attach_file(files)
            else:
                msgtoUser.attach_file(attachment)
        except Exception as e:
            attachment = None

        msgtoUser.attach_alternative(msg, "text/html")
        msgtoUser.send()


    except Exception as e:
        print("couldnt send email")
        print(str(e))

def send_new_tender_main(client_mail,location):
    tday = date.today()
    start_datetime = datetime.combine(tday, datetime.min.time())  # Start of today
    # my_filtered_data = Tender.objects.filter(insert_date__gte=start_datetime, tender_location=location)
    my_filtered_data = Tender.objects.filter(tender_location=location)

    try:
        subject = f"New Tender in {location}"
        username = "Sir/Ma'am"
        context = {'old_obj': my_filtered_data, 'username': username}
        message = render_to_string('New_Case_Template_Khaitan.html', context)
        send_templated_email(subject=subject, email=[client_mail], msg=message)
        print("Email sent")
    except Exception as e:
        print(f"Invalid header or validation error: {e}")
    return HttpResponse("Email sent successfully")


def running_client_location_crowling():
    client_objs=client_table.objects.all()
    for i in client_objs:
        result=main(i.tender_location)
        if result[0]==1:
            send_new_tender_main(i.client_mail,i.tender_location)
        else:
            print('tender mail not send')