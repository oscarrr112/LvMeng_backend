
from django.urls import path

from authorize import views

urlpatterns = [
    path('authorize', views.AuthorizedView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('idCert', views.IDCertificationView.as_view()),
    path('phoneCert', views.PhoneCertificationView.as_view()),
    path('image', views.ImageView.as_view()),
    path('nickname', views.NickNameView.as_view())
]
