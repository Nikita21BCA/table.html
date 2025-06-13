from django.contrib import admin
from django.urls import path
from ledger_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('delete/<int:id>/', views.delete_entry, name='delete'),
    path('edit/<int:id>/', views.edit_entry, name='edit'),
    path('export_excel/', views.export_excel, name='export_excel'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('signup/', views.signup_view, name='signup'),
]
