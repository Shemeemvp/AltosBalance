import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Collapse } from "react-bootstrap";
import { Trans } from "react-i18next";
import "./styles/Sidebar.css";
import Cookies from "js-cookie";
import config from "../../functions/config";
import axios from "axios";

const Sidebar = () => {
  const [menuState, setMenuState] = useState({});
  const location = useLocation();

  const ID = Cookies.get("user_id");

  const user = Cookies.get("role");
  var is_company = false;
  if (user === "Company") {
    is_company = true;
  }

  const [modules, setModules] = useState({});

  const fetchModules = () => {
    axios
      .get(`${config.base_url}/get_modules/${ID}/`)
      .then((res) => {
        if (res.data.status) {
          const modules = res.data.modules;

          setModules(modules);
        }
      })
      .catch((err) => {
        console.log("MODULES ERROR==", err);
      });
  };

  useEffect(() => {
    fetchModules();
  }, []);

  const toggleMenuState = (menu) => {
    setMenuState((prevState) => {
      const newState = { ...prevState };
      Object.keys(newState).forEach((key) => {
        newState[key] = false;
      });
      newState[menu] = !prevState[menu];
      return newState;
    });
  };

  const onRouteChanged = () => {
    document.querySelector("#sidebar").classList.remove("active");
    setMenuState({});

    const dropdownPaths = [
      { path: "/company_home", state: "appsMenuOpen" },
      { path: "/company_staffs", state: "companyStaffMenuOpen" },
    ];

    dropdownPaths.forEach((obj) => {
      if (isPathActive(obj.path)) {
        setMenuState((prevState) => ({ ...prevState, [obj.state]: true }));
      }
    });
  };

  useEffect(() => {
    onRouteChanged();
    const body = document.querySelector("body");
    document.querySelectorAll(".sidebar .nav-item").forEach((el) => {
      el.addEventListener("mouseover", function () {
        if (body.classList.contains("sidebar-icon-only")) {
          el.classList.add("hover-open");
        }
      });
      el.addEventListener("mouseout", function () {
        if (body.classList.contains("sidebar-icon-only")) {
          el.classList.remove("hover-open");
        }
      });
    });
  }, [location]);

  const isPathActive = (path) => {
    return location.pathname.startsWith(path);
  };

  return (
    <nav className="sidebar sidebar-offcanvas" id="sidebar">
      <ul className="nav">
        <li
          className={
            isPathActive("/company_home") ? "nav-item active" : "nav-item"
          }
        >
          <Link className="nav-link" to="/company_home">
            <span className="menu-title">
              <Trans>Dashboard</Trans>
            </span>
            <i className="mdi mdi-home menu-icon mb-0"></i>
          </Link>
        </li>
        {is_company ? (
          <li
            className={
              isPathActive("/company_staffs") ? "nav-item active" : "nav-item"
            }
          >
            <div
              className={
                menuState.companyStaffMenuOpen
                  ? "nav-link menu-expanded"
                  : "nav-link"
              }
              onClick={() => toggleMenuState("companyStaffMenuOpen")}
              data-toggle="collapse"
            >
              <span className="menu-title">
                <Trans>Staff</Trans>
              </span>
              <i className="menu-arrow"></i>
              <i className="mdi mdi-account menu-icon mb-0"></i>
            </div>
            <Collapse in={menuState.companyStaffMenuOpen}>
              <ul className="nav flex-column sub-menu">
                <li className="nav-item">
                  {" "}
                  <Link
                    className={
                      isPathActive("/company_staffs/staff_requests")
                        ? "nav-link active"
                        : "nav-link"
                    }
                    to="/company_staffs/staff_requests"
                  >
                    <Trans>Staff Request</Trans>
                  </Link>
                </li>
                <li className="nav-item">
                  {" "}
                  <Link
                    className={
                      isPathActive("/company_staffs/all_staffs")
                        ? "nav-link active"
                        : "nav-link"
                    }
                    to="/company_staffs/all_staffs"
                  >
                    <Trans>All Staff</Trans>
                  </Link>
                </li>
              </ul>
            </Collapse>
          </li>
        ) : null}
      </ul>
    </nav>
  );
};

export default Sidebar;
