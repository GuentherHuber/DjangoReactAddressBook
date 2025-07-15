import './App.css';
import React, {useEffect} from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Welcome from './components/common/Welcome';
import Navbar from './components/common/Navbar';

import Addressbook from './components/addressbook/Addressbook';

/*function App() {
  

  

  return (
    <div>
      {addresses.map(function(address){
        return(
          <AddressCard
            key={address.id}
            first_name={address.first_name}
            last_name={address.last_name}
            city={address.city}
            street_name={address.street_name}
            house_number={address.house_number}
            postcode={address.postcode}
            profile_picture={address.profile_picture}
          />
        )
      })}
    </div>
  );
}*/

function App(){

  
  /*useEffect(function(event){
    fetch('http://127.0.0.1:8000/addressbook/api/')
    .then(function(response){
      return response.json();
    })
    .then(function(data){
      //setAddresses(data);
    })
    .catch(function(error){
      console.error("Fehler beim Laden");
    })
  },[])*/

  return(
    <Router>
      <Navbar/>
      <Routes>
        <Route path="/" element={<Welcome/>}/>
        <Route path="/addressbook" element={<Addressbook/>} />
      </Routes>
    </Router>

  )
}

export default App;
