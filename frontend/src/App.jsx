import { BrowserRouter, Routes, Route } from "react-router-dom";
import AdminPrivateRoutes from "./components/routes/AdminPrivateRoutes";
import Index from "./components/index/Index";
import SignIn from "./components/SignIn/SignIn";
import AdminHome from "./components/admin/AdminHome";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />}></Route>
          <Route path="/login" element={<SignIn />}></Route>
          {/* <Route path="/company_registration" element={<CompanyReg />}></Route>
          <Route path="/Company_Registration2" element={<CompanyReg2 />}></Route>
          <Route path="/modules_list" element={<Modules />}></Route>
          <Route path="/wrong" element={<Wrong />}></Route>
          <Route path="/term_update_modules" element={<TermUpdateModules />}></Route>

          <Route path="/distributor_registration" element={<DistributorReg />}></Route>
          <Route path="/distributor_registration2" element={<DistributorReg2 />}></Route>
          
          <Route path="/staff_registration" element={<StaffReg />}></Route>
          <Route path="/staff_registration2" element={<StaffReg2 />}></Route> */}

          <Route element={<AdminPrivateRoutes />}>
            <Route path="/admin_home" element={<AdminHome />}></Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
