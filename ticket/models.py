from django.core import urlresolvers
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from projects.models import Project
from ticketsystem import settings
from .signals import send_mail_done_receiver
from .signals import send_mail_create_receiver


def file_upload_path(instance, filename, **kwargs):
    return '/'.join(['media', str(instance.subject), filename])


class DjangoMailboxMailbox(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=255)
    uri = models.CharField(max_length=255, blank=True, null=True)
    from_email = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField()
    last_polling = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_mailbox_mailbox'


class DjangoMailboxMessage(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    subject = models.CharField(max_length=255)
    message_id = models.CharField(max_length=255)
    from_header = models.CharField(max_length=255)
    to_header = models.TextField()
    outgoing = models.BooleanField()
    body = models.TextField()
    encoded = models.BooleanField()
    processed = models.DateTimeField()
    read = models.DateTimeField(blank=True, null=True)
    mailbox = models.ForeignKey(DjangoMailboxMailbox, models.DO_NOTHING)
    eml = models.CharField(max_length=100, blank=True, null=True)
    in_reply_to = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_mailbox_message'

    def __str__(self):
        return self.message_id


class DjangoMailboxMessageattachment(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    headers = models.TextField(blank=True, null=True)
    message = models.ForeignKey(DjangoMailboxMessage, models.DO_NOTHING, blank=True, null=True)
    document = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_mailbox_messageattachment'

    def __str__(self):
        return self.headers


class Prioritaet(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    project = models.ForeignKey(Project)
    subject = models.CharField(max_length=255, null=True, blank=True)
    from_email = models.CharField(blank=True, null=True, max_length=100)
    comment = models.TextField(max_length=5000, blank=True, null=True)
    file = models.FileField(null=True, blank=True, upload_to=file_upload_path)
    prioritaet = models.ForeignKey(Prioritaet, blank=True, null=True)
    progress = models.TextField(max_length=500, null=True, blank=True)
    done = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(blank=True, null=True)
    assigned_to = models.CharField(null=True, blank=True, max_length=100)

    class Meta:
        ordering = ['done', 'prioritaet', '-created_at']
        app_label = 'ticket'

    def __str__(self):
        return self.subject

    def ready(self):
        send_mail_done_receiver()

    def get_update_progress_url(self):
        return reverse('ticket:update_progress', kwargs={
            'pk': self.pk,
        })

    def get_update_prio_url(self):
        return reverse('ticket:update_prioritaet', kwargs={
            'pk': self.pk,
        })

    def get_update_comment_url(self):
        return reverse('ticket:update_comment', kwargs={
            'pk': self.pk,
        })

    def get_update_done_url(self):
        return reverse('ticket:update_done', kwargs={
            'pk': self.pk,
        })

    def get_detail_url(self):
        return reverse('ticket:detail', kwargs={
            'pk': self.pk,
        })

    def get_attachment(self):
        try:
            return reverse('ticket:download', kwargs={
                'pk': self.pk
            })
        except:
            pass

    def get_admin_url(self):
        return reverse('admin:ticket_ticket_change', args=(self.pk,))


post_save.connect(send_mail_create_receiver, sender=Ticket, apps='ticket')
