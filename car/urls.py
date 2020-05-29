from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('addreservation/<int:id>', views.addreservation, name='addreservation'),
    path('reservation_list', views.reservation_list, name='reservation_list'),
    path('reservation/<int:id>', views.reservation, name='reservation')
]