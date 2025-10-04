import React, { useState } from "react";
import './left-container.css';

function LeftContainer() {
  const [filters, setFilters] = useState({
    keyword: "",
    author: "",
    yearRange: "",
    sortOrder: "desc",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Filters applied:", filters);
    // Later: pass filters to parent or API
  };

  return (
    <div className="left-container">
      <nav className="search">
        <form className="search-form" onSubmit={handleSubmit}>
          {/* Keyword search */}
          <div className="filter-group">
            <label htmlFor="keyword">Keyword</label>
            <input
              type="text"
              id="keyword"
              name="keyword"
              placeholder="e.g. microgravity"
              value={filters.keyword}
              onChange={handleChange}
            />
          </div>

          {/* Author search */}
          <div className="filter-group">
            <label htmlFor="author">Author</label>
            <input
              type="text"
              id="author"
              name="author"
              placeholder="e.g. John Doe"
              value={filters.author}
              onChange={handleChange}
            />
          </div>

          {/* Year range dropdown */}
          <div className="filter-group">
            <label htmlFor="yearRange">Year Range</label>
            <select
              id="yearRange"
              name="yearRange"
              value={filters.yearRange}
              onChange={handleChange}
            >
              <option value="">All Years</option>
              <option value="2020-2025">2020–2025</option>
              <option value="2010-2019">2010–2019</option>
              <option value="2000-2009">2000–2009</option>
              <option value="Before 2000">Before 2000</option>
            </select>
          </div>

          {/* Sort order dropdown */}
          <div className="filter-group">
            <label htmlFor="sortOrder">Sort By</label>
            <select
              id="sortOrder"
              name="sortOrder"
              value={filters.sortOrder}
              onChange={handleChange}
            >
              <option value="desc">Years Descending</option>
              <option value="asc">Years Ascending</option>
            </select>
          </div>

          {/* Search button */}
          <button type="submit" className="search-button">
            Search
          </button>
        </form>
      </nav>
    </div>
  );
}

export default LeftContainer;
