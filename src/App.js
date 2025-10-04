// import './App.css'

import Footer from './components/footer.js'
import Navbar from './components/header.js'
// import RightContainer from './components/right-container.js'
// import LeftContainer from './components/left-container.js'
// import RightContainer from './components/right-container.js'
import Contents from './components/contents.js'

function App() {
  return (
    <div className="App">
      <Navbar />
      <div className = "main container">
{/* //         <LeftContainer /> */}
{/* //         <RightContainer /> */}
      <Contents />
     </div>
      <Footer />
    </div>
  );
}

export default App;
