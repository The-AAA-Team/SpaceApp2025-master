import './right-container.css'
import publicationsData from './data/publications.json'
import React, { useState, useEffect } from 'react'
import Summary from './summary.js'
import { Context } from './context'
import axios from 'axios'

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

    const Summarizer = () => {
        const [title, setTitle] = useState('');
        const [summary, setSummary] = useState('');
        const [loading, setLoading] = useState(false);
        const [error, setError] = useState(null);

        const handleSubmit = async (e) => {
            e.preventDefault();
            setLoading(true);
            setSummary('');
            setError(null);

            const FLASK_API_URL = 'https://localhost:5000/summarize'

            try {
            const response = await axios.post(FLASK_API_URL, {
                title: openPublicationId
            })
            } catch (err) {
                console.log('API Error:', err);
            } finally {
                setLoading(false);
            }
        }
    };

    const slicedData = data.slice(startIndex, endIndex);

    const [openPublicationId, setOpenPublicationId] = useState(null);    

    const handleOpenPopup = (id) => {
        setOpenPublicationId(id);
    };
    const handleClosePopup = () => {
        setOpenPublicationId(null);
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
                        <Summary isOpen={true} onClose={handleClosePopup} publicationData={publication}>
                            
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