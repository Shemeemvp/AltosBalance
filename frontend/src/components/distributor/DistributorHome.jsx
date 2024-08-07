import React, { useState, useEffect } from "react";
import Cookies from "js-cookie";
import axios from "axios";
import config from "../../functions/config";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function DistributorHome() {
  const navigate = useNavigate();
  const [paymentDetails, setPaymentDetails] = useState({
    PaymentRequest: false,
    daysLeft: 0,
    endDate: "",
    alertMessage: false,
  });
  const ID = Cookies.get("user_id");
  const user = Cookies.get("role");
  function fetchPaymentDetails() {
    axios
      .get(`${config.base_url}/check_distributor_payment_term/${ID}/`)
      .then((res) => {
        if (res.data.status) {
          console.log(res.data)
          const pData = {
            PaymentRequest: res.data.payment_request,
            daysLeft: res.data.days_left,
            endDate: res.data.endDate,
            alertMessage: res.data.alert_message,
          };
          setPaymentDetails(pData);
          showModal(res.data.alert_message);
        }
      })
      .catch((err) => {
        console.log(err)
      });
  }

  function showModal(status) {
    setTimeout(() => {
      if (status) {
        try {
          document.getElementById("modalBtn").click();
        } catch (error) {}
      }
    }, 2000);
  }

  useEffect(() => {
    fetchPaymentDetails();
  }, []);

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
                  <div className="col"></div>
                  <div className="col-md-5">
                    <div className="card radius-15 p-3">
                      <Link to="/DClient_req">
                        <div className="card-body">
                          <div className="card-title"></div>
                          <div className="row">
                            <div className="col-md-9">
                              <h5 className="card-title mb-9 fw-semibold">
                                <b className="text-secondary">CLIENT REQUESTS</b>
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
                  <div className="col-md-5">
                    <div className="card radius-15 p-3">
                      <Link to="/DClients">
                        <div className="card-body">
                          <div className="card-title"></div>
                          <div className="row">
                            <div className="col-md-9">
                              <h5 className="card-title mb-9 fw-semibold">
                                <b className="text-secondary">ALL CLIENTS</b>
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
                  <div className="col"></div>
                </div>
              </div>
              <button
                style={{ visibility: "hidden" }}
                id="modalBtn"
                data-toggle="modal"
                data-target="#myModal"
              ></button>
            </div>
            {!paymentDetails.PaymentRequest &&
              (paymentDetails.alertMessage ? (
                <>
                  <div
                    className="modal fade"
                    id="myModal"
                    tabindex="-1"
                    role="dialog"
                  >
                    <div className="modal-dialog" role="document">
                      <div
                        className="modal-content"
                        style={{
                          backgroundColor: "rgb(209 209 209)",
                          border: "1px solid rgba(255, 255, 255, 0.3)",
                        }}
                      >
                        <div className="modal-header">
                          <h5
                            className="modal-title"
                            id="exampleModalLongTitle"
                          >
                            <i className="fa fa-exclamation-triangle fa-lg text-danger ms-1"></i>
                            <span className="font-monospace">
                              Payment Term Ends
                              {paymentDetails.daysLeft != 0 ? (
                                <span className="text-danger">
                                  in {paymentDetails.daysLeft} days
                                </span>
                              ) : (
                                <span className="text-danger">Today</span>
                              )}
                            </span>
                          </h5>
                          <button
                            type="button"
                            className="close"
                            data-dismiss="modal"
                            aria-label="Close"
                          >
                            <span aria-hidden="true">&times;</span>
                          </button>
                        </div>

                        <div className="modal-body">
                          <h6 className="text-secondary mt-1 ">
                            Your current plan is expiring on{" "}
                            {paymentDetails.endDate}
                          </h6>
                          <div className="row mb-3 mt-3 w-100 d-flex justify-content-center">
                            <button
                              className="btn btn-sm btn-success"
                              data-dismiss="modal"
                              onClick={() => navigate("/distributor_profile")}
                            >
                              <small>click to renew</small>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </>
              ) : null)}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DistributorHome;
