import React, { useState } from "react";
import Swal from "sweetalert2";
import axios from "axios";
import Cookies from "js-cookie";
import config from "../../functions/config";
import { useNavigate } from "react-router-dom";
import '../styles/SignIn.css'

function SignIn() {
  const [logUsername, setLogUsername] = useState("");
  const [logPassword, setLogPassword] = useState("");

  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    const loginData = {
      username: logUsername,
      password: logPassword,
    };

    axios
      .post(`${config.base_url}/LogIn/`, loginData)
      .then((res) => {
        if (res.data.status) {
          Cookies.set("user_id", res.data.user);
          Cookies.set("access", res.data.access);
          Cookies.set("refresh", res.data.refresh);
          Cookies.set("role", res.data.role);

          if (res.data.redirect != "") {
            navigate("/" + res.data.redirect);
          }
        } else if (!res.data.status && res.data.redirect != "") {
          Cookies.set("user_id", res.data.user);
          Swal.fire({
            icon: "error",
            title: `${res.data.message}`,
          });
          navigate("/" + res.data.redirect);
        }
      })
      .catch((err) => {
        if (!err.response.data.status) {
          Swal.fire({
            icon: "error",
            title: `${err.response.data.message}`,
          });
          if (err.response.data.redirect && err.response.data.redirect != "") {
            navigate("/" + err.response.data.redirect);
          }
        }
      });
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
            <form onSubmit={handleLogin} className="sign-in-form">
              <h2 className="titleh2" style={{ fontWeight: "bolder" }}>
                Sign in
              </h2>
              <div className="input-field">
                <i className="fa fa-user"></i>
                <input
                  type="text"
                  placeholder="Username"
                  name="username"
                  value={logUsername}
                  onChange={(e) => setLogUsername(e.target.value)}
                  required
                />
              </div>
              <div className="input-field">
                <i className="fa fa-lock"></i>
                <input
                  type="password"
                  placeholder="Password"
                  name="password"
                  value={logPassword}
                  onChange={(e) => setLogPassword(e.target.value)}
                  required
                />
              </div>
              <input type="submit" value="Login" className="bttn solid" />
              <a className="forgot-password">Forgot password...?</a>
              <msg></msg>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}

export default SignIn;
