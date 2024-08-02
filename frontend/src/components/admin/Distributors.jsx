import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function Distributors() {
  return (
    <div className="container-scroller">
      <Navbar />
      <div className="container-fluid page-body-wrapper d-flex">
        <Sidebar />
        <div
          className="main-panel px-3 py-2"
          style={{ background: "#a9a9a961" }}
        >
          <div className="content-wrapper">
            <div className="body-wrapper p-3" style={{ height: "100vh" }}>
              <div className="container-fluid">
                <div className="row p-4">
                  <div className="col-md-4">
                    <div className="card radius-15 p-3 mb-0 h-100">
                      <Link to="/distributors_requests">
                        <div className="card-body">
                          <div className="card-title"></div>
                          <div className="row">
                            <div className="col-md-9">
                              <h5 className="card-title mb-9 fw-semibold">
                                <b className="text-secondary">DISTRIBUTOR REQUESTS</b>
                              </h5>
                            </div>
                            <div className="col-md-3">
                              <i
                                className="fa fa-user-plus text-secondary"
                                style={{ fontSize: "2.5em" }}
                              ></i>
                            </div>
                          </div>
                        </div>
                      </Link>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className="card radius-15 p-3 mb-0 h-100">
                      <Link to="/all_distributors">
                        <div className="card-body">
                          <div className="card-title"></div>
                          <div className="row">
                            <div className="col-md-9">
                              <h5 className="card-title mb-9 fw-semibold">
                                <b className="text-secondary">ALL DISTRIBUTORS</b>
                              </h5>
                            </div>
                            <div className="col-md-3">
                              <i
                                className="fa fa-users text-secondary"
                                style={{ fontSize: "2.5em" }}
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

export default Distributors;
