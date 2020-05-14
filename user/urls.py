from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    #path('addcomment/<int:id>', views.addcomment, name='addcomment')
    path('update/', views.user_update, name='user_update'),
    path('password/', views.change_password, name='change_password'),
    path('comments/', views.comments, name='comments'),
    path('reservations/', views.reservations, name='reservations'),
    path('deletecomment/<int:id>', views.deletecomment, name='deletecomment'),
    path('deletereservation/<int:id>', views.deletereservation, name='deletecomment'),
]