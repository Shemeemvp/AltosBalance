from django.urls import path
from AltosBalance.views import *

urlpatterns = [
    path('',home),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('LogIn/',Login),
    path('add_payment_terms/',add_payment_terms),
    path('get_payment_terms/',getPaymentTerms),
    path('delete_payment_term/<int:id>/',delete_payment_terms),
    path("companyReg_action/", companyReg_action),
    path('CompanyReg2_action2/',companyReg2_action2),
    path('Add_Modules/',addModules),
    path('staffReg_action/',staffReg_action),
    path('get_staff_data/<int:id>/',getStaffData),
    path('staffReg2_Action/',staffReg2_Action),
    path('Distributor_Registration_Action/',distributorReg_Action),
    path('get_distributor_data/<int:id>/',getDistributorData),
    path('Distributor_Registration_Action2/',distributorReg2_Action2),

    # Admin
    path('get_clients/',getClients),
    path('get_clients_requests/',getClientsRequests),
    path('Client_Req_Accept/<int:id>/',client_Req_Accept),
    path('Client_Req_Reject/<int:id>/',client_Req_Reject),
    path('get_distributors_requests/',getDistributorsRequests),
    path('get_distributors/',getDistributors),
    path('DReq_Accept/<int:id>/',distributorReq_Accept),
    path('DReq_Reject/<int:id>/',distributorReq_Reject),
    path('get_distributors_overview_data/<int:id>/',getDistributorsOverviewData),
    path('get_clients_overview_data/<int:id>/',getClientsOverviewData),

    # Distributor
    path('get_distributor_clients_requests/<int:id>/',distributorClientRequest),
    path('get_distributor_clients/<int:id>/',distributorClients),
    path('DClient_Req_Accept/<int:id>/',distributorClient_Req_Accept),
    path('DClient_Req_Reject/<int:id>/',distributorClient_Req_Reject),
    # path('check_distributor_payment_term/<int:id>/',checkDistributorPaymentTerms),

]