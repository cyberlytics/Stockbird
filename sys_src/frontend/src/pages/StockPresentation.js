import '../App.css';
import logo from '../assets/Stockbird-Logo2.png';
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useLocation, Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material/styles';
import { LocalizationProvider } from '@mui/x-date-pickers-pro';
import { AdapterDayjs } from '@mui/x-date-pickers-pro/AdapterDayjs';
import { DateRangePicker } from '@mui/x-date-pickers-pro/DateRangePicker';
import { callAPITweets } from './api'; // Import the callAPI function

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary
}));

export default function StockPresentation() {

    //location contains a JSON-Files, the stock-data and the symbol of the Stock
    const location = useLocation();
    //Both can be accessed with location.state
    //parsedResult2 contains the stockData and symbol is the Symbol name of the Stock (Used for visualizing and mapping)
    const { parsedResult2, symbol } = location.state;
    //jsonDataString is a string which contains the stockData as a String, which has to be converted into a JSON-File
    const jsonDataString = parsedResult2;
    //jsonData contains the stock-data as a jsonType Object
    const jsonData = JSON.parse(jsonDataString);

    //Both tweetData and data is used to store the tweets which we get from api.js
    //state allows to store and manage data that can change over time, which in this case does everytime when the user wants to see new Stocks
    const [tweetData, setTweetData] = useState('');
    const [data, setData] = useState('');

    //useRef allows the manipulation of the DOM, where we plot the stock if data is available
    const chartRef = useRef(null);

    //here we map our symbols to the corresponding name of the Company which is necessary for receiving the right tweets
    const symbolMapping = {
        TSLA: 'Tesla',
        AAPL: 'Apple',
        GOOG: 'Google',
        'DOGE-USD': 'Dogecoin',
        'BTC-USD': 'Bitcoin'
    };

    //in this variable we store in the symbol because in the api.js we need a substring for the backend for filtering the tweets where for example 'Dogecoin' is included the tweet
    const secondParameter = symbolMapping[symbol];

    //draws the chart when the stock-data is available
    useEffect(() => {
        if (jsonData) {
            drawChart();
        }
        //Here if the json-data would change then we could pass in here the jsonData but that's not necessary otherwise it will get drawn twice if we press on the 'analyze' button
    }, []);

    const drawChart = () => {
        //'Close' includes the information we want to plot to the screen
        //Other attributes are for example: Open,High,Low,Volume,Dividends,Stock Splits
        const jsonDataClose = jsonData.Close;
        // Die Zeitangaben in der JSON-Datei sind vom Typ UNIX und werden entsprechend umgewandelt
        //the timestamps have the type of UNIX, with this map function we iterate through each element and parse the values from the 'Close' attribute
        const data = Object.entries(jsonDataClose).map(([timestamp, value]) => ({
            timestamp: parseInt(timestamp),
            value: parseFloat(value),
            //filtering data where the data is NaN
        })).filter(dataPoint => !isNaN(dataPoint.value));

        // Some Styling of the d3 plot
        const margin = { top: 70, right: 30, bottom: 30, left: 40 };
        const width = 800 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        //here we select the chartRef as we assigned it before to manipulate the DOM
        const svg = d3
            .select(chartRef.current)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        //x-axis is being scaled based on the timestamps in the data
        const xScale = d3
            .scaleTime()
            .domain(d3.extent(data, d => d.timestamp))
            .range([0, width]);

        //y-axis is being scaled based on the values in the data
        const yScale = d3
            .scaleLinear()
            .domain(d3.extent(data, d => d.value))
            .range([height, 0]);

        //creating the x-axis and y-axis
        const xAxis = d3.axisBottom(xScale);
        const yAxis = d3.axisLeft(yScale);

        svg.append('g').attr('transform', `translate(0,${height})`).call(xAxis);
        svg.append('g').call(yAxis);

        //plot should be a line
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

    //this function gets triggered when the 'Analyze' button is clicked
    //with this function we call the 'callAPITweets' which is defined in the 'api.js'
    //we store all the information we get from the 'callAPITweets' in the jsonDataTweet
    const handleAnalyzeClick = async () => {
        try {
            const apiTweets = await callAPITweets('_query_tweets_by_substring', secondParameter);
            //here we set the tweetData value to the tweets we get back, but here are some information we don't need like
            setTweetData(apiTweets);
            const jsonDataTweet = JSON.parse(tweetData);
            //here we only select the 'data' attribute and not the column names
            setData(jsonDataTweet.data);
        } catch (error) {
            console.log('Error during API call:', error);
        }
    };

    return (
        <>
            <div>
              <div className="spHeader">
                <Link to="/">
                  <img id="splogo" src={logo} alt="Stockbird Logo" />
                </Link>
              </div>
              <div className='stockPresentation'>
                <Stack
                    direction="row"
                    divider={<Divider orientation="vertical" flexItem />}
                    spacing={2}
                  >
                    <div>
                      <Typography variant="h3">{symbol}</Typography>
                      <div ref={chartRef}></div>
                      <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DateRangePicker className="datePicker" localeText={{ start: 'Twitter analysis start', end: 'Twitter analysis end' }} />
                      </LocalizationProvider>
                      <Button id="analyzeBtn" variant="contained" onClick={handleAnalyzeClick}>
                        Analyze
                      </Button>
                    </div>
                    <div>
                      <Stack spacing={2}>
                        <Item> 
                          <Typography variant='body2'>
                            Tweet 1 Preview
                          </Typography>
                        </Item>
                        <Item> 
                          <Typography variant='body2'>
                            Tweet 2 Preview
                          </Typography>
                        </Item>
                        <Item> 
                          <Typography variant='body2'>
                            Tweet 3 Preview
                          </Typography>
                        </Item>
                      </Stack>
                    </div>
                  </Stack>
              </div>
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
