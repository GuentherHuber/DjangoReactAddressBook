export function collectErrorMessages(response){
    let errorArray=[];
    if(Array.isArray(response)){
        console.log("isArray")
        response.forEach(function(value){
            errorArray.push(value)
        })
    }
    else{
       for(let [key] of Object.entries(response)){
            errorArray.push(response[key])
       }
    }
    return errorArray;
}