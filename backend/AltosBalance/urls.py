from django.urls import path
from AltosBalance.views import *

urlpatterns = [
    path('',home),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('LogIn/',Login),
    path('add_payment_terms/',add_payment_terms),
    path('get_payment_terms/',getPaymentTerms),
    path('delete_payment_term/<int:id>/',delete_payment_terms),

]