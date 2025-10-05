import './summary.css'
import PublicationSummary from './data/publicationsummary.json'

const Summary = ({isOpen, onClose, publicationData, summaryText}) => {

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
          <p class="summary-paragraph">
            {summaryText}
          </p>
      </div>
    </div>
  );
}

export default Summary;