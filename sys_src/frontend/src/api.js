
    var callAPI = (symbol)=>{
        // instantiate a headers object
        var myHeaders = new Headers();
        // add content type header to object
        myHeaders.append("Content-Type", "application/json");
        // using built in JSON utility package turn object to string and store in a variable
        var raw = JSON.stringify({"symbol":symbol});
        // create a JSON object with parameters for API call and store in a variable
        var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
};
    // make API call with parameters and use promises to get response
    fetch("https://szlw5m95d9.execute-api.eu-central-1.amazonaws.com/dev", requestOptions)
    .then(response => response.text())
    .then(result => console.log(JSON.parse(result.body)))
    .catch(error => console.log('error', error));
}
