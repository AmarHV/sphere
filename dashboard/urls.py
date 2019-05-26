from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
	path('projects/new/', views.new, name='projects.new'),
	path('projects/view/<int:id>/', views.view, name='projects.view'),
	path('projects/enter_data/<int:id>/', views.enter_data, name='projects.enter_data'),
]