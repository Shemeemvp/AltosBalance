import React, { useEffect, useState } from "react";
import Cookies from "js-cookie";
import axios from "axios";
import config from "../../functions/config";
import { Link, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function DistributorProfileEdit() {
  const user = Cookies.get("role");
  const navigate = useNavigate();

  const [personalData, setPersonalData] = useState([
    {
      userImage: false,
      firstName: "",
      lastName: "",
      email: "",
      userContact: "",
    },
  ]);

  const [file, setFile] = useState(null);

  const ID = Cookies.get("user_id");
  const getProfileDetails = () => {
    axios
      .get(`${config.base_url}/get_distributor_profile_data/${ID}/`)
      .then((res) => {
        if (res.data.status) {
          const pers = res.data.personalData;
          if (pers.userImage) {
            var logoUrl = `${config.base_url}/${pers.userImage}`;
          }
          const p = {
            userImage: logoUrl,
            firstName: pers.firstName,
            lastName: pers.lastName,
            email: pers.email,
            userContact: pers.userContact,
          };
          setPersonalData(p);
        }
      })
      .catch((err) => {
      });
  };

  useEffect(() => {
    getProfileDetails();
  }, []);

  const handlePersonalDataChange = (e) => {
    setPersonalData({
      ...personalData,
      [e.target.name]: e.target.value,
    });
  };

  function handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("Id", ID);
    formData.append("first_name", personalData.firstName);
    formData.append("last_name", personalData.lastName);
    formData.append("email", personalData.email);
    formData.append("contact", personalData.userContact);
    if (file) {
      formData.append("image", file);
    }

    axios
      .put(`${config.base_url}/edit_distributor_profile/`, formData)
      .then((res) => {
        if (res.data.status) {
          Toast.fire({
            icon: "success",
            title: "Profile Updated",
          });
          navigate("/distributor_profile");
        }
      })
      .catch((err) => {
        console.log(err)
        if (!err.response.data.status) {
          Swal.fire({
            icon: "error",
            title: `${err.response.data.message}`,
          });
        }
      });
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
              <div className="card radius-15">
                <div className="card-body">
                  <div className="card-title">
                    <form
                      action="#"
                      onSubmit={handleSubmit}
                      method="post"
                      encType="multipart/form-data"
                    >
                      <center>
                        <h3 className="mb-0" style={{ fontWeight: "bolder" }}>
                          MY PROFILE
                        </h3>

                        {personalData.userImage ? (
                          <img
                            src={personalData.userImage}
                            className="img img-fluid m-3"
                            style={{
                              width: "150px",
                              height: "150px",
                              borderRadius: "50%",
                            }}
                          />
                        ) : (
                          <img
                            src={`${process.env.PUBLIC_URL}/static/assets/images/user-1.jpg`}
                            className="img img-fluid m-3"
                            style={{
                              width: "150px",
                              height: "150px",
                              borderRadius: "50%",
                            }}
                          />
                        )}

                        <div className="row d-flex justify-content-center">
                          <input
                            type="file"
                            name="img"
                            className="form-control w-25"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                            accept="image/*"
                            onChange={(e) => setFile(e.target.files[0])}
                          />
                        </div>
                      </center>
                      <hr className="text-white" />

                      <h4 className="m-4 w-100">Personal Info</h4>
                      <div className="row m-3 w-100">
                        <div className="col-md-6">
                          <label htmlFor="first_name">First Name</label>
                          <input
                            type="text"
                            name="firstName"
                            id="first_name"
                            value={personalData.firstName}
                            onChange={handlePersonalDataChange}
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                        <div className="col-md-6">
                          <label htmlFor="last_name">Last Name</label>
                          <input
                            type="text"
                            name="lastName"
                            id="last_name"
                            value={personalData.lastName}
                            onChange={handlePersonalDataChange}
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                      </div>
                      <div className="row m-3 w-100">
                        <div className="col-md-6">
                          <label htmlFor="email">E-mail</label>
                          <input
                            type="email"
                            name="email"
                            id="email"
                            value={personalData.email}
                            onChange={handlePersonalDataChange}
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                        <div className="col-md-6">
                          <label htmlFor="email">Contact</label>
                          <input
                            type="text"
                            name="userContact"
                            id="contact"
                            value={personalData.userContact}
                            onChange={handlePersonalDataChange}
                            pattern="[0-9]{10}"
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                      </div>
                      <div className="row m-3">
                        <div className="col-md-6"></div>
                      </div>

                      <center className="w-100">
                        <button
                          className="btn btn-outline-secondary mt-4 px-5"
                          type="submit"
                          style={{ width: "fit-content", height:"fit-content" }}
                        >
                          Submit
                        </button>
                      </center>
                    </form>
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

export default DistributorProfileEdit;
