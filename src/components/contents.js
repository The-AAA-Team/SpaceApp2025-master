import RightContainer from './right-container.js'
import LeftContainer from './left-container.js'
import './contents.css'
import Summary from './summary.js'

function Contents(){
    return(
        <div class="contents-main">
            <Summary />
            <LeftContainer />
            <RightContainer />
        </div>
    );
}

export default Contents;