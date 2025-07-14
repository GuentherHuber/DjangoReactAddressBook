import {useState,useEffect} from 'react';
import AddressCard from "../addresscard/AddressCard";
import { loadDataFromBackend} from "./AddressbookBackendApi";
import "./Addressbook.css"

function Addressbook(){
    const [addresses, setAddresses]=useState([]);
    const [editId, setEditId]=useState(null);
    const [newCardVisible, setNewCardVisible]=useState(false);
    const [searchTerm, setSearchTerm]=useState("");
    
    //Wird zu Beginn einmal ausgeführt
    useEffect(function(){
        loadDataFromBackend()
        .then(function(result){
            if(result.success){
                setAddresses(result.response);
            }
            else{
              setAddresses([]);
            }
        })
    },[])

    function addNewAddress(newAddressJson){
      const copyAddresses=[...addresses]
      copyAddresses.push(newAddressJson);
      setAddresses(copyAddresses);
    }

    function deleteAddressById(id){
      setAddresses(function(prev){
        return prev.filter(function(address){
          return address.id!==id;
        })
      })
    }

    function handleEditId(id){
      setEditId(id);
      if(id===null){
        setNewCardVisible(false);
      }
    };

    function onClickButtonNewAddress(event){
      setEditId("neu");
      setNewCardVisible(true);
    };

    function onChangeSearchTerm(event){
        setSearchTerm(event.target.value);
    }

    const filteredAddresses = addresses.filter(function(address){
      return(
        address.first_name.toLowerCase().includes(searchTerm)||
        address.last_name.toLowerCase().includes(searchTerm)||
        address.city.toLowerCase().includes(searchTerm)||
        address.street_name.toLowerCase().includes(searchTerm)||
        address.house_number.toLowerCase().includes(searchTerm)||
        address.postcode.toString().toLowerCase().includes(searchTerm)
      )
    })
    
    return (
    <div>
      <div className="headerContainer">
        <h1>Willkommen zum Adressbuch</h1>
        <button onClick={onClickButtonNewAddress}>Neue Adresse hinzufügen</button>
        <input className="inputSearch" name="searchTerm" placeholder="Suche"  value={searchTerm} onChange={onChangeSearchTerm}/>
      </div>
      <div className="addressCardContainer">
        {newCardVisible &&
          <AddressCard
            id={"new"}
            first_name=""
            last_name=""
            city=""
            street_name=""
            house_number=""
            postcode=""
            handleEditId={handleEditId}
            editId={"new"}
            addNewAddress={addNewAddress}
          />
        }
        {filteredAddresses.map(function(address){
          return(
            <AddressCard
              key={address.id}
              id={address.id}
              first_name={address.first_name}
              last_name={address.last_name}
              city={address.city}
              street_name={address.street_name}
              house_number={address.house_number}
              postcode={address.postcode}
              profile_picture={address.profile_picture}
              deleteAddressById={deleteAddressById}
              handleEditId={handleEditId}
              editId={editId}
            />
          )
        })}
      </div>
    </div>
  );
}

export default Addressbook