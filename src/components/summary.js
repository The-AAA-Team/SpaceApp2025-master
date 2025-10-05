import './summary.css'
import PublicationSummary from './data/publicationsummary.json'

const Summary = ({isOpen, onClose, publicationData}) => {

  if (!isOpen || !publicationData){
    return null;
  }
  return (
    <div class="sumarry-main">
      <button class="close-button" onClick={onClose}>
          X
      </button>
      <div class="summary-content">
        <p class="summary-header">{publicationData.Title}</p>
        {
          PublicationSummary.map((summary) => (
            <p class="summary-paragraph">
              {publicationData.Title.toLowerCase() === summary.title.toLowerCase && (
                <p>summary.summary</p>
              )}
            </p>
          ))
        }
      </div>
    </div>
  );
}

export default Summary;