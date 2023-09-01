from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('samples/', views.samples, name="samples"),
    path('search/', views.search_view, name='search_view'),
    path('new_sample/', views.new_sample,name='new_sample'),
    path('edit_sample/', views.edit_sample,name='edit_sample'),
    path('new_sample_success/', views.submit_new_sample, name='submit_new_sample'),
    path('edit_selected/', views.edit_selected_rows, name='edit_selected_rows'),
    path('update_selected_row/', views.update_selected_row, name='update_row'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cupping_sci/', views.cupping_session_sci, name='cupping_sci')
    ]