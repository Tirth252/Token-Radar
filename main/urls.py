from django.urls import path
from .views import Home, alltimebestView,coinsubmissionView, coindetailView,SearchcoinView, privacypolicy
from . import views
from django.conf.urls import url
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('coin/new/', coinsubmissionView.as_view() , name='coinsubmit'),
    path('coin/<int:pk>/',coindetailView.as_view(), name = 'coin'),
    path("alltimebest/", alltimebestView.as_view(),name= 'alltimebest'),
    path("coin/<int:pk>/vote/",views.Vote, name = 'vote'),
    path("search/",SearchcoinView.as_view(),name = 'search'),
    path("privacypolicy",privacypolicy,name= "privacypolicy"),

]