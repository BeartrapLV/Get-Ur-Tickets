import React, { useState, useContext } from 'react';
import PropTypes from 'prop-types'; // Import PropTypes
import airportData from '../airportData_flatui.json'; // Import JSON
import { LocationContext } from '../index';           // Import context
import '../AirportSearchBar.css';
import SearchBar from './SearchBar';
export var test = "";
export var test2 ="";
const AirportSearchBar = ({ onSelect }) => {
  const {location, setLocation } = useContext(LocationContext);
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredAirports, setFilteredAirports] = useState([]);

  SearchBar.originAirportCode = location;
  const airports = airportData; // Imported JSON data

  const handleSearch = (event) => {
    const term = event.target.value;
    setSearchTerm(term);

    // Clear the populated suggestions if the user has not entered anything
    if (term.trim() === '') {
      setFilteredAirports([]);
      return;
    }

  
    // Filter out municipality (city) and iata code (airport code)
    const filtered = airports.filter(airport =>
      (airport.municipality && airport.municipality.toLowerCase().includes(term.toLowerCase())) ||
      (airport.iata_code && airport.iata_code.toLowerCase().includes(term.toLowerCase())) ||
      (airport.name && airport.name.toLowerCase().includes(term.toLowerCase()))
    );
    setFilteredAirports(filtered);
  };
  
  const handleSelect = (airport) => {
    setSearchTerm(airport.name);
    setFilteredAirports([]);
    setLocation(airport);
    if (onSelect) onSelect(airport);
    test = airport.iata_code;
    test2 = airport.name + " (" + airport.iata_code + ")";
    console.log(airport);
  };

  return (
    <div className="Airport-search-bar">
      <div className='description' >Enter your Home Airport. Currently set to: {test2}</div>
      <input
        style={{width: '42%', alignItems: 'center'}}
        type="text"
        value={searchTerm}
        onChange={handleSearch}
        placeholder="Search for an airport..."
      />
      {searchTerm && filteredAirports.length > 0 && (
        <div className="suggestions" >
          {filteredAirports.map((airport) => (
            <button 
              key={airport.iata_code || airport.municipality || airport.name}
              onClick={() => handleSelect(airport)}
              
            >
              {airport.name} ({airport.iata_code})
            </button>
          ))}
        </div>
      )}
      <br/>
      <div className='description'>Search for an Event.</div>
    </div>
  );
};

AirportSearchBar.propTypes = {
  onSelect: PropTypes.func.isRequired, // onSelect is required and should be a function
};

export default AirportSearchBar;