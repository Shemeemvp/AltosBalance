import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import Cookies from "js-cookie";
import { jwtDecode } from "jwt-decode";

const CompanyStaffPrivateRoutes = () => {
  const accessToken = Cookies.get("access") || "";
  const role = Cookies.get("role") || "";

  if (accessToken === "") {
    return <Navigate to="/" />;
  }

  try {
    const decodedToken = jwtDecode(accessToken);
    // console.log("Decoded Token:", decodedToken);

    // Adjust the field name based on your token structure
    // const is_admin = decodedToken.user_is_staff !== undefined ? decodedToken.user_is_staff : decodedToken.is_staff
    var is_company_staff = false;
    if (role == "Company" || role == "Staff") {
      is_company_staff = true;
    }
    return is_company_staff ? <Outlet /> : <Navigate to="/" />;
  } catch (error) {
    // Error decoding token or other issues
    console.error("Error decoding token:", error);
    return <Navigate to="/" />;
  }
};

export default CompanyStaffPrivateRoutes;
