import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { Collapse } from "react-bootstrap";
import { Trans } from "react-i18next";
import './styles/Sidebar.css'

const Sidebar = () => {
  const [menuState, setMenuState] = useState({});
  const location = useLocation();

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
      { path: "/distributor_home", state: "appsMenuOpen" },
      { path: "/payment_terms", state: "paymentTermsMenuOpen" },
      { path: "/trial_periods", state: "trialPeriodMenuOpen" },
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
            isPathActive("/distributor_home") ? "nav-item active" : "nav-item"
          }
        >
          <Link className="nav-link" to="/distributor_home">
            <span className="menu-title">
              <Trans>Dashboard</Trans>
            </span>
            <i className="mdi mdi-home menu-icon mb-0"></i>
          </Link>
        </li>
        <li
          className={isPathActive("/trial_periods") ? "nav-item active" : "nav-item"}
        >
          <div
            className={
              menuState.trialPeriodMenuOpen ? "nav-link menu-expanded" : "nav-link"
            }
            onClick={() => toggleMenuState("trialPeriodMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>Trial Periods</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-table-large menu-icon mb-0"></i>
          </div>
          <Collapse in={menuState.trialPeriodMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/trial_periods/trial_periods")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/trial_periods/trial_periods"
                >
                  <Trans>Trial Periods</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
      </ul>
    </nav>
  );
};

export default Sidebar;