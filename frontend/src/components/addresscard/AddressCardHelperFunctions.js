export function collectErrorMessages(response){
    let errorArray=[];
    for (let error in response){
        errorArray.push(response[error][0]);
    }
    return errorArray;
}