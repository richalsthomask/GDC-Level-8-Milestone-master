
from celery.decorators import periodic_task
from datetime import timedelta
from django.contrib.auth.models import User
from tasks.models import Task, Client
from django.core.mail import send_mail
import datetime

@periodic_task(run_every=timedelta(seconds=60))
def sent_email_reminder():
    print('senting email reminders now')
    current_time=datetime.datetime.utcnow()+datetime.timedelta(hours=5.5)
    for user in User.objects.all():
        client=Client.objects.filter(user=user).first()
        
        if(client is None 
           or client.daily_email_time is None 
           or client.email is None 
           or client.daily_email_time.hour!=current_time.hour 
           or client.daily_email_time.minute!=current_time.minute
        ):
            continue
        tasks=Task.objects.filter(user=user,deleted=False,status='PENDING')
        email_content=f'You have {tasks.count()} tasks pending\n'
        for task in tasks:
            email_content+=f'{task.title} - {task.description}\n'
        send_mail('pending tasks',email_content,'tasks@gmail.com',[client.email])
