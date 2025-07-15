import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Welcome from './components/common/Welcome';
import Navbar from './components/common/Navbar';

import Addressbook from './components/addressbook/Addressbook';

function App(){

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
