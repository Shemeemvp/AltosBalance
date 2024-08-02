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
            <Route path="/distributors" element={<Distributors />}></Route>
            <Route path="/all_distributors" element={<AllDistributors />}></Route>
            <Route path="/distributors_requests" element={<DistributorsReq />}></Route>

          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
