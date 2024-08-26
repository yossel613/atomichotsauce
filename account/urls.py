from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('account/', views.account, name='account' ),
    
    path('registration/email-verification/<str:uidb64>/<str:token>', views.email_verification, name='email_verification'),
    path('email-verification-sent/', views.email_verification_sent, name='email_verification_sent'),
    path('email-verification-success/', views.email_verification_success, name='email_verification_success'),
    path('email-verification-failed/', views.email_verification_failed, name='email_verification_failed'),
    
    path('my-login/', views.my_login, name='my_login'),
    path('user-logout/', views.user_logout, name='user_logout'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete-account'),
    
    path('reset_password', auth_views.PasswordResetView.as_view(template_name='account/password/password-reset.html'), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password-reset-sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password-reset-form.html'), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password-reset-complete.html'), name='password_reset_complete'),

    path('manage-shipping', views.manage_shipping, name='manage-shipping'),
    path('track-orders', views.track_orders, name='track-orders'),
]
