import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    //StrictMode entfernt ansonsten gibt es Probleme beim rendern (Rendert alles doppelt)
    <App />
);
