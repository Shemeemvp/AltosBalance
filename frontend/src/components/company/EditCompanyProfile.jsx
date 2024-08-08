import React, { useEffect, useState } from "react";
import Cookies from "js-cookie";
import axios from "axios";
import config from "../../functions/config";
import { Link, useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

function EditCompanyProfile() {
  const user = Cookies.get("role");
  const navigate = useNavigate();
  var is_company = false;
  if (user === "Company") {
    is_company = true;
  }

  const [personalData, setPersonalData] = useState([
    {
      companyLogo: false,
      firstName: "",
      lastName: "",
      email: "",
      companyContact: "",
    },
  ]);

  const [file, setFile] = useState(null);

  const [companyData, setCompanyData] = useState([
    {
      businessName: "",
      companyName: "",
      companyType: "",
      industry: "",
      companyEmail: "",
      panNumber: "",
      gstType: "",
      gstNo: "",
      paymentTerm: "",
      endDate: "",
      address: "",
      city: "",
      state: "",
      pincode: "",
    },
  ]);

  const ID = Cookies.get("user_id");
  const getProfileDetails = () => {
    axios
      .get(`${config.base_url}/get_profile_data/${ID}/`)
      .then((res) => {
        console.log(res)
        if (res.data.status) {
          const pers = res.data.personalData;
          const cmp = res.data.companyData;
          if (pers.companyLogo) {
            var logoUrl = `${config.base_url}/${pers.companyLogo}`;
          }
          const p = {
            companyLogo: logoUrl,
            firstName: pers.firstName,
            lastName: pers.lastName,
            email: pers.email,
            companyContact: pers.companyContact,
          };
          const c = {
            businessName: cmp.businessName,
            companyName: cmp.companyName,
            companyType: cmp.companyType,
            industry: cmp.industry,
            companyEmail: cmp.companyEmail,
            panNumber: cmp.panNumber,
            gstType: cmp.gstType,
            gstNo: cmp.gstNo,
            paymentTerm: cmp.paymentTerm,
            address: cmp.address,
            city: cmp.city,
            state: cmp.state,
            pincode: cmp.pincode,
          };
          setPersonalData(p);
          setCompanyData(c);
        }
      })
      .catch((err) => {
        console.log("ERROR==", err);
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

  const handleCompanyDataChange = (e) => {
    setCompanyData({
      ...companyData,
      [e.target.name]: e.target.value,
    });
  };

  function validatePan() {
    var panVal = document.getElementById("pannum").value;
    var regpan = /^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$/;
    var pannumElement = document.getElementById("pannum");

    if (regpan.test(panVal)) {
      pannumElement.style.border = "2px solid green";
    } else {
      pannumElement.style.border = "2px solid red";
    }
  }

  function validateGST() {
    var gstVal = document.getElementById("gstnum").value;
    var regGST = /^\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}$/;
    var gstnumElement = document.getElementById("gstnum");

    if (regGST.test(gstVal)) {
      gstnumElement.style.border = "2px solid green";
    } else {
      gstnumElement.style.border = "2px solid red";
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("Id", ID);
    formData.append("first_name", personalData.firstName);
    formData.append("last_name", personalData.lastName);
    formData.append("email", personalData.email);
    formData.append("contact", personalData.companyContact);
    formData.append("company_name", companyData.companyName);
    formData.append("address", companyData.address);
    formData.append("city", companyData.city);
    formData.append("state", companyData.state);
    formData.append("pincode", companyData.pincode);
    formData.append("business_name", companyData.businessName);
    formData.append("industry", companyData.industry);
    formData.append("company_type", companyData.companyType);
    formData.append("pan_no", companyData.panNumber);
    formData.append("gst_type", companyData.gstType);
    formData.append("gst_no", companyData.gstNo);
    if (file) {
      formData.append("image", file);
    }

    axios
      .put(`${config.base_url}/edit_company_profile/`, formData)
      .then((res) => {
        if (res.data.status) {
          Toast.fire({
            icon: "success",
            title: "Profile Updated",
          });
          navigate("/company_profile");
        }
      })
      .catch((err) => {
        console.log("ERROR==", err);
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
  const [gstType, setGstType] = useState("");
  const handleGstTypeSubmit = (e) => {
    e.preventDefault();

    const data = {
      ID: ID,
      gsttype: gstType,
    };

    axios
      .post(`${config.base_url}/edit_gsttype/`, data)
      .then((res) => {
        if (res.data.status) {
          Toast.fire({
            icon: "success",
            title: `${res.data.message}`,
          });
          document.getElementById('closeGstTypeModal').click();
          getProfileDetails();
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
  };
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
                    <form
                      onSubmit={handleSubmit}
                      encType="multipart/form-data"
                    >
                      <center>
                        <h3 className="mb-0" style={{ fontWeight: "bolder" }}>
                          MY PROFILE
                        </h3>

                        {personalData.companyLogo ? (
                          <img
                            src={personalData.companyLogo}
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
                            name="companyContact"
                            id="contact"
                            value={personalData.companyContact}
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

                      <h4 className="m-4 w-100">Company Info</h4>

                      <div className="row m-3 w-100">
                        <div className="col-md-6">
                          <label htmlFor="cname">Company Name</label>
                          <input
                            type="text"
                            name="companyName"
                            id="cname"
                            value={companyData.companyName}
                            onChange={handleCompanyDataChange}
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                        <div className="col-md-6">
                          <label htmlFor="caddress">Company Address</label>
                          <input
                            type="text"
                            name="address"
                            id="caddress"
                            value={companyData.address}
                            onChange={handleCompanyDataChange}
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
                          <label htmlFor="city">City</label>
                          <input
                            type="text"
                            name="city"
                            id="city"
                            value={companyData.city}
                            onChange={handleCompanyDataChange}
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                        <div className="col-md-6">
                          <label htmlFor="state">State</label>
                          <input
                            type="text"
                            name="state"
                            id="state"
                            value={companyData.state}
                            onChange={handleCompanyDataChange}
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
                          <label htmlFor="pincode">Pincode</label>
                          <input
                            type="text"
                            name="pincode"
                            id="pincode"
                            value={companyData.pincode}
                            onChange={handleCompanyDataChange}
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
                          <label htmlFor="bname">Legal Business Name</label>
                          <input
                            type="text"
                            name="businessName"
                            id="bname"
                            value={companyData.businessName}
                            onChange={handleCompanyDataChange}
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                        <div className="col-md-6">
                          <label htmlFor="ctype">Pan Number</label>
                          <input
                            type="text"
                            name="panNumber"
                            id="pannum"
                            value={companyData.panNumber}
                            onChange={handleCompanyDataChange}
                            onInput={validatePan}
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          />
                        </div>
                      </div>
                      <div className="row m-3 w-100 align-items-center">
                        <div className="col-md-6">
                          <label for="industry">GST Type</label>
                            <div className="d-flex">
                            <input
                              type="text"
                              className="form-control"
                              name="gstType"
                              id="gsttype"
                              style={{
                                backgroundColor: "rgb(244 245 247)",
                                color: "black",
                              }}
                              value={companyData.gstType}
                            />
                            <button
                              type="button"
                              style={{
                                borderRadius: "0px 10px 10px 0px",
                                margin: "0",
                              }}
                              title="change Payment Term"
                              typeof="button"
                              className="btn btn-secondary"
                              data-toggle="modal"
                              data-target="#gstchange"
                            >
                              <i className="fa fa-edit"></i>
                            </button>

                            </div>
                        </div>
                        {/* <div className="col-md-1">
                          <a
                            className=" text-warning-emphasis"
                            data-toggle="modal"
                            data-target="#gstchange"
                          >
                            <i
                              className="fa fa-edit mt-4"
                              style={{ fontSize: "larger" }}
                            ></i>
                          </a>
                        </div> */}
                        <div className="col-md-6">
                          {companyData.gstType ==
                            "Registered Business - Regular" ||
                          companyData.gstType ==
                            "Registered Business - Composition" ? (
                            <>
                              <label for="ctype">GST Number</label>
                              {companyData.gstNo != "" || companyData.gstNo != null ? (
                                <input
                                  type="text"
                                  name="gstNo"
                                  id="gstnum"
                                  value={companyData.gstNo}
                                  onChange={handleCompanyDataChange}
                                  onInput={validateGST}
                                  className="form-control "
                                  style={{
                                    backgroundColor: "rgb(244 245 247)",
                                    color: "black",
                                  }}
                                  pattern="[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}"
                                  title="GST Number should be in the format '11AAAAA1111A1ZA'"
                                  required
                                />
                              ) : (
                                <input
                                  type="text"
                                  name="gstNo"
                                  id="gstnum"
                                  onChange={handleCompanyDataChange}
                                  placeholder="Enter your GST number*"
                                  onInput={validateGST}
                                  className="form-control "
                                  style={{
                                    backgroundColor: "rgb(244 245 247)",
                                    color: "black",
                                  }}
                                  pattern="[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}"
                                  title="GST Number should be in the format '11AAAAA1111A1ZA'"
                                  required
                                />
                              )}
                            </>
                          ) : null}
                        </div>
                      </div>
                      <div className="row m-3 w-100">
                        <div className="col-md-6">
                          <label for="industry">Your Industry</label>
                          <select
                            name="industry"
                            id="industry"
                            onChange={handleCompanyDataChange}
                            required
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                          >
                            <option value={companyData.industry}>
                              {companyData.industry}
                            </option>
                            <option value="Accounting Services">
                              Accounting Services
                            </option>
                            <option value="Consultants, doctors, Lawyers and similar">
                              Consultants, doctors, Lawyers and similar
                            </option>
                            <option value="Information Technology">
                              Information Technology
                            </option>
                            <option value="Manufacturing">Manufacturing</option>
                            <option value="Professional Scientific and Technical Services">
                              Professional, Scientific and Technical Services
                            </option>
                            <option value="Restaurant/Bar and similar">
                              Restaurant/Bar and similar
                            </option>
                            <option value="Retail and Smilar">
                              Retail and Smilar
                            </option>
                            <option value="Other Finanacial Services">
                              Other Finanacial Services
                            </option>
                          </select>
                        </div>
                        <div className="col-md-6">
                          <label for="ctype">Company Type</label>
                          <select
                            name="companyType"
                            onChange={handleCompanyDataChange}
                            id="ctype"
                            className="form-control"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                            required
                          >
                            <option value={companyData.companyType} hidden>
                              {companyData.companyType}
                            </option>
                            <option value="Private Limited Company">
                              Private Limited Company
                            </option>
                            <option value="Public Limited Company">
                              Public Limited Company
                            </option>
                            <option value="Joint-Venture Company">
                              Joint-Venture Company
                            </option>
                            <option value="Partnership Firm Company">
                              Partnership Firm Company
                            </option>
                            <option value="One Person Company">
                              One Person Company
                            </option>
                            <option value="Branch Office Company">
                              Branch Office Company
                            </option>
                            <option value="Non Government Organization">
                              Non Government Organization
                            </option>
                          </select>
                        </div>
                      </div>

                      <center className="w-100">
                        <button
                          className="btn btn-outline-secondary px-5 mt-4"
                          type="submit"
                          style={{
                            width: "fit-content",
                            height: "fit-content",
                          }}
                        >
                          Submit
                        </button>
                      </center>
                    </form>
                  </div>
                </div>
              </div>
            </div>

            {/* <!-- Modal for change gst type--> */}
            <div
              className="modal fade"
              id="gstchange"
              tabindex="-1"
              aria-labelledby="exampleModalLabel"
              aria-hidden="true"
            >
              <div className="modal-dialog">
                <div
                  className="modal-content shadow p-3 rounded"
                  style={{
                    backgroundColor: "rgb(209 209 209)",
                    border: "1px solid rgba(255, 255, 255, 0.3)",
                  }}
                >
                  <div className="modal-body">
                    <form
                      onSubmit={handleGstTypeSubmit}
                      className="w-100 px-0"
                    >
                      <div className="row mt-3 w-100">
                        <h5 className="text-secondary w-100 font-weight-bold">GST Type Change</h5>
                      </div>

                      <div className="row mt-3 w-100">
                        <div className="col-md-3">
                          <h6 className="text-secondary mt-2">Type*</h6>
                        </div>
                        <div className="col-md-9">
                          <select
                            className="form-control"
                            name="gsttype"
                            onChange={(e) => setGstType(e.target.value)}
                            id="gsttype"
                            style={{
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                            required
                          >
                            <option
                              value=""
                              style={{
                                backgroundColor: "rgb(244 245 247)",
                                color: "black",
                              }}
                            >
                              Select
                            </option>
                            <option
                              value="Registered Business - Regular"
                              style={{
                                backgroundColor: "rgb(244 245 247)",
                                color: "black",
                              }}
                            >
                              Registered Business - Regular
                              <span>
                                <i>(Business that is registered under gst)</i>
                              </span>
                            </option>
                            <option
                              value="Registered Business - Composition"
                              style={{
                                backgroundColor: "rgb(244 245 247)",
                                color: "black",
                              }}
                            >
                              Registered Business - Composition (Business that
                              is registered under composition scheme in gst)
                            </option>
                            <option
                              value="unregistered Business"
                              style={{
                                backgroundColor: "rgb(244 245 247)",
                                color: "black",
                              }}
                            >
                              Unregistered Business (Business that has not been
                              registered under gst)
                            </option>
                            <option
                              value="Overseas"
                              style={{
                                backgroundColor: "rgb(244 245 247)",
                                color: "black",
                              }}
                            >
                              Overseas (Import/Export of supply outside india)
                            </option>
                            <option
                              value="Consumer"
                              style={{
                                backgroundColor: "rgb(244 245 247)",
                                color: "black",
                              }}
                            >
                              Consumer
                            </option>
                          </select>
                          <input
                            type="text"
                            name="gstno"
                            id="gstno"
                            placeholder="GST Number"
                            className="gstno form-control d-none mt-2 text-white"
                            style={{
                              border: "1px solid rgba(255, 255, 255, 0.3)",
                              backgroundColor: "rgb(244 245 247)",
                              color: "black",
                            }}
                            pattern="^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
                            title="GST Number should be in the format '11AAAAA1111A1ZA'"
                          />
                        </div>
                      </div>

                      <div className="modal-footer mt-3 d-flex justify-content-end w-100">
                        <button
                          type="reset"
                          style={{ width: "70px", height: "30px" }}
                          className="btn btn-sm btn-outline-danger"
                          data-dismiss="modal"
                          id="closeGstTypeModal"
                        >
                          Close
                        </button>
                        <button
                          type="submit"
                          style={{ width: "70px", height: "30px" }}
                          className="btn btn-sm btn-success"
                        >
                          Save
                        </button>
                      </div>
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

export default EditCompanyProfile;
