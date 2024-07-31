import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";
import "./styles/Layout.css";
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
    const body = document.querySelector("body");
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
      <div className="container-fluid page-body-wrapper d-flex">
        {!isFullPageLayout && <Sidebar />}
        <div className="main-panel px-3 py-2" style={{background:"#a9a9a961"}}>
          <div className="content-wrapper">
            <div
              className="body-wrapper p-3"
              style={{ height: "100vh" }}
            >
              <div className="container-fluid">
                <div className="row p-3">
                  <div className="col-md-4">
                    <div className="card radius-15 p-3 border-0" style={{background:"#f4f5f7"}}>
                      <Link to="/distributors">
                        <div className="card-body">
                          <div className="card-title"></div>
                          <div className="row">
                            <div className="col-md-9">
                              <h5 className="card-title mb-9 fw-semibold">
                                <b className="text-secondary">DISTRIBUTORS</b>
                              </h5>
                            </div>
                            <div className="col">
                              <i
                                className="fa fa-users text-secondary"
                                style={{ fontSize: "2em" }}
                              ></i>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className="card radius-15 p-3 border-0" style={{background:"#f4f5f7"}}>
                      <Link to="/clients">
                        <div className="card-body">
                          <div className="card-title"></div>
                          <div className="row">
                            <div className="col-md-9">
                              <h5 className="card-title mb-9 fw-semibold">
                                <b className="text-secondary">CLIENTS</b>
                              </h5>
                            </div>
                            <div className="col">
                              <i
                                className="fa fa-users text-secondary"
                                style={{ fontSize: "2em" }}
                              ></i>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </div>
                  </div>
                  <div className="col-md-4"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminHome;
