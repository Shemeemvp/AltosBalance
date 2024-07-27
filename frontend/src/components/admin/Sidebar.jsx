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
      { path: "/apps", state: "appsMenuOpen" },
      { path: "/basic-ui", state: "basicUiMenuOpen" },
      { path: "/advanced-ui", state: "advancedUiMenuOpen" },
      { path: "/form-elements", state: "formElementsMenuOpen" },
      { path: "/tables", state: "tablesMenuOpen" },
      { path: "/maps", state: "mapsMenuOpen" },
      { path: "/icons", state: "iconsMenuOpen" },
      { path: "/charts", state: "chartsMenuOpen" },
      { path: "/user-pages", state: "userPagesMenuOpen" },
      { path: "/error-pages", state: "errorPagesMenuOpen" },
      { path: "/general-pages", state: "generalPagesMenuOpen" },
      { path: "/ecommerce", state: "ecommercePagesMenuOpen" },
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
    <nav className="sidebar" id="sidebar">
      <ul className="nav">
        <li
          className={
            isPathActive("/dashboard") ? "nav-item active" : "nav-item"
          }
        >
          <Link className="nav-link" to="/dashboard">
            <span className="menu-title">
              <Trans>Dashboard</Trans>
            </span>
            <i className="mdi mdi-home menu-icon"></i>
          </Link>
        </li>
        <li
          className={isPathActive("/basic-ui") ? "nav-item active" : "nav-item"}
        >
          <div
            className={
              menuState.basicUiMenuOpen ? "nav-link menu-expanded" : "nav-link"
            }
            onClick={() => toggleMenuState("basicUiMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>Basic UI Elements</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-crosshairs-gps menu-icon"></i>
          </div>
          <Collapse in={menuState.basicUiMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/basic-ui/buttons")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/basic-ui/buttons"
                >
                  <Trans>Buttons</Trans>
                </Link>
              </li>
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/basic-ui/dropdowns")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/basic-ui/dropdowns"
                >
                  <Trans>Dropdowns</Trans>
                </Link>
              </li>
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/basic-ui/typography")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/basic-ui/typography"
                >
                  <Trans>Typography</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li
          className={
            isPathActive("/form-elements") ? "nav-item active" : "nav-item"
          }
        >
          <div
            className={
              menuState.formElementsMenuOpen
                ? "nav-link menu-expanded"
                : "nav-link"
            }
            onClick={() => toggleMenuState("formElementsMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>Form Elements</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-format-list-bulleted menu-icon"></i>
          </div>
          <Collapse in={menuState.formElementsMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/form-elements/basic-elements")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/form-elements/basic-elements"
                >
                  <Trans>Basic Elements</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li
          className={isPathActive("/tables") ? "nav-item active" : "nav-item"}
        >
          <div
            className={
              menuState.tablesMenuOpen ? "nav-link menu-expanded" : "nav-link"
            }
            onClick={() => toggleMenuState("tablesMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>Tables</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-table-large menu-icon"></i>
          </div>
          <Collapse in={menuState.tablesMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/tables/basic-table")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/tables/basic-table"
                >
                  <Trans>Basic Table</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li className={isPathActive("/icons") ? "nav-item active" : "nav-item"}>
          <div
            className={
              menuState.iconsMenuOpen ? "nav-link menu-expanded" : "nav-link"
            }
            onClick={() => toggleMenuState("iconsMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>Icons</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-contacts menu-icon"></i>
          </div>
          <Collapse in={menuState.iconsMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/icons/mdi") ? "nav-link active" : "nav-link"
                  }
                  to="/icons/mdi"
                >
                  <Trans>Material</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li
          className={isPathActive("/charts") ? "nav-item active" : "nav-item"}
        >
          <div
            className={
              menuState.chartsMenuOpen ? "nav-link menu-expanded" : "nav-link"
            }
            onClick={() => toggleMenuState("chartsMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>Charts</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-chart-bar menu-icon"></i>
          </div>
          <Collapse in={menuState.chartsMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/charts/chart-js")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/charts/chart-js"
                >
                  <Trans>Chart Js</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li
          className={
            isPathActive("/user-pages") ? "nav-item active" : "nav-item"
          }
        >
          <div
            className={
              menuState.userPagesMenuOpen
                ? "nav-link menu-expanded"
                : "nav-link"
            }
            onClick={() => toggleMenuState("userPagesMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>User Pages</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-lock menu-icon"></i>
          </div>
          <Collapse in={menuState.userPagesMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/user-pages/login-1")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/user-pages/login-1"
                >
                  <Trans>Login</Trans>
                </Link>
              </li>
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/user-pages/register-1")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/user-pages/register-1"
                >
                  <Trans>Register</Trans>
                </Link>
              </li>
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/user-pages/lockscreen")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/user-pages/lockscreen"
                >
                  <Trans>Lockscreen</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li
          className={
            isPathActive("/error-pages") ? "nav-item active" : "nav-item"
          }
        >
          <div
            className={
              menuState.errorPagesMenuOpen
                ? "nav-link menu-expanded"
                : "nav-link"
            }
            onClick={() => toggleMenuState("errorPagesMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>Error Pages</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-security menu-icon"></i>
          </div>
          <Collapse in={menuState.errorPagesMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/error-pages/error-404")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/error-pages/error-404"
                >
                  404
                </Link>
              </li>
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/error-pages/error-500")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/error-pages/error-500"
                >
                  500
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li
          className={
            isPathActive("/general-pages") ? "nav-item active" : "nav-item"
          }
        >
          <div
            className={
              menuState.generalPagesMenuOpen
                ? "nav-link menu-expanded"
                : "nav-link"
            }
            onClick={() => toggleMenuState("generalPagesMenuOpen")}
            data-toggle="collapse"
          >
            <span className="menu-title">
              <Trans>General Pages</Trans>
            </span>
            <i className="menu-arrow"></i>
            <i className="mdi mdi-medical-bag menu-icon"></i>
          </div>
          <Collapse in={menuState.generalPagesMenuOpen}>
            <ul className="nav flex-column sub-menu">
              <li className="nav-item">
                {" "}
                <Link
                  className={
                    isPathActive("/general-pages/blank-page")
                      ? "nav-link active"
                      : "nav-link"
                  }
                  to="/general-pages/blank-page"
                >
                  <Trans>Blank Page</Trans>
                </Link>
              </li>
            </ul>
          </Collapse>
        </li>
        <li className="nav-item">
          <a
            className="nav-link"
            href="http://bootstrapdash.com/demo/purple-react-free/documentation/documentation.html"
            rel="noopener noreferrer"
            target="_blank"
          >
            <span className="menu-title">
              <Trans>Documentation</Trans>
            </span>
            <i className="mdi mdi-file-document-box menu-icon"></i>
          </a>
        </li>
      </ul>
    </nav>
  );
};

export default Sidebar;
