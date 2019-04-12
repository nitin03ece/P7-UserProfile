from django.conf.urls import url
from . import views

urlpatterns = [
    url('edit_profile/(?P<username>\w+)$', views.edit_profile, name='edit_profile'),
    url('change_password/(?P<username>\w+)$', views.change_password, name='change_password'),
    url('profile/(?P<username>\w+)$', views.profile, name='profile'),
    url('sign_in/$', views.sign_in, name='sign_in'),
    url('sign_out/$', views.sign_out, name='sign_out'),
    url('sign_up/$', views.sign_up, name='sign_up'),
]
