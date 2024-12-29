from django.contrib import admin
from django.urls import path
from Notes.views import *  # Import all views from the Notes app
from Notes.views import pending_notes
from django.contrib.auth.views import LogoutView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('login/', userlogin, name='login'),
    path('admin_login/', admin_login, name='admin_login'),
    path('signup/', signup1, name='signup'),
    path('admin_home/', admin_home, name='admin_home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('changepassword/', changepassword, name='changepassword'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('upload_notes/', upload_notes, name='upload_notes'),
    path('view_mynotes/', view_mynotes, name="view_mynotes"),
    path('delete_mynotes/<int:pid>', delete_mynotes, name='delete_mynotes'),
    path('view_users/', view_users, name='view_users'),
    path('delete_user/<int:pid>', delete_user, name='delete_user'),
    path('pending_notes',pending_notes, name='pending_notes'),
    path('assign_status/<int:pid>', assign_status, name='assign_status'),
    path('accepted_notes', accepted_notes, name='accepted_notes'),
    path('rejected_notes', rejected_notes, name='rejected_notes'),
    path('all_notes', all_notes, name='all_notes'),
    path('delete_notes/<int:pid>', delete_notes, name='delete_notes'),
    path('viewallnotes', viewallnotes, name='viewallnotes'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
