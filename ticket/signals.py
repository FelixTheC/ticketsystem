from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from staff.models import Staff


def send_mail_done_receiver(sender, instance, *args, **kwargs):
    if instance.done == True:
        staff_obj = Staff.objects.get(initialies=instance.from_email)
        send_mail(
            subject=f'[Ticketsystem] {instance.subject}',
            message=f'Your Subject: {instance.subject} \n\n We could resolve your Problem '
                    f'\n\n With best regards your it-Team from VECTRONIC Aerospace ',
            from_email='foo@bar.com',
            recipient_list=[staff_obj.email],
            fail_silently=False
        )


def send_mail_create_receiver(sender, instance, *args, **kwargs):
    staff = Staff.objects.get(initialies=instance.from_email)
    if kwargs['created'] == True:
        send_mail(
            subject=f'[Ticketsystem] {instance.subject}',
            message=f'A new ticket was created \n\n Subject: {instance.subject} \n\n'
                    f' http://192.168.0.34:9004/admin/ticket/ticket/{instance.pk}/change/',
            from_email=staff.email,
            recipient_list=['foo@bar.com'],
            fail_silently=False
        )