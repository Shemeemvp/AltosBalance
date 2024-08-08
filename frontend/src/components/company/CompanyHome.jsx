import React, { useEffect, useState } from "react";
import Cookies from "js-cookie";
import axios from "axios";
import config from "../../functions/config";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function CompanyHome() {
  const navigate = useNavigate();
  const [companyName, setCompanyName] = useState("COMPANY NAME");
  const [paymentDetails, setPaymentDetails] = useState({
    PaymentRequest: false,
    daysLeft: 0,
    paymentTerm: false,
    endDate: "",
    alertMessage: false,
  });
  const ID = Cookies.get("user_id");
  const user = Cookies.get("role");
  function fetchCompanyDetails() {
    axios
      .get(`${config.base_url}/check_payment_term/${ID}/`)
      .then((res) => {
        console.log("HOME RESPONSE==", res);
        if (res.data.status) {
          setCompanyName(res.data.companyName);
          if (user === "Company") {
            const pData = {
              PaymentRequest: res.data.payment_request,
              daysLeft: res.data.days_left,
              paymentTerm: res.data.paymentTerm,
              endDate: res.data.endDate,
              alertMessage: res.data.alert_message,
            };
            setPaymentDetails(pData);
            showModal(res.data.alert_message);
          }
        }
      })
      .catch((err) => {
        console.log("HOME ERROR==", err);
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
    fetchCompanyDetails();
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
            <div className="body-wrapper p-3" style={{ minHeight: "100vh" }}>
              <div className="card radius-15">
                <div className="card-body">
                  <div className="card-title">
                    <form method="post">
                      <div className="row w-100">
                        <div className="col"></div>
                        <div className="col">
                          <center className="w-100">
                            <label
                              style={{
                                textAlign: "center",
                                fontSize: "30px",
                                textTransform: "uppercase",
                              }}
                            >
                              <b>{companyName}</b>
                            </label>
                          </center>
                        </div>
                        <div className="col"></div>
                      </div>
                    </form>
                    <hr />
                  </div>
                </div>
              </div>
              {/* <div className="card-deck flex-column flex-lg-row">
                <div className="card radius-15">
                  <div className="card-body">
                    <div className="card-title">
                      <h5 className="mb-0">PROFIT AND LOSS </h5>
                    </div>
                    <hr />
                    <br />
                    <h6 id="pf"></h6>
                    <br />
                    <canvas id="pie-chart"></canvas>
                  </div>
                </div>

                <div className="card radius-15">
                  <div className="card-body">
                    <div className="card-title">
                      <h5 className="mb-0">EXPENSES: &#8377 {"EXP"} </h5>
                    </div>
                    <hr />
                    <div id="chartexp"></div>
                  </div>
                </div>

                <div className="card radius-15">
                  <div className="card-body">
                    <div className="card-title">
                      <h5 className="mb-0">BANK ACCOUNTS </h5>
                    </div>
                    <hr />
                  </div>
                </div>
              </div> */}

              {/* <div className="card-deck flex-column flex-lg-row">
                <div className="card radius-15">
                  <div className="card-body">
                    <div className="card-title">
                      <h5 className="mb-0">INCOME: &#8377 {"inc"} </h5>
                    </div>
                    <hr />
                    <div id="chartinc"></div>
                  </div>
                </div>
                <div className="card radius-15">
                  <div className="card-body">
                    <div className="card-title">
                      <h5 className="mb-0">INVOICE </h5>
                    </div>
                    <hr />
                    <br />
                    <h6>UNPAID:&#8377 {"up"}</h6>
                    <h6>PAID:&#8377 {"p"}</h6>

                    <br />
                    <canvas id="pie-chart5"></canvas>
                  </div>
                </div>

                <div className="card radius-15">
                  <div className="card-body">
                    <div className="card-title">
                      <h5 className="mb-0">SALES: &#8377 {"s"} </h5>
                    </div>
                    <hr />

                    <canvas id="pie-chart12"></canvas>
                  </div>
                </div>
              </div> */}
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
                            <i className="fa fa-exclamation-triangle fa-lg text-danger ml-1"></i>
                            <span className="font-monospace">
                              {paymentDetails.paymentTerm
                                ? "Payment Term Ends in"
                                : "Trial Period Ends in"}

                              {paymentDetails.daysLeft != 0 ? (
                                <span className="text-danger">
                                  {" "}
                                  {paymentDetails.daysLeft} days
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

                        {paymentDetails.paymentTerm ? (
                          <div className="modal-body">
                            <h6 className="text-secondary mt-1 ">
                              Your current plan is expiring on{" "}
                              {paymentDetails.endDate}
                            </h6>
                            <div className="row mb-3 mt-3">
                              <div className="col-md-4"></div>
                              <div className="col-md-4"></div>
                              <div className="col-md-4">
                                <button
                                  className="btn btn-sm btn-success ms-5"
                                  data-dismiss="modal"
                                  onClick={()=>navigate('/company_profile')}
                                >
                                  <small>click to renew</small>
                                </button>
                              </div>
                            </div>
                          </div>
                        ) : (
                          <div className="modal-body">
                            <form
                              className="w-100 px-1"
                            >
                              <div className="row w-100">
                                <div className="w-100">
                                  <p className="text-secondary">
                                    Do you want to continue with our services?
                                  </p>
                                </div>
                                <div className="d-flex w-100">
                                  <div className="form-check form-check-inline">
                                    <input
                                      className="form-check-input bg-white form-control"
                                      type="radio"
                                      name="interested"
                                      id="inlineRadio1"
                                      value="yes"
                                      required
                                    />
                                    <label
                                      className="form-check-label text-secondary"
                                      for="inlineRadio1"
                                    >
                                      Yes
                                    </label>
                                  </div>
                                  <div className="form-check form-check-inline">
                                    <input
                                      className="form-check-input bg-white form-control"
                                      type="radio"
                                      name="interested"
                                      id="inlineRadio2"
                                      value="no"
                                      required
                                    />
                                    <label
                                      className="form-check-label text-secondary"
                                      for="inlineRadio2"
                                    >
                                      No
                                    </label>
                                  </div>
                                </div>
                                <textarea
                                  className="mt-3 mb-3 rounded text-dark form-control"
                                  name="feedback"
                                  cols="62"
                                  rows="3"
                                  placeholder="Please give feedback..."
                                ></textarea>
                              </div>
                              <div className="row w-100">
                                <center className="w-100">
                                  <button
                                    type="submit"
                                    className="btn btn-success btn-sm"
                                  >
                                    Submit
                                  </button>
                                </center>
                              </div>
                            </form>
                          </div>
                        )}
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

export default CompanyHome;
