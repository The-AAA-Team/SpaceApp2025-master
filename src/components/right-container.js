import './right-container.css'
import publicationsData from './data/publications.json'
import React, { useState } from 'react';

import Summary from './summary.js'

function RightContainer(){
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const [data, setData] = useState(publicationsData);
    const [startIndex, setStartIndex] = useState(0);
    const [endIndex, setEndIndex] = useState(10);

    const slicedData = data.slice(startIndex, endIndex);

    const handleOpenPopup = () => setIsPopupOpen(true);
    const handleClosePopup = () => setIsPopupOpen(false);

    let value = 0;

    const leftArrowClick = () => {
        setStartIndex(prev => Math.max(0, prev - 10));
        setEndIndex(prev => Math.max(10, prev-10));
    }

    const rightArrowClick = () => {
        setStartIndex(prev => Math.min(data.length-10, prev + 10));
        setEndIndex(prev => Math.min(data.length, prev+10));
    }

    return(
        <div class="right-container">
            <div class="page-arrows">
                <button class="arrows" onClick={() => leftArrowClick()}>{"<"}</button>
                <div class="arrows">{Math.ceil(startIndex/10)+1} / {Math.floor(data.length/10)+1}</div>
                <button class="arrows" onClick={() => rightArrowClick()}>{">"}</button>
            </div>
            {slicedData.map((publication,x) => (
                <div class="right-rows" key={x}>
                    <button class="articles" key={x} onClick={handleOpenPopup}>
                        {publication.Title}
                    </button>
                    <Summary isOpen={isPopupOpen} onClose={handleClosePopup}>

                    </Summary>
                </div>
            ))}
            <div class="page-arrows">
                <button class="arrows" onClick={() => leftArrowClick()}>{"<"}</button>
                <div class="arrows">1/68</div>
                <button class="arrows" onClick={() => rightArrowClick()}>{">"}</button>
            </div>
        </div>
    );
}

export default RightContainer;