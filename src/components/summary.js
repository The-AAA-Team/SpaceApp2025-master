import './summary.css'
import './data/publicationsummary.json'

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
        <p class="summary-paragraph">Content</p>
      </div>
    </div>
  );
}

export default Summary;