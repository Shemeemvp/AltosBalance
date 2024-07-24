import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import Cookies from "js-cookie";
import {jwtDecode} from "jwt-decode";

const AdminPrivateRoutes = () => {
  const accessToken = Cookies.get("access") || "";

  if (accessToken === "") {
    return <Navigate to="/" />;
  }

  try {
    const decodedToken = jwtDecode(accessToken);
    console.log("Decoded Token:", decodedToken); // Debugging line

    // Adjust the field name based on your token structure
    const is_staff = decodedToken.user_is_staff !== undefined ? decodedToken.user_is_staff : decodedToken.is_staff;

    if (typeof is_staff === 'undefined') {
      console.error("Token does not contain is_staff or user_is_staff field");
      return <Navigate to="/" />;
    }

    const currentTime = Date.now() / 1000;

    if (decodedToken.exp < currentTime) {
      // Token has expired
      return <Navigate to="/" />;
    }

    return is_staff ? <Outlet /> : <Navigate to="/" />;
  } catch (error) {
    // Error decoding token or other issues
    console.error("Error decoding token:", error);
    return <Navigate to="/" />;
  }
};

export default AdminPrivateRoutes;
