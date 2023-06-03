import './App.css';
import Home from './pages/Home';
import Impressum from './pages/Impressum';
import InfluencePresentation from './pages/InfluencePresentation';
import StockPresentation from './pages/StockPresentation';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/impressum" element={<Impressum />} />
        <Route path="/influence-presentation" element={<InfluencePresentation />} />
        <Route path="/stock-presentation" element={<StockPresentation />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
