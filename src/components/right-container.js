import './right-container.css'
import publicationsData from './data/publications.json'
import React, { useState } from 'react';

import Summary from './summary.js'

function RightContainer(){
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const handleOpenPopup = () => setIsPopupOpen(true);
    const handleClosePopup = () => setIsPopupOpen(false);

    return(
        <div class="right-container">
            {publicationsData.slice(0,10).map((publication,x) => (
                <div class="right-rows" key={x}>
                    <button class="articles" key={x} onClick={handleOpenPopup}>
                        {publication.Title}
                    </button>
                    <Summary isOpen={isPopupOpen} onClose={handleClosePopup}>
                        
                    </Summary>
                </div>
            ))}
        </div>
    );
}

export default RightContainer;