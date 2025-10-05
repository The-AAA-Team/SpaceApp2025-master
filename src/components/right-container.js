import './right-container.css'
import publicationsData from './data/publications.json'
import React, { useState, useEffect } from 'react'
import Summary from './summary.js'
import { Context } from './context'

function RightContainer(){

    const [data, setData] = useState(publicationsData);
    const [startIndex, setStartIndex] = useState(0);
    const [endIndex, setEndIndex] = useState(10);

    const { JSONData } = Context();

    useEffect(() => {
        if (!JSONData) {
            return;
        }
        if (JSONData.keyword.length === 0){
            setData(publicationsData); //useless for 
        }
        else{
            const filteredList = publicationsData.filter((publication) => {
                return publication.Title.toLowerCase().includes(JSONData.keyword.toLowerCase());
            });
            setData(filteredList);
            console.log(filteredList);
            setStartIndex(0);
            setEndIndex(Math.min(filteredList.length, 10));
        }
    }, [JSONData]);

    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSendToBackend = async (publicationTitle) => {
        setLoading(true);
        setSummary('');
        try {
            const res = await fetch('http://localhost:5000/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ title: publicationTitle}),
            });

            if (!res.ok){
                throw new Error(`HTTP Error! Status: ${res.status}`);
            }

            const response = await res.json();
            setSummary(response.summary)
        }
        catch (error) {
            setSummary('Error: Could not connect to backend');
        }
        finally {
            setLoading(false);
        }
    };

    const slicedData = data.slice(startIndex, endIndex);

    const [openPublicationId, setOpenPublicationId] = useState(null);    

    const handleOpenPopup = (id) => {
        setOpenPublicationId(id);
        handleSendToBackend(id);
    };
    const handleClosePopup = () => {
        setOpenPublicationId(null);
        setSummary('');
    };

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
                <div class="arrows">{Math.ceil(startIndex/10)+1} / {Math.ceil(data.length/10)}</div>
                <button class="arrows" onClick={() => rightArrowClick()}>{">"}</button>
            </div>
            {slicedData.map((publication,x) => (
                <div class="right-rows" key={publication.Title}>
                    <button class="articles" key={x} onClick={() => handleOpenPopup(publication.Title)}>
                        {publication.Title}
                    </button>
                    {publication.Title === openPublicationId && (
                        <Summary 
                        isOpen={true} 
                        onClose={handleClosePopup} 
                        publicationData={publication}
                        summaryText={summary}
                        isLoading={loading}>
                        </Summary>
                    )}
                </div>
            ))}
            <div class="page-arrows">
                <button class="arrows" onClick={() => leftArrowClick()}>{"<"}</button>
                <div class="arrows">{Math.ceil(startIndex/10)+1} / {Math.ceil(data.length/10)}</div>
                <button class="arrows" onClick={() => rightArrowClick()}>{">"}</button>
            </div>
        </div>
    );
}

export default RightContainer;