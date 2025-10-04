// import './App.css'

import Footer from './components/footer.js'
import Navbar from './components/navbar.js'
import RightContainer from './components/right-container.js'
import LeftContainer from './components/left-container.js'

function App() {
  return (
    <div className="App">
      <Navbar />
      <div className = "main container">
        <LeftContainer />
        <RightContainer />
      </div>
      <Footer />
    </div>
  );
}

export default App;
