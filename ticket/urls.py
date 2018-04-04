from django.conf.urls import url
from ticket import views
from .views import PrioUpdateView
from .views import DoneUpdateView
from .views import TicketDetailView
from .views import TicketCreateView
from .views import ProgressUpdateView
from .views import UpdateCommentView

app_name='ticket'
urlpatterns = [
    url(r'^overview/$', views.ticket_list, name='list'),
    url(r'^$', TicketCreateView.as_view(), name='create_ticket'),
    url(r'^update_prio/(?P<pk>[\d]+)/$', PrioUpdateView.as_view(), name='update_prioritaet'),
    url(r'^update_done/(?P<pk>[\d]+)/$', DoneUpdateView.as_view(), name='update_done'),
    url(r'^update_comment/(?P<pk>[\d]+)/$', UpdateCommentView.as_view(), name='update_comment'),
    url(r'^update_progress/(?P<pk>[\d]+)/$', ProgressUpdateView.as_view(), name='update_progress'),
    url(r'^detail/(?P<pk>[\d]+)/$', TicketDetailView.as_view(), name='detail'),
    url(r'^download/(?P<pk>[\d]+)/$', views.download_file, name='download'),
]
