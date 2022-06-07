from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('me', views.get_me, name='get-me'),
    path('classifications', views.get_classifications, name='classifications'),
    path('entity', views.get_next_entity, name='next-entity'),
    path('entity/<uuid>', views.write_entity_data, name='write-entity'),
]
