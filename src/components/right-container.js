import './right-container.css'
import publicationsData from './data/publications.json'

function RightContainer(){
    return(
        <div class="right-container">
            {publicationsData.slice(0,10).map(publication => (
                <div class="right-rows">
                    <a href="">
                        {publication.Title}
                    </a>
                </div>
            ))}
        </div>
    );
}

export default RightContainer;