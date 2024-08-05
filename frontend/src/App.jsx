import { BrowserRouter, Routes, Route } from "react-router-dom";
import AdminPrivateRoutes from "./components/routes/AdminPrivateRoutes";
import Index from "./components/index/Index";
import SignIn from "./components/SignIn/SignIn";
import AdminHome from "./components/admin/AdminHome";
import CompanyReg from "./components/company/CompanyReg";
import PaymentTerms from "./components/admin/PaymentTerms";
import CompanyReg2 from "./components/company/CompanyReg2";
import Modules from "./components/company/Modules";
import StaffReg from "./components/staff/StaffReg";
import StaffReg2 from "./components/staff/StaffReg2";
import DistributorReg from "./components/distributor/DistributorReg";
import DistributorReg2 from "./components/distributor/DistributorReg2";
import AllClients from "./components/admin/AllClients";
import Clients from "./components/admin/Clients";
import ClientsReq from "./components/admin/ClientsReq";
import Distributors from "./components/admin/Distributors";
import AllDistributors from "./components/admin/AllDistributors";
import DistributorsReq from "./components/admin/DistributorsReq";
import DistributorReqOverview from "./components/admin/DistributorReqOverview";
import ClientReqOverview from "./components/admin/ClientReqOverview";
import AllDistributorsOverview from "./components/admin/AllDistributorsOverview";
import AllClientsOverview from "./components/admin/AllClientsOverview";
import DistributorPrivateRoutes from "./components/routes/DistributorPrivateRoutes";
import DistributorHome from "./components/distributor/DistributorHome";
import DAllClients from "./components/distributor/DAllClients";
import DClientReq from "./components/distributor/DClientReq";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />}></Route>
          <Route path="/login" element={<SignIn />}></Route>
          <Route path="/company_registration" element={<CompanyReg />}></Route>
          <Route path="/company_registration2" element={<CompanyReg2 />}></Route>
          <Route path="/modules_list" element={<Modules />}></Route>
          {/* <Route path="/wrong" element={<Wrong />}></Route> */}
          {/* <Route path="/term_update_modules" element={<TermUpdateModules />}></Route> */}

          <Route path="/distributor_registration" element={<DistributorReg />}></Route>
          <Route path="/distributor_registration2" element={<DistributorReg2 />}></Route>
          
          <Route path="/staff_registration" element={<StaffReg />}></Route>
          <Route path="/staff_registration2" element={<StaffReg2 />}></Route>

          <Route element={<AdminPrivateRoutes />}>
            <Route path="/admin_home" element={<AdminHome />}></Route>
            <Route path="/payment_terms/new_term" element={<PaymentTerms />}></Route>
            <Route path="/clients" element={<Clients />}></Route>
            <Route path="/all_clients" element={<AllClients />}></Route>
            <Route path="/clients_requests" element={<ClientsReq />}></Route>
            <Route path="/client_request_overview/:id/" element={<ClientReqOverview />}></Route>
            <Route path="/all_clients_overview/:id/" element={<AllClientsOverview />}></Route>
            <Route path="/distributors" element={<Distributors />}></Route>
            <Route path="/all_distributors" element={<AllDistributors />}></Route>
            <Route path="/distributors_requests" element={<DistributorsReq />}></Route>
            <Route path="/distributors_request_overview/:id/" element={<DistributorReqOverview />}></Route>
            <Route path="/all_distributors_overview/:id/" element={<AllDistributorsOverview />}></Route>

          </Route>
          <Route element={<DistributorPrivateRoutes />}>
            <Route path="/distributor_home" element={<DistributorHome />}></Route>
            {/* <Route path="/distributor_notifications" element={<DistNotifications />}></Route> */}
            {/* <Route path="/distributor_profile" element={<DistributorProfile />}></Route> */}
            {/* <Route path="/edit_distributor_profile" element={<DistributorProfileEdit />}></Route> */}
            <Route path="/DClient_req" element={<DClientReq />}></Route>
            <Route path="/DClients" element={<DAllClients />}></Route>
            {/* <Route path="/DClient_request_overview/:id/" element={<DClientReqOverview />}></Route> */}
            {/* <Route path="/DClient_overview/:id/" element={<DClientOverview />}></Route> */}
            {/* <Route path="/dnotification_overview/:id/" element={<DistNotificationOverview />}></Route> */}
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
