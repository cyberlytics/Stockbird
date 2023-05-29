import React from 'react';
import { useLocation } from 'react-router-dom';


/*Json-File wird hier uebergeben und mit d3.js visualisiert*/
export default function StockPresentation () {
    const location = useLocation();
    const jsonData = location.state;


    //Zeitangabe im JSON File ist in UNIX --> "1198796400000" als "KEY" stellt diese Zeitangabe dar: 27, 2008, at 14:00:00 UTC.
    console.log('jsonData type:', typeof jsonData);

    return (
        <div>
            <p>Stock Presentation</p>
        </div>
    );
};