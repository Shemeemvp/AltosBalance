from django.urls import path
from AltosBalance.views import *

urlpatterns = [
    path('',home),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('LogIn/',Login),

]