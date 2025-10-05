import RightContainer from './right-container.js'
import LeftContainer from './left-container.js'
import './contents.css'
import Summary from './summary.js'
import { ContextProvider } from './context'

function Contents(){
    
    return(
        <ContextProvider>
            <div class="contents-main">
                <Summary>

                </Summary>
                <LeftContainer />
                <RightContainer />
            </div>
        </ContextProvider>
    );
}

export default Contents;