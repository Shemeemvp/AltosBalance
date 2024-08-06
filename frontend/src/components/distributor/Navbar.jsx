import React, { useState } from "react";
import { Dropdown } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { Trans, useSSR } from "react-i18next";
import "./styles/Navbar.css";
import "bootstrap/dist/css/bootstrap.css";
import Cookies from "js-cookie";

const Navbar = () => {
  const navigate = useNavigate();
  const [showFullLogo, setShowFullLogo] = useState(true);

  const toggleOffcanvas = () => {
    document.querySelector(".sidebar-offcanvas").classList.toggle("active");
    // setShowFullLogo(!showFullLogo)
  };

  function toggleSidebar(){
    document.body.classList.toggle("sidebar-icon-only");
    setShowFullLogo(!showFullLogo);
  }

  const toggleRightSidebar = () => {
    document.querySelector(".right-sidebar").classList.toggle("open");
  };

  function handleLogout() {
    Cookies.remove("role");
    Cookies.remove("user_id");
    Cookies.remove("access");
    Cookies.remove("refresh");
    navigate("/");
  }

  return (
    <nav className="admin-nav navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row justify-content-between">
      <div className="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
        {showFullLogo ? (
          <Link
            className="navbar-brand brand-logo pl-4 d-lg-block d-none"
            to="/distributor_home"
          >
            <h2 className="text-muted">AltosBalance</h2>
          </Link>
        ) : (
          <Link
            className="navbar-brand brand-logo pl-4 d-lg-block d-none"
            to="/distributor_home"
          >
            <h2 className="text-muted">AB</h2>
          </Link>
        )}
        <Link
          className="navbar-brand brand-logo-mini d-block d-lg-none pl-4"
          to="/distributor_home"
        >
          {/* <img src={require("../../assets/images/logo-mini.svg")} alt="logo" /> */}
          <h2 className="text-muted">AB</h2>
        </Link>
      </div>
      <div className="navbar-menu-wrapper d-flex align-items-stretch justify-content-between">
        <div className="left d-flex align-items-center justify-content-start">
          <button
            className="navbar-toggler navbar-toggler align-self-center  d-none d-lg-block"
            type="button"
            onClick={toggleSidebar}
          >
            <span className="mdi mdi-menu"></span>
          </button>
          <div className="search-field d-none d-md-block">
            <form className="d-flex align-items-center h-100" action="#">
              <div className="input-group">
                <div className="input-group-prepend bg-transparent">
                  <i className="input-group-text border-0 mdi mdi-magnify"></i>
                </div>
                <input
                  type="text"
                  className="form-control bg-transparent border-0"
                  placeholder="Search.."
                />
              </div>
            </form>
          </div>
        </div>
        <div className="right pr-5">
          <ul className="navbar-nav navbar-nav-right d-flex flex-row">
            <li className="nav-item ml-2">
              <Dropdown alignRight>
                <Dropdown.Toggle className="nav-link count-indicator navDropButtons">
                  <i className="mdi mdi-bell-outline"></i>
                  <span className="count-symbol bg-danger"></span>
                </Dropdown.Toggle>
                <Dropdown.Menu className="dropdown-menu navbar-dropdown preview-list">
                  <h6 className="p-3 mb-0">
                    <Trans>Notifications</Trans>
                  </h6>
                  <div className="dropdown-divider"></div>
                  <Dropdown.Item
                    className="dropdown-item preview-item"
                    onClick={(evt) => evt.preventDefault()}
                  >
                    <div className="preview-item-content d-flex align-items-start flex-column justify-content-center">
                      <div className="notification_head d-flex align-items-center justify-content-between">
                        <h6 className="preview-subject font-weight-normal mb-1">
                          <Trans>Launch Distributor</Trans>
                        </h6>
                        <span className="ml-5">31-07-2024</span>
                      </div>
                      <p className="text-gray ellipsis mb-0">
                        <Trans>New Distributor wow</Trans>!
                      </p>
                    </div>
                  </Dropdown.Item>
                  <div className="dropdown-divider"></div>
                  <h6 className="p-3 mb-0 text-center cursor-pointer">
                    <Trans>See all notifications</Trans>
                  </h6>
                </Dropdown.Menu>
              </Dropdown>
            </li>
            <li className="nav-item nav-profile ml-5 mr-2">
              <Dropdown alignRight>
                <Dropdown.Toggle className="nav-link d-flex align-items-center navDropButtons">
                  <div className="nav-profile-img">
                    <img
                      src={require("../../assets/images/faces/user-1.jpg")}
                      alt="user"
                    />
                    <span className="availability-status online"></span>
                  </div>
                  <div className="nav-profile-text">
                    <p className="mb-1 text-grey font-weight-bold">
                      <Trans>Distributor</Trans>
                    </p>
                  </div>
                </Dropdown.Toggle>
                <Dropdown.Menu className="navbar-dropdown">
                  <Dropdown.Item onClick={() => navigate("/distributor_home")}>
                    <i className="mdi mdi-account mr-2 text-success"></i>
                    <Trans>Profile</Trans>
                  </Dropdown.Item>
                  <Dropdown.Item onClick={() => navigate("/distributor_home")}>
                    <i className="mdi mdi-home mr-2 text-secondary"></i>
                    <Trans>Dashboard</Trans>
                  </Dropdown.Item>
                  <Dropdown.Item onClick={handleLogout}>
                    <i className="mdi mdi-logout mr-2 text-danger"></i>
                    <Trans>Logout</Trans>
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </li>
            {/* <li className="nav-item nav-settings d-none d-lg-block">
              <button
                type="button"
                className="nav-link border-0"
                onClick={toggleRightSidebar}
              >
                <i className="mdi mdi-format-line-spacing"></i>
              </button>
            </li> */}
          </ul>
        </div>
        <button
          className="navbar-toggler navbar-toggler-right d-lg-none align-self-center"
          type="button"
          onClick={toggleOffcanvas}
        >
          <span className="mdi mdi-menu"></span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
