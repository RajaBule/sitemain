from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('samples/', views.samples, name="samples"),
    path('search/', views.search_view, name='search_view'),
    path('new_sample/', views.new_sample,name='new_sample'),
    path('edit_sample/', views.edit_sample,name='edit_sample'),
    path('new_sample_success/', views.submit_new_sample, name='submit_new_sample'),
    path('samples/edit_selected/', views.edit_selected_rows, name='edit_selected_rows'),
    path('update_selected_row/', views.update_selected_row, name='update_row'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('samples/cupping_sci/', views.cupping_sci, name='cupping_sci'),
    path('save_session/', views.save_session, name='save_session'),
    path('sample_view/<str:coffee_id>/', views.sample_view, name='sample_view'),
    path('samples/search_users/', views.search_users, name='search_users'),
    path('add_to_shared/',views.add_to_shared, name='add_to_shared'),
    path('samples/delete_selected_samples/', views.delete_selected_samples, name='delete_selected_samples'),
    path('inventory/', views.inventory, name='inventory'),
    path('inventory/new', views.invnew, name='invnew'),
    path('inventory/new/submit', views.submit_new_inventory, name='submitinv')
    ]