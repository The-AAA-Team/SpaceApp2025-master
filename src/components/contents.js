import RightContainer from './right-container.js'
import LeftContainer from './left-container.js'
import './contents.css'

function Contents(){
    return(
        <div class="contents-main">
            <LeftContainer />
            <RightContainer />
        </div>
    );
}

export default Contents;