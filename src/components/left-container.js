import React, { useState } from "react";
import './left-container.css';
import KnowledgeGraph from './knowledgegraph.js'
import { Context } from './context';

function LeftContainer() {
  const { setJSONData } = Context();

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
    setJSONData(filters);
    console.log("Filters applied:", filters);
  };

  return (
    <div className="left-container">
      <div className="search-section">
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

          {/* Year range and Sort order side by side */}
          <div className="filter-row">
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
                <option value="before-2000">Before 2000</option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="sortOrder">Sort By</label>
              <select
                id="sortOrder"
                name="sortOrder"
                value={filters.sortOrder}
                onChange={handleChange}
              disabled>
                <option value="desc">Years Descending</option>
                <option value="asc">Years Ascending</option>
              </select>
            </div>
          </div>

          {/* Search button */}
          <button type="submit" className="search-button">
            Search
          </button>
        </form>
      </div>

      <KnowledgeGraph />
    </div>
  );
}

export default LeftContainer;