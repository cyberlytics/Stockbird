import React from 'react';
import {useNavigate} from "react-router-dom";
import logo from '../assets/Stockbird-Logo.png';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function Home() {

    const navigate = useNavigate();

    const callAPI = (control, symbol) => {

        // instantiate a headers object
        var myHeaders = new Headers();
        // add content type header to object
        myHeaders.append("Content-Type", "application/json");
        // using built-in JSON utility package turn object to string and store in a variable
        var raw = JSON.stringify({ "control": control, "symbol": symbol });
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
            .then(result => {
                try {
                    const parsedResult = JSON.parse(result).body;
                    const parsedResult2 = JSON.parse(parsedResult);
                    if (control === "_get_stock_data") {
                        console.log(parsedResult2);
                        navigate('/stock-presentation', { state: parsedResult2 });
                    }
                } catch (error) {
                    console.log('Error parsing JSON:', error);
                }
            })
            .catch(error => console.log('Error fetching data:', error));
    }

    return (
        <>
            <div className="App">
                <header className="App-header">
                    <img className="Centered-img" src={logo} alt="Stockbird Logo" />
                    <div className="Centered-div">
                        <Typography variant="body1">
                            Welcome to Stockbird, where you can find out how relevant tweets influence the stock market.
                        </Typography>
                    </div>
                </header>
                <div className="Centered-div" id="Colored-search">
                    <form className="Stock-search">
                        <input id="symbol" type="text" placeholder="Search stocks by symbol (e. g. META)" />
                        <Button variant="contained" onClick={() => callAPI("_get_stock_data", "META")}>OK</Button>
                    </form>
                </div>
                <footer className="footer">
                    <Typography variant='body2' align='center' gutterBottom>
                        © 2023 Stockbird.
                    </Typography>
                    <Typography variant='subtitle2' align='center' color="textSecondary">
                        Impressum
                    </Typography>
                </footer>
            </div>
        </>
    )
}