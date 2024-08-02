import React, { useEffect, useState } from "react";
import Cookies from "js-cookie";
import axios from "axios";
import config from "../../functions/config";
import { Link, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function DistributorsReq() {
  const [requests, setRequests] = useState([]);
  const user = Cookies.get("role");
  const fetchDistributorRequests = () => {
    if (user === "Admin") {
      axios
        .get(`${config.base_url}/get_distributors_requests/`)
        .then((res) => {
          if (res.data.status) {
            setRequests([]);
            const distReq = res.data.data;
            distReq.map((req) => {
              const r = {
                name: req.name,
                email: req.email,
                contact: req.contact,
                endDate: req.endDate,
                term: req.term,
                id: req.id,
              };
              setRequests((prevState) => [...prevState, r]);
            });
          }
        })
        .catch((err) => {
          if (!err.response.data.status) {
            Swal.fire({
              icon: "error",
              title: `${err.response.data.message}`,
            });
          }
        });
    }
  };

  useEffect(() => {
    fetchDistributorRequests();
  }, []);

  function handleAccept(id) {
    if (user === "Admin") {
      axios
        .put(`${config.base_url}/DReq_Accept/${id}/`)
        .then((res) => {
          if (res.data.status) {
            Toast.fire({
              icon: "success",
              title: "Request Accepted",
            });
            fetchDistributorRequests();
          }
        })
        .catch((err) => {
          if (!err.response.data.status) {
            Swal.fire({
              icon: "error",
              title: `${err.response.data.message}`,
            });
          }
        });
    }
  }

  function handleReject(id) {
    if (user === "Admin") {
      axios
        .delete(`${config.base_url}/DReq_Reject/${id}/`)
        .then((res) => {
          if (res.data.status) {
            Toast.fire({
              icon: "success",
              title: "Request Rejected",
            });
            fetchDistributorRequests();
          }
        })
        .catch((err) => {
          if (!err.response.data.status) {
            Swal.fire({
              icon: "error",
              title: `${err.response.data.message}`,
            });
          }
        });
    }
  }

  const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.onmouseenter = Swal.stopTimer;
      toast.onmouseleave = Swal.resumeTimer;
    },
  });
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
                <div className="card radius-15">
                  <div className="card-body">
                    <div className="card-title"></div>
                    <table className="table table-responsive-md mt-4 table-hover">
                      <thead>
                        <tr>
                          <th
                            style={{
                              textAlign: "center",
                              textTransform: "uppercase",
                            }}
                          >
                            <b>ID</b>
                          </th>
                          <th
                            style={{
                              textAlign: "center",
                              textTransform: "uppercase",
                            }}
                          >
                            <b>Name</b>
                          </th>
                          <th
                            style={{
                              textAlign: "center",
                              textTransform: "uppercase",
                            }}
                          >
                            <b>Email</b>
                          </th>
                          <th
                            style={{
                              textAlign: "center",
                              textTransform: "uppercase",
                            }}
                          >
                            <b>Contact</b>
                          </th>
                          <th
                            style={{
                              textAlign: "center",
                              textTransform: "uppercase",
                            }}
                          >
                            <b>Payment Terms</b>
                          </th>
                          <th
                            style={{
                              textAlign: "center",
                              textTransform: "uppercase",
                            }}
                          >
                            <b>End Date</b>
                          </th>
                          <th
                            style={{
                              textAlign: "center",
                              textTransform: "uppercase",
                            }}
                          >
                            <b>Action</b>
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {requests &&
                          requests.map((req, index) => (
                            <tr>
                              <td style={{ textAlign: "center" }}>
                                {index + 1}
                              </td>
                              <td style={{ textAlign: "center" }}>
                                <Link
                                  to={`/distributors_request_overview/${req.id}/`}
                                >
                                  {req.name}
                                </Link>
                              </td>
                              <td style={{ textAlign: "center" }}>
                                {req.email}
                              </td>
                              <td style={{ textAlign: "center" }}>
                                {req.contact}
                              </td>
                              <td style={{ textAlign: "center" }}>
                                {req.term}
                              </td>
                              <td style={{ textAlign: "center" }}>
                                {req.endDate}
                              </td>
                              <td style={{ textAlign: "center" }}>
                                <button
                                  onClick={() => handleAccept(`${req.id}`)}
                                  className="btn btn-success m-1"
                                  style={{ width: "80px", height: "40px" }}
                                >
                                  Accept
                                </button>
                                <button
                                  onClick={() => handleReject(`${req.id}`)}
                                  className="btn btn-danger m-1"
                                  style={{ width: "80px", height: "40px" }}
                                >
                                  Reject
                                </button>
                              </td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DistributorsReq;
