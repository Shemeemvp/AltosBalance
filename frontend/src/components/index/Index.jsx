import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

function Index() {
  const [dropdownVisible, setDropdownVisible] = useState(false);

  const navigate = useNavigate();

  const handleMouseEnter = () => {
    setDropdownVisible(true);
  };

  const handleMouseLeave = () => {
    setDropdownVisible(false);
  };

  return (
    <>
      {/* ***** Preloader Start ***** */}
      <div id="preloader">
        <div className="jumper">
          <div />
          <div />
          <div />
        </div>
      </div>
      {/* ***** Preloader End ***** */}
      {/* Header */}
      <header className="">
        <nav className="navbar navbar-expand-lg">
          <div className="container">
            <a className="navbar-brand" href="#">
              <h2>AltosBalance</h2>
            </a>
            <button
              className="navbar-toggler"
              type="button"
              data-toggle="collapse"
              data-target="#navbarResponsive"
              aria-controls="navbarResponsive"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon" />
            </button>
            <div className="collapse navbar-collapse" id="navbarResponsive">
              <ul className="navbar-nav ml-auto">
                <li className="nav-item">
                  <a className="nav-link current" href="#top">
                    Home
                    <span className="sr-only">(current)</span>
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" href="#services">
                    Our Services
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" href="#about">
                    About Us
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link" href="#contactus">
                    Contact Us
                  </a>
                </li>
                <li
                  className="nav-item"
                  onMouseEnter={handleMouseEnter}
                  onMouseLeave={handleMouseLeave}
                >
                  <a href="#" className="nav-link">
                    Sign Up <i className="bi bi-chevron-down"></i>
                  </a>
                  <ul
                    className={`${dropdownVisible ? " show_reg_options" : ""}`}
                    id="regMenu"
                    style={{ display: dropdownVisible ? "block" : "none" }}
                  >
                    <li>
                      <Link to="/login">Distributor Registration</Link>
                    </li>
                    <li>
                      <a onClick={()=>navigate("/company_registration")}>
                        Company Registration
                      </a>
                    </li>
                    <li>
                      <Link to="/staff_registration">Staff Registration</Link>
                    </li>
                  </ul>
                </li>
                <a
                  onClick={() => navigate("/login")}
                  style={{ width: "fit-content", height: "fit-content" }}
                  className="filled-button"
                >
                  LOGIN
                </a>
                {/* <li className="nav-item">
                  <a className="nav-link external" href="index.html">
                    Multi-page
                  </a>
                </li> */}
              </ul>
            </div>
          </div>
        </nav>
      </header>
      {/* Page Content */}
      {/* Banner Starts Here */}
      <div className="main-banner header-text" id="top">
        <div className="Modern-Slider">
          {/* Item */}
          <div className="item item-1">
            <div className="img-fill">
              <div className="text-content">
                <h6>we are ready to help you</h6>
                <h4>
                  Financial Analysis
                  <br />
                  &amp; Consulting
                </h4>
                <p>
                  This finance HTML template is 100% free of charge provided by
                  TemplateMo. This is one-page version added in 2021 February.{" "}
                  <a href="#">Multiple-page version</a> with different HTML
                  pages are also available.
                </p>
                <a href="contact.html" className="filled-button">
                  contact us
                </a>
              </div>
            </div>
          </div>
          {/* // Item */}
          {/* Item */}
          <div className="item item-2">
            <div className="img-fill">
              <div className="text-content">
                <h6>we are here to support you</h6>
                <h4>
                  Accounting
                  <br />
                  &amp; Management
                </h4>
                <p>
                  You are allowed to use this template for your company
                  websites. You are NOT allowed to re-distribute this template
                  ZIP file on any template download website. Please contact
                  TemplateMo for more detail.
                </p>
                <a href="#" className="filled-button">
                  our services
                </a>
              </div>
            </div>
          </div>
          {/* // Item */}
          {/* Item */}
          <div className="item item-3">
            <div className="img-fill">
              <div className="text-content">
                <h6>we have a solid background</h6>
                <h4>
                  Market Analysis
                  <br />
                  &amp; Statistics
                </h4>
                <p>
                  You can download, edit and use this finance business layout
                  for your commercial websites. You just need to put
                  className="external" if you wish to link to external URLs in
                  the main menu.
                </p>
                <a href="#" className="filled-button">
                  learn more
                </a>
              </div>
            </div>
          </div>
          {/* // Item */}
        </div>
      </div>
      {/* Banner Ends Here */}
      <div className="request-form">
        <div className="container">
          <div className="row">
            <div className="col-md-8">
              <h4>Request a call back right now ?</h4>
              <span>
                Mauris ut dapibus velit cras interdum nisl ac urna tempor
                mollis.
              </span>
            </div>
            <div className="col-md-4">
              <a href="#" className="border-button">
                Contact Us
              </a>
            </div>
          </div>
        </div>
      </div>
      <div className="services" id="services">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <div className="section-heading">
                <h2>
                  Financial <em>Services</em>
                </h2>
                <span>Aliquam id urna imperdiet libero mollis hendrerit</span>
              </div>
            </div>
            <div className="col-md-4">
              <div className="service-item">
                <img
                  src={`${process.env.PUBLIC_URL}/assets/images/service_01.jpg`}
                  alt=""
                />
                <div className="down-content">
                  <h4>Digital Currency</h4>
                  <p>
                    Sed tincidunt dictum lobortis. Aenean tempus diam vel augue
                    luctus dignissim. Nunc ornare leo tortor.
                  </p>
                  <a href="" className="filled-button">
                    Read More
                  </a>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="service-item">
                <img
                  src={`${process.env.PUBLIC_URL}/assets/images/service_02.jpg`}
                  alt=""
                />
                <div className="down-content">
                  <h4>Market Analysis</h4>
                  <p>
                    Sed tincidunt dictum lobortis. Aenean tempus diam vel augue
                    luctus dignissim. Nunc ornare leo tortor.
                  </p>
                  <a href="" className="filled-button">
                    Read More
                  </a>
                </div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="service-item">
                <img
                  src={`${process.env.PUBLIC_URL}/assets/images/service_03.jpg`}
                  alt=""
                />
                <div className="down-content">
                  <h4>Historical Data</h4>
                  <p>
                    Sed tincidunt dictum lobortis. Aenean tempus diam vel augue
                    luctus dignissim. Nunc ornare leo tortor.
                  </p>
                  <a href="" className="filled-button">
                    Read More
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="fun-facts">
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <div className="left-content">
                <span>Lorem ipsum dolor sit amet</span>
                <h2>
                  Our solutions for your <em>business growth</em>
                </h2>
                <p>
                  Pellentesque ultrices at turpis in vestibulum. Aenean pretium
                  elit nec congue elementum. Nulla luctus laoreet porta.
                  Maecenas at nisi tempus, porta metus vitae, faucibus augue.
                  <br />
                  <br />
                  Fusce et venenatis ex. Quisque varius, velit quis dictum
                  sagittis, odio velit molestie nunc, ut posuere ante tortor ut
                  neque.
                </p>
                <a href="" className="filled-button">
                  Read More
                </a>
              </div>
            </div>
            <div className="col-md-6 align-self-center">
              <div className="row">
                <div className="col-md-6">
                  <div className="count-area-content">
                    <div className="count-digit">945</div>
                    <div className="count-title">Work Hours</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="count-area-content">
                    <div className="count-digit">1280</div>
                    <div className="count-title">Great Reviews</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="count-area-content">
                    <div className="count-digit">578</div>
                    <div className="count-title">Projects Done</div>
                  </div>
                </div>
                <div className="col-md-6">
                  <div className="count-area-content">
                    <div className="count-digit">26</div>
                    <div className="count-title">Awards Won</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="more-info" id="about">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <div className="more-info-content">
                <div className="row">
                  <div className="col-md-6">
                    <div className="left-image">
                      <img
                        src={`${process.env.PUBLIC_URL}/assets/images/more-info.jpg`}
                        alt=""
                      />
                    </div>
                  </div>
                  <div className="col-md-6 align-self-center">
                    <div className="right-content">
                      <span>Who we are</span>
                      <h2>
                        Get to know about <em>our company</em>
                      </h2>
                      <p>
                        Curabitur pulvinar sem a leo tempus facilisis. Sed non
                        sagittis neque. Nulla conse quat tellus nibh, id
                        molestie felis sagittis ut. Nam ullamcorper tempus ipsum
                        in cursus
                        <br />
                        <br />
                        Praes end at dictum metus. Morbi id hendrerit lectus,
                        nec dapibus ex. Etiam ipsum quam, luctus eu egestas
                        eget, tincidunt
                      </p>
                      <a href="#" className="filled-button">
                        Read More
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="testimonials">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <div className="section-heading">
                <h2>
                  What they say <em>about us</em>
                </h2>
                <span>testimonials from our greatest clients</span>
              </div>
            </div>
            <div className="col-md-12">
              <div className="owl-testimonials owl-carousel">
                <div className="testimonial-item">
                  <div className="inner-content">
                    <h4>George Walker</h4>
                    <span>Chief Financial Analyst</span>
                    <p>
                      "Nulla ullamcorper, ipsum vel condimentum congue, mi odio
                      vehicula tellus, sit amet malesuada justo sem sit amet
                      quam. Pellentesque in sagittis lacus."
                    </p>
                  </div>
                  <img src="http://placehold.it/60x60" alt="" />
                </div>
                <div className="testimonial-item">
                  <div className="inner-content">
                    <h4>John Smith</h4>
                    <span>Market Specialist</span>
                    <p>
                      "In eget leo ante. Sed nibh leo, laoreet accumsan euismod
                      quis, scelerisque a nunc. Mauris accumsan, arcu id ornare
                      malesuada, est nulla luctus nisi."
                    </p>
                  </div>
                  <img src="http://placehold.it/60x60" alt="" />
                </div>
                <div className="testimonial-item">
                  <div className="inner-content">
                    <h4>David Wood</h4>
                    <span>Chief Accountant</span>
                    <p>
                      "Ut ultricies maximus turpis, in sollicitudin ligula
                      posuere vel. Donec finibus maximus neque, vitae egestas
                      quam imperdiet nec. Proin nec mauris eu tortor consectetur
                      tristique."
                    </p>
                  </div>
                  <img src="http://placehold.it/60x60" alt="" />
                </div>
                <div className="testimonial-item">
                  <div className="inner-content">
                    <h4>Andrew Boom</h4>
                    <span>Marketing Head</span>
                    <p>
                      "Curabitur sollicitudin, tortor at suscipit volutpat, nisi
                      arcu aliquet dui, vitae semper sem turpis quis libero.
                      Quisque vulputate lacinia nisl ac lobortis."
                    </p>
                  </div>
                  <img src="http://placehold.it/60x60" alt="" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="callback-form" id="contactus">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <div className="section-heading">
                <h2>
                  Request a <em>call back</em>
                </h2>
                <span>Etiam suscipit ante a odio consequat</span>
              </div>
            </div>
            <div className="col-md-12">
              <div className="contact-form">
                <form id="contact" action="" method="post">
                  <div className="row">
                    <div className="col-lg-4 col-md-12 col-sm-12">
                      <fieldset>
                        <input
                          name="name"
                          type="text"
                          className="form-control"
                          id="name"
                          placeholder="Full Name"
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div className="col-lg-4 col-md-12 col-sm-12">
                      <fieldset>
                        <input
                          name="email"
                          type="text"
                          className="form-control"
                          id="email"
                          pattern="[^ @]*@[^ @]*"
                          placeholder="E-Mail Address"
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div className="col-lg-4 col-md-12 col-sm-12">
                      <fieldset>
                        <input
                          name="subject"
                          type="text"
                          className="form-control"
                          id="subject"
                          placeholder="Subject"
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div className="col-lg-12">
                      <fieldset>
                        <textarea
                          name="message"
                          rows={6}
                          className="form-control"
                          id="message"
                          placeholder="Your Message"
                          required=""
                          defaultValue={""}
                        />
                      </fieldset>
                    </div>
                    <div className="col-lg-12">
                      <fieldset>
                        <button
                          type="submit"
                          id="form-submit"
                          className="border-button"
                        >
                          Send Message
                        </button>
                      </fieldset>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="partners">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <div className="owl-partners owl-carousel">
                <div className="partner-item">
                  <img
                    src={`${process.env.PUBLIC_URL}/assets/images/client-01.png`}
                    title={1}
                    alt={1}
                  />
                </div>
                <div className="partner-item">
                  <img
                    src={`${process.env.PUBLIC_URL}/assets/images/client-01.png`}
                    title={2}
                    alt={2}
                  />
                </div>
                <div className="partner-item">
                  <img
                    src={`${process.env.PUBLIC_URL}/assets/images/client-01.png`}
                    title={3}
                    alt={3}
                  />
                </div>
                <div className="partner-item">
                  <img
                    src={`${process.env.PUBLIC_URL}/assets/images/client-01.png`}
                    title={4}
                    alt={4}
                  />
                </div>
                <div className="partner-item">
                  <img
                    src={`${process.env.PUBLIC_URL}/assets/images/client-01.png`}
                    title={5}
                    alt={5}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Footer Starts Here */}
      <footer>
        <div className="container">
          <div className="row">
            <div className="col-md-3 footer-item">
              <h4>Finance Business</h4>
              <p>
                Vivamus tellus mi. Nulla ne cursus elit,vulputate. Sed ne cursus
                augue hasellus lacinia sapien vitae.
              </p>
              <ul className="social-icons">
                <li>
                  <a
                    rel="nofollow"
                    href="https://fb.com/templatemo"
                    target="_blank"
                  >
                    <i className="fa fa-facebook" />
                  </a>
                </li>
                <li>
                  <a href="#">
                    <i className="fa fa-twitter" />
                  </a>
                </li>
                <li>
                  <a href="#">
                    <i className="fa fa-linkedin" />
                  </a>
                </li>
                <li>
                  <a href="#">
                    <i className="fa fa-behance" />
                  </a>
                </li>
              </ul>
            </div>
            <div className="col-md-3 footer-item">
              <h4>Useful Links</h4>
              <ul className="menu-list">
                <li>
                  <a href="#">Vivamus ut tellus mi</a>
                </li>
                <li>
                  <a href="#">Nulla nec cursus elit</a>
                </li>
                <li>
                  <a href="#">Vulputate sed nec</a>
                </li>
                <li>
                  <a href="#">Cursus augue hasellus</a>
                </li>
                <li>
                  <a href="#">Lacinia ac sapien</a>
                </li>
              </ul>
            </div>
            <div className="col-md-3 footer-item">
              <h4>Additional Pages</h4>
              <ul className="menu-list">
                <li>
                  <a href="#">About Us</a>
                </li>
                <li>
                  <a href="#">How We Work</a>
                </li>
                <li>
                  <a href="#">Quick Support</a>
                </li>
                <li>
                  <a href="#">Contact Us</a>
                </li>
                <li>
                  <a href="#">Privacy Policy</a>
                </li>
              </ul>
            </div>
            <div className="col-md-3 footer-item last-item">
              <h4>Contact Us</h4>
              <div className="contact-form">
                <form id="contact footer-contact" action="" method="post">
                  <div className="row">
                    <div className="col-lg-12 col-md-12 col-sm-12">
                      <fieldset>
                        <input
                          name="name"
                          type="text"
                          className="form-control"
                          id="name"
                          placeholder="Full Name"
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div className="col-lg-12 col-md-12 col-sm-12">
                      <fieldset>
                        <input
                          name="email"
                          type="text"
                          className="form-control"
                          id="email"
                          pattern="[^ @]*@[^ @]*"
                          placeholder="E-Mail Address"
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div className="col-lg-12">
                      <fieldset>
                        <textarea
                          name="message"
                          rows={6}
                          className="form-control"
                          id="message"
                          placeholder="Your Message"
                          required=""
                          defaultValue={""}
                        />
                      </fieldset>
                    </div>
                    <div className="col-lg-12">
                      <fieldset>
                        <button
                          type="submit"
                          id="form-submit"
                          className="filled-button"
                        >
                          Send Message
                        </button>
                      </fieldset>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
}

export default Index;
