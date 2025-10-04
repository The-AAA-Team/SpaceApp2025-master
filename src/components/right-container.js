import './right-container.css'
import publicationsData from './data/publications.json'

function RightContainer(){
    return(
        <div class="right-container">
            {publicationsData.slice(0,10).map(publication => (
            <div class="right-rows">
                {publication.Title}
            </div>
            ))}
        </div>
    );
}

export default RightContainer;