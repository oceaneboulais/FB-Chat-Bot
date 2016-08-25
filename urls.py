from django.conf.urls import include, url
from .views import SeeSoBotView

urlpatterns =[
		url(r'^0ce4fa400a44450ffc0ace8b7ac7a4185654eade6535b5704f/?$',SeeSoBotView.as_view()),
             ] 

