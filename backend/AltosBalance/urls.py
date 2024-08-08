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
    path('fetch_admin_notifications/',fetchAdminNotifications),
    path('admin_notification_overview/<int:id>/',getAdminNotificationOverview),
    path('accept_module_updation_request/', module_Updation_Accept),
    path('reject_module_updation_request/', module_Updation_Reject),

    path('user/<int:id>/',getSelfData),

    # Distributor
    path('get_distributor_clients_requests/<int:id>/',distributorClientRequest),
    path('get_distributor_clients/<int:id>/',distributorClients),
    path('DClient_Req_Accept/<int:id>/',distributorClient_Req_Accept),
    path('DClient_Req_Reject/<int:id>/',distributorClient_Req_Reject),
    path('check_distributor_payment_term/<int:id>/',checkDistributorPaymentTerms),

    path('get_distributor_profile_data/<int:id>/',getDistributorProfileData),
    path('Change_distributor_payment_terms/',changeDistributorPaymentTerms),
    path('edit_distributor_profile/',editDistributorProfile),
    path('fetch_dist_notifications/<int:id>/',fetchDistNotifications),
    path('distributor_notification_overview/<int:id>/',getDistributorNotificationOverview),
    path('accept_dmodule_updation_request/', distributorModuleUpdationAccept),
    path('reject_dmodule_updation_request/', distributorModuleUpdationReject),

    # Company
    path('check_payment_term/<int:id>/',checkCompanyPaymentTerms),
    path('get_modules/<int:id>/',getModules),
    path('get_profile_data/<int:id>/',getProfileData),
    path('get_staff_requests/<int:id>/',getStaffRequests),
    path('get_all_staffs/<int:id>/',getAllStaffs),
    path('Staff_Req_Accept/<int:id>/',staffRequestAccept),
    path('Staff_Req_Reject/<int:id>/',staffRequestReject),
    path('edit_company_profile/',editCompanyProfile),
    path('edit_staff_profile/',editStaffProfile),
    path('edit_gsttype/',company_gsttype_change),
    path('Change_payment_terms/',changeCompanyPaymentTerm),
    path('Edit_Modules/',editModules),
    path('fetch_notifications/<int:id>/',fetchNotifications),
]