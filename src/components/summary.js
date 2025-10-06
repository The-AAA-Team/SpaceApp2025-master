import './summary.css'

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
        <p class="summary-header">{publicationData.title}</p>
        {/* <hr/> */}
          <p class="summary-paragraph">
            {summaryText}
          </p>
      </div>
    </div>
  );
}

export default Summary;