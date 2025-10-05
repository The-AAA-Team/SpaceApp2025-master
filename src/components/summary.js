import './summary.css'
import React from 'react'

const Summary = ({isOpen, onClose, children}) => {
  if (!isOpen){
    return null;
  }
  return (
    <div class="sumarry-main" onClick={onClose}>
      {children}
      <button class="close-button" onClick={(e) => e.stopPropagation()}>
          X
      </button>
      <div class="summary-content" onClick={onClose}>
        <p class="summary-header">Heading</p>
        <p class="summary-paragraph">Content</p>
      </div>
    </div>
  );
}

export default Summary;