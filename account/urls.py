from django.urls import path

from account.views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('reset_password/', ResetPasswordView.as_view()),
    path('complete_reset_password/', CompleteResetPasswordView.as_view()),
]
