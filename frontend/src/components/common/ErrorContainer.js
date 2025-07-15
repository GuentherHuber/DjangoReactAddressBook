import './ErrorContainer.css'

function ErrorContainer(errorProp){
    return(
        <div className="errorContainer">
            <ul>
                {errorProp.errorMessages.map(function(message,index){
                    return <li key={index}>{message}</li>
                })}
            </ul>
        </div>
    )
}

export default ErrorContainer