import './App.css';
import Home from './pages/Home';
import Impressum from './pages/Impressum';
import InfluencePresentation from './pages/InfluencePresentation';
import StockPresentation from './pages/StockPresentation';

function App() {
    let page
    switch (window.location.pathname) {
      case "/":
        page = <Home />
        break
      case "/impressum":
        page = <Impressum />
        break
      case "/influence-presentation":
        page = <InfluencePresentation />
        break
      case "/stock-presentation":
        page = <StockPresentation />
        break
      default:
        page = <Home />
    }

    return (
      <>
        {page}
      </>
    )
}

export default App;
