import React, { useState } from 'react';
import logo from '../assets/Stockbird-Logo.png';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import {useNavigate} from "react-router-dom";

export default function Home() {

    const navigate = useNavigate();

    const callAPI = (symbol) => {
        // instantiate a headers object
        var myHeaders = new Headers();
        // add content type header to object
        myHeaders.append("Content-Type", "application/json");
        // using built-in JSON utility package turn object to string and store in a variable
        var raw = JSON.stringify({ "symbol": symbol });
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
                const parsedResult = JSON.parse(result).body;
                //Hier nochmal parsen ansonsten gibt es Probleme mit StockPresentation
                const parsedResult2 = JSON.parse(parsedResult)
                //Variable wird hier übergeben und nicht in dem anderen Component in ein JSON-Object umgewandelt
                navigate('/stockpresentation', {state: parsedResult2});
            })
            .catch(error => console.log('error', error));
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
                        <Button variant="contained" onClick={() => callAPI("META")}>OK</Button>
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