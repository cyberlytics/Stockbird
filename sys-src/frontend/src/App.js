import './App.css';
import logo from './assets/Stockbird-Logo.png';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

function App() {
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
            .then(result => console.log(JSON.parse(result).body))
            .catch(error => console.log('error', error));
    }
  return (

        <div className="App">
          <header className="App-header">
            <img src={logo} alt="Stockbird Logo"/>
          </header>
            <body>
            <form>
                <label><Typography variant="body1">Search stocks:</Typography></label>
                <input type="text" id="symbol"></input>
                <Button variant="contained" onClick= {callAPI("META")}>OK</Button>
            </form>
            </body>
        </div>
  );
}

export default App;
