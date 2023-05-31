import './App.css';
import Home from './pages/Home';
import StockPresentation from './pages/StockPresentation';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/stockpresentation" element={<StockPresentation/>} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
