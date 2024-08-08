import React, { useEffect, useState } from "react";
import { Dropdown } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import { Trans } from "react-i18next";
import "./styles/Navbar.css";
import "bootstrap/dist/css/bootstrap.css";
import logo from "../../assets/images/logo.svg";
import Cookies from "js-cookie";
import axios from "axios";
import config from "../../functions/config";

const Navbar = () => {
  const navigate = useNavigate();

  const [showFullLogo, setShowFullLogo] = useState(true);

  const toggleOffcanvas = () => {
    document.querySelector(".sidebar-offcanvas").classList.toggle("active");
  };

  function toggleSidebar() {
    document.body.classList.toggle("sidebar-icon-only");
    setShowFullLogo(!showFullLogo);
  }

  const toggleRightSidebar = () => {
    document.querySelector(".right-sidebar").classList.toggle("open");
  };

  const [noti, setNoti] = useState(false);
  const [notification, setNotification] = useState([]);

  const fetchNotifications = () => {
    axios
      .get(`${config.base_url}/fetch_admin_notifications/`)
      .then((res) => {
        if (res.data.status) {
          var ntfs = res.data.notifications;
          setNoti(res.data.status);
          setNotification([]);
          ntfs.map((i) => {
            var obj = {
              title: i.title,
              desc: i.description,
              date: i.date_created,
              time: i.time,
            };
            setNotification((prevState) => [...prevState, obj]);
          });
        }
      })
      .catch((err) => {
        console.log("ERROR", err);
      });
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  function handleLogout() {
    Cookies.remove("role");
    Cookies.remove("user_id");
    Cookies.remove("access");
    Cookies.remove("refresh");
    navigate("/");
  }

  function formatTimeInput(timeString) {
    let [hours, minutes] = timeString.split(":").slice(0, 2);

    hours = parseInt(hours, 10);

    let meridiem = hours >= 12 ? "PM" : "AM";
    hours = hours % 12 || 12; // Handle midnight (0) and noon (12)

    hours = String(hours).padStart(2, "0");
    minutes = String(minutes).padStart(2, "0");

    return `${hours}:${minutes} ${meridiem}`;
  }

  return (
    <nav className="admin-nav navbar col-lg-12 col-12 p-0 fixed-top d-flex flex-row justify-content-between">
      <div className="text-center navbar-brand-wrapper d-flex align-items-center justify-content-center">
        {showFullLogo ? (
          <Link
            className="navbar-brand brand-logo pl-4 d-lg-block d-none"
            to="/admin_home"
          >
            <h2 className="text-muted">AltosBalance</h2>
          </Link>
        ) : (
          <Link
            className="navbar-brand brand-logo pl-4 d-lg-block d-none"
            to="/admin_home"
          >
            <h2 className="text-muted">AB</h2>
          </Link>
        )}
        <Link
          className="navbar-brand brand-logo-mini d-block d-lg-none pl-4"
          to="/"
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
            <li className="nav-item dropdown dropdown-lg">
              <a
                className="nav-link dropdown-toggle dropdown-toggle-nocaret position-relative notification-dropdown-button"
                href="javascript:;"
                data-toggle="dropdown"
              >
                <i
                  className="mdi mdi-bell-outline vertical-align-middle"
                  style={{ fontSize: "25px", color: "grey" }}
                ></i>
                <span className="msg-count">{notification.length}</span>
              </a>
              <div className="dropdown-menu dropdown-menu-right position-absolute noti-drop-menu">
                <a className="p-0" href="javascript:;">
                  <div className="noti-msg-header w-100">
                    <h6 className="noti-msg-header-title font-weight-bold">
                      {notification.length} New
                    </h6>
                    <p className="noti-msg-header-subtitle">
                      Application Notifications
                    </p>
                  </div>
                </a>
                <div className="header-notifications-list">
                  {noti ? (
                    <>
                      {notification.map((item) => (
                        <Link
                          className="dropdown-item w-100 noti-item"
                          to="/admin_notifications"
                        >
                          <div className="media align-items-center w-100">
                            <div className="media-body">
                              <h6 className="msg-name w-100 mb-0">
                                {item.title}
                                <p className="msg-time m-0" style={{fontSize:"0.7rem"}}>
                                  {item.date} {formatTimeInput(item.time)}
                                </p>
                              </h6>
                              <p className="msg-info">{item.desc}</p>
                            </div>
                          </div>
                        </Link>
                      ))}
                      <Link
                        className="w-100 justify-content-center"
                        to="/admin_notifications"
                      >
                        <p className="msg-info text-center">
                          View All Notifications
                        </p>
                      </Link>
                    </>
                  ) : (
                    <p className="msg-info text-center mt-5">
                      Notifications is not found
                    </p>
                  )}
                </div>
              </div>
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
                      <Trans>Admin</Trans>
                    </p>
                  </div>
                </Dropdown.Toggle>
                <Dropdown.Menu className="navbar-dropdown">
                  <Dropdown.Item onClick={() => navigate("/admin_home")}>
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
