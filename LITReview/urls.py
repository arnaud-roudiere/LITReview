from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('signup/', authentication.views.signup_page, name='signup'),

    path('home/', blog.views.flux, name='home'),
    path('ticket_review/create/', blog.views.create_ticket_and_review_view, name='create_ticket_review'),
    path('ticket/create/', blog.views.create_ticket_view, name='create_ticket'),
    path('ticket/<int:ticket_id>/delete', blog.views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:id>/update', blog.views.update_ticket, name='update_ticket'),
    path('posts/', blog.views.posts_view, name='posts'),
    path('flux/', blog.views.flux, name='flux'),
    path('follow/', blog.views.follow_users_view, name='follow'),
    path('follow/<int:id>/remove', blog.views.remove_following_user_view, name='remove_following'),
    path('review/create/<int:ticket_id>', blog.views.create_review, name='create_review'),
    path('review/<int:review_id>/update', blog.views.update_review, name='update_review'),
    path('review/<int:review_id>/delete', blog.views.delete_review, name='delete_review'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
