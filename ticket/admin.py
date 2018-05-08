from django.contrib import admin
from django.core.mail import send_mail

from staff.models import Staff
from .models import Ticket
from .models import Prioritaet


def send_done_mail(obj):
    staff_obj = Staff.objects.get(initialies=obj.from_email)
    send_mail(
        subject=f'{obj.subject} - DONE',
        message=f'Your Subject: {obj.subject} \n\n Your Ticketmessage:  obj.comment \n\n '
                f'IT-Notice:\n\n {obj.progress} \n\nWe could resolve your Problem \n\nWith best regards from  {obj.assigned_to}',
        from_email='it@vectronic-aerospace.com',
        recipient_list=[staff_obj.email],
        fail_silently=False
    )


def make_done(modeladmin, request, queryset):
    queryset.update(done='True')
    for query in queryset:
        send_done_mail(query)


make_done.short_description = 'Mark selected Tickets as Done'


class TicketAdmin(admin.ModelAdmin):
    list_display = ['done', 'project', 'subject', 'from_email', 'prioritaet', 'assigned_to', 'created_at', ]
    list_display_links = ['done', 'project', 'subject', ]
    list_filter = ['done', 'prioritaet', 'from_email', 'project', 'created_at', ]
    actions = [make_done, ]
    readonly_fields = ['subject', 'from_email', 'comment', 'file', 'created_at', 'assigned_to', ]
    change_form_template = 'admin/change_form.html'

    def get_queryset(self, request):
        return super(TicketAdmin, self).get_queryset(request)

    def save_model(self, request, obj, form, change):
        if not obj.assigned_to:
            obj.assigned_to = request.user.username
        if obj.done:
            send_done_mail(obj)
        return super(TicketAdmin, self).save_model(request, obj, form, change)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Prioritaet)