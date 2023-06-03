import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { useLocation } from 'react-router-dom';

export default function StockPresentation() {

    const location = useLocation();
    const jsonDataString = location.state;
    const jsonData = JSON.parse(jsonDataString);

    const chartRef = useRef(null);

    useEffect(() => {
        //Wenn die Daten verfügbar sind dann zeichne den Graphen
        if (jsonData) {
            drawChart();
        }
    });

    const drawChart = () => {
        //Die Zeitangaben in der JSON-Datei ist vom typ UNIX, wird entsprechend umgewandelt mit dieser Methode
        const data = Object.entries(jsonData.Close).map(([timestamp, value]) => ({
            timestamp: parseInt(timestamp),
            value: parseFloat(value),
        }));

        //Styling festlegen
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

    return <div ref={chartRef}></div>;
}
