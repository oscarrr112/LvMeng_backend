
from django.urls import path, include

urlpatterns = [
    path('auth/', include('authorize.urls')),
    path('suggest/', include('suggestion.urls'))
]