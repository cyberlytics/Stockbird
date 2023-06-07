import '../App.css';
import logo from '../assets/Stockbird-Logo.png';
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useLocation, useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function StockPresentation() {
    const location = useLocation();
    const jsonDataString = location.state;
    const jsonData = JSON.parse(jsonDataString);

    const [tweetData, setTweetData] = useState('');

    const chartRef = useRef(null);


    const [data, setData] = useState('');
    //let data = [];

    useEffect(() => {
        //Wenn die Daten verfügbar sind dann zeichne den Graphen
        if (jsonData) {
            drawChart();
        }
    }, []); // Pass `jsonData` as a dependency to the useEffect hook

    const drawChart = () => {

        const jsonDataClose = jsonData.Close;
        // Die Zeitangaben in der JSON-Datei sind vom Typ UNIX und werden entsprechend umgewandelt
        const data = Object.entries(jsonDataClose).map(([timestamp, value]) => ({
            timestamp: parseInt(timestamp),
            value: parseFloat(value),
        })).filter(dataPoint => !isNaN(dataPoint.value));

        // Styling festlegen
        const margin = { top: 70, right: 30, bottom: 30, left: 40 };
        const width = 800 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        const svg = d3
            .select(chartRef.current)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        const xScale = d3
            .scaleTime()
            .domain(d3.extent(data, d => d.timestamp))
            .range([0, width]);

        const yScale = d3
            .scaleLinear()
            .domain(d3.extent(data, d => d.value))
            .range([height, 0]);

        const xAxis = d3.axisBottom(xScale);
        const yAxis = d3.axisLeft(yScale);

        svg.append('g').attr('transform', `translate(0,${height})`).call(xAxis);
        svg.append('g').call(yAxis);

        const line = d3
            .line()
            .x(d => xScale(d.timestamp))
            .y(d => yScale(d.value));

        svg
            .append('path')
            .datum(data)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 1.5)
            .attr('d', line);
    };

    const callAPI = async (control, substring) => {
        // instantiate a headers object
        var myHeaders = new Headers();
        // add content type header to object
        myHeaders.append('Content-Type', 'application/json');
        // using built-in JSON utility package turn object to string and store in a variable
        var raw = JSON.stringify({ control: control, substring: substring });
        // create a JSON object with parameters for API call and store in a variable
        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow',
        };

        // make API call with parameters and use promises to get response
        fetch('https://szlw5m95d9.execute-api.eu-central-1.amazonaws.com/dev', requestOptions)
            .then(response => response.text())
            .then(result => {
                try {
                    const parsedResult = JSON.parse(result).body;
                    const parsedResult2 = JSON.parse(parsedResult);
                    if (control === '_query_tweets_by_substring') {
                        setTweetData(parsedResult2);
                        const jsonDataTweet = JSON.parse(tweetData);
                        setData(jsonDataTweet.data)
                        console.log(data);
                    }
                } catch (error) {
                    console.log('Error parsing JSON:', error);
                }
            })
            .catch(error => console.log('Error fetching data:', error));
    };

    return (
        <>
            <div className="stockPresentation">
                <img className="Centered-img" id="splogo" src={logo} alt="Stockbird Logo" />
                <Typography variant="h3">Name of Stock</Typography>
                <div ref={chartRef}></div>
                <Button variant="contained" onClick={() => callAPI('_query_tweets_by_substring', 'META')}>
                    Analyze
                </Button>
            </div>

            <div className="tweetData">
                {data && data.length > 0 && (
                    <>
                        {data.map((row, index) => (
                            <div key={index}>
                                <p>{row[0]}</p>
                                <p>{row[2]}</p>
                                <p>{row[3]}</p>
                            </div>
                        ))}
                    </>
                )}
            </div>

        </>
    );
}