import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import './styles/Layout.css'
// import { useTranslation } from "react-i18next";

function AdminHome() {
    const [isFullPageLayout, setIsFullPageLayout] = useState(false);
  const location = useLocation();
//   const { i18n } = useTranslation();

  useEffect(() => {
    onRouteChanged();
  }, [location]);

  const onRouteChanged = () => {
    console.log("ROUTE CHANGED");
    const body = document.querySelector('body');
    // if (location.pathname === '/layout/RtlLayout') {
    //   body.classList.add('rtl');
    //   i18n.changeLanguage('ar');
    // } else {
    //   body.classList.remove('rtl');
    //   i18n.changeLanguage('en');
    // }
    window.scrollTo(0, 0);

    // const fullPageLayoutRoutes = [
    //   '/user-pages/register-1', 
    //   '/user-pages/lockscreen', 
    //   '/error-pages/error-404', 
    //   '/error-pages/error-500', 
    //   '/general-pages/landing-page'
    // ];

    // if (fullPageLayoutRoutes.includes(location.pathname)) {
    //   setIsFullPageLayout(true);
    //   document.querySelector('.page-body-wrapper').classList.add('full-page-wrapper');
    // } else {
    //   setIsFullPageLayout(false);
    //   document.querySelector('.page-body-wrapper').classList.remove('full-page-wrapper');
    // }
  };
  return (
    <div className="container-scroller">
      {!isFullPageLayout && <Navbar />}
      <div className="container-fluid page-body-wrapper">
        {!isFullPageLayout && <Sidebar />}
        <div className="main-panel">
          <div className="content-wrapper">
            <h1>ADMIN HOME</h1>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdminHome
