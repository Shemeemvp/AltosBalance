import React, { useState } from "react";
import "../styles/SignIn.css";
import config from "../../functions/config";
import Swal from "sweetalert2";
import axios from "axios";
import Cookies from "js-cookie";
import { useNavigate } from "react-router-dom";

function StaffReg() {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [companyCode, setCompanyCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const navigate = useNavigate();

  function validate() {
    var pwd = document.getElementById("pwd").value;
    var cnfpwd = document.getElementById("cnfpwd").value;

    if (pwd.length < 8 || pwd.length > 18) {
      alert("Password length is invalid");
      return false;
    }
    if (pwd != cnfpwd) {
      alert("password and confirm password does not match");
      return false;
    }
    return true;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    let valid = validate();
    if (valid) {
      const data = {
        first_name: firstName,
        last_name: lastName,
        username: username,
        company_code: companyCode,
        email: email,
        password: password,
      };
      axios
        .post(`${config.base_url}/staffReg_action/`, data, {
          headers: { "Content-Type": "application/json" },
        })
        .then((res) => {
          if (res.data.status) {
            Cookies.set("user_id", res.data.data.user);
            navigate("/staff_registration2");
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
    <>
      <div className="container_div">
        <div className="forms-container">
          <div className="signin-signup">
            <form action="#" className="sign-up-form" onSubmit={handleSubmit}>
              <h2 className="titleh2" style={{fontWeight:"bolder"}}>Staff Sign up</h2>

              <div className="input-field">
                <i className="fa fa-user"></i>
                <input
                  type="text"
                  placeholder="Firstname"
                  name="first_name"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  required
                />
              </div>
              <div className="input-field">
                <i className="fa fa-user"></i>
                <input
                  type="text"
                  placeholder="Lastname"
                  name="last_name"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  required
                />
              </div>
              <div className="input-field">
                <i className="fa fa-envelope"></i>
                <input
                  type="email"
                  placeholder="Email"
                  name="email"
                  pattern="[^@\s]+@[^@\s]+\.[^@\s]+"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="input-field">
                <i className="fa fa-user"></i>
                <input
                  type="text"
                  placeholder="Username"
                  name="cusername"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  id="user"
                  required
                />
              </div>
              <div class="input-field">
                <i class="fa fa-codepen"></i>
                <input
                  type="text"
                  name="Company_Code"
                  placeholder="Company Code"
                  value={companyCode}
                  onChange={(e) => setCompanyCode(e.target.value)}
                  required
                />
              </div>
              <div className="input-field">
                <i className="fa fa-lock"></i>
                <input
                  type="password"
                  placeholder="Password"
                  pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                  title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
                  name="cpassword"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  id="pwd"
                />
              </div>
              <div className="input-field">
                <i className="fa fa-lock"></i>
                <input
                  type="password"
                  placeholder="Confirm Password"
                  pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                  title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
                  name="cconformpassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  id="cnfpwd"
                />
              </div>
              <input type="submit" className="bttn" value="Sign up" />
            </form>
          </div>
        </div>
      </div>
    </>
  );
}

export default StaffReg;
