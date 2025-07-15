import "./AddressCard.css"
import { useState } from "react";
import { updateBackendData,addNewAddressToBackend,deleteAddressInBackend} from "../addressbook/AddressbookBackendApi";

function AddressCard({id,first_name,last_name,city,street_name,house_number,postcode,profile_picture,
                        deleteAddressById, handleEditId,editId,addNewAddress}){

    const [form,setForm]=useState({id,first_name,last_name,city,street_name,house_number,postcode,profile_picture});
    const [prevForm,setPrevForm]=useState({id,first_name,last_name,city,street_name,house_number,postcode,profile_picture});

    function onClickButtonDelete(){
        deleteAddressInBackend(form.id)
        .then(function(respsonse){
            if(!respsonse.success){
                //Es muss eine Fehlermeldung angezeigt werden
            }
            else{
                deleteAddressById(form.id);
            }
        })
        
    }

    function onClickButtonEdit(){
        handleEditId(form.id);
    }

    function onClickButtonSave(){
        //Neue Adresse wird gespeichert
        if(id==="new"){
            const formData=new FormData();
            console.log(profile_picture);
            for(let key in form){
                if(key==='id'){//Id für neue Adresse ist "new". Id wird beim Anlegen per POST automtisich vergeben und wird daher hier ignoriert
                    continue;
                }
                if(key==='profile_picture' && !(form[key] instanceof File)){//Wenn kein Bild angegeben ist, wird profile_picture nicht an formData angehängt
                    continue;
                }
                formData.append(key,form[key]);
            }
            addNewAddressToBackend(formData)
            .then(function(response){
                if(!response.success){
                    //Es muss eine Fehlermeldung angezeigt werden
                }
                else{
                    addNewAddress(response.response);
                    setPrevForm(response.response);
                    handleEditId(null);                    
                }
            })
            return;
        }
        //Änderung an bestehender Adresse wird gespeichert
        else{
            const formData=new FormData();
            for(let key in form){
                if((key==='profile_picture' && !(form[key] instanceof File))){ //Wenn kein Bild (neues) angegeben ist, wird profile_picture nicht an formData angehängt
                    continue;
                }
                formData.append(key,form[key]);
            }        
            updateBackendData(formData)
            .then(function(response){
                if(!response.success){
                    setForm(prevForm);
                }
                else{                                        
                    setForm(response.response);
                    setPrevForm(form);
                    handleEditId(null);
                }
            })
        }
    }

    function onClickButtonAbort(){
        setForm(prevForm);
        handleEditId(null);
    }

    function onChange(event){
        const copyForm={...form};
        copyForm[event.target.name]=event.target.value;
        setForm(copyForm);
    }

    function onSelectProfilePicture(event){
        let copyForm={...form};
        copyForm.profile_picture=event.target.files[0];
        setForm(copyForm);
    }

    if(editId===id){
        return(
            <div className="addressCard">
                <div className="addressContent">
                    <div className="inputRow">
                        <label htmlFor="vorname">Vorname: </label>
                        <input name="first_name" value={form.first_name} onChange={onChange}/>
                        
                    </div>
                    <div className="inputRow">
                        <label htmlFor="Nachname">Nachname: </label>   
                        <input name="last_name" value={form.last_name} onChange={onChange}/>
                        
                    </div>
                    <div className="inputRow">
                        <label htmlFor="strasse">Strasse: </label>
                        <input name="street_name" value={form.street_name} onChange={onChange}/>
                        
                    </div>
                    <div className="inputRow">
                        <label htmlFor="strasse">Hausummer: </label>
                        <input name="house_number" value={form.house_number} onChange={onChange}/>
                    </div>
                    <div className="inputRow">
                        <label htmlFor="stadt">Stadt: </label>
                        <input name="city" value={form.city} onChange={onChange}/>
                        
                    </div>
                    <div className="inputRow">
                        <label htmlFor="plz">PLZ: </label>
                        <input name="postcode" value={form.postcode} onChange={onChange}/><br></br>
                        
                    </div>
                    <div className="buttonRow">
                        <button name="buttonSave" onClick={onClickButtonSave}>Speichern</button>
                        <button name="buttonAbort" onClick={onClickButtonAbort}>Abbrechen</button>
                    </div>
                    <div className="buttonRow">
                        <input type="file" accept="image/*" onChange={onSelectProfilePicture}/>
                    </div>
                </div>
            </div>
        )
    }

    else{
        return(
            <div className="addressCard">
                {<img src={form.profile_picture} alt="profilePicture" className="profilePicture"/>}
                <div className="addressContent">                    
                    <h3>{form.first_name} {form.last_name} </h3>
                    <p>{form.street_name} {form.house_number}</p>
                    <p>{form.postcode} {form.city}</p>
                    <div className="buttonRow">
                        <button onClick={onClickButtonEdit}>Bearbeiten</button>
                        <button onClick={onClickButtonDelete}>Löschen</button>
                    </div>
                </div>
            </div>
        )
    }
}

export default AddressCard