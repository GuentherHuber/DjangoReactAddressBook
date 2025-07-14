const apiUrl= process.env.REACT_APP_API_URL;

export function loadDataFromBackend(){
    return fetch(apiUrl,{
        method:"GET"
    })

    .then(function(response){
        if(!response.ok){
            return response.json()
            .then(function(errorData){
                return{success:false,response:errorData};
            })
        }
        else{
            return response.json()
            .then(function(data){
                return{success:true,response:data}
            })
        }
    })
    .catch(function(error){
        return{success:false,response:error};
    })
}

//Method DELETE sendet als Antwort kein JSON. Daher nicht respsonse.json()
export function deleteAddressInBackend(id){
    return fetch(apiUrl+"/"+id+"/",{
        method:"DELETE",
        headers:{"Content-Type":"application/json"},
    })
    .then(function(response){
        if(!response.ok){
            return{success:false,response:response}
        }

        else{
            return {success:true,response:response}
        }            
    })
    .catch(function(error){
        return{success:false,response:error};
    })
}

export function updateBackendData(formData){
    return fetch(apiUrl+formData.get("id")+"/",{
        method:"PATCH",
        body:formData
    })
    .then(function(response){
        if(!response.ok){
            return response.json()
            .then(function(errorData){
                return{success:false,response:errorData};
            })
        }
        else{
            return response.json()
            .then(function(data){
                return{success:true,response:data};
            })
        }
    })
    .catch(function(error){
        return{success:false,response:error};
    })
}

export function addNewAddressToBackend(formData){
    return fetch(apiUrl,{
        method:"POST",
        body:formData,
    })
    .then(function(response){
        if(!response.ok){
            return response.json()
            .then(function(errorData){
                return {success:false,response:errorData};
            })
        }
        else{
            return response.json()
            .then(function(data){
                return {success:true,response:data};
            })
        }
    })
    .catch(function(error){
        return {success:false,response:error};
    })
}
  

