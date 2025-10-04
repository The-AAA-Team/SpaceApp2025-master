import React, { useState } from "react";
import "./navbar.css";

function Navbar() {
  const [searchTerm, setSearchTerm] = useState("");

  const handleChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("Searching for:", searchTerm);
    // later add filtering or api calls here
    //currently stores search terms to console
  };

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <h1>DataShip</h1>
      </div>

      <form className="search-form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="search-input"
          placeholder="Search for articles..."
          value={searchTerm}
          onChange={handleChange}
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>
    </nav>
  );
}

export default Navbar;
