import React, { createContext, useState, useContext } from 'react';

const DataContext = createContext(null);

export const ContextProvider = ({ children }) => {
  const [sharedData, setSharedData] = useState(null);

  const contextValue = {
    JSONData: sharedData,    
    setJSONData: setSharedData,  
  };

  return (
    <DataContext.Provider value={contextValue}>
      {children}
    </DataContext.Provider>
  );
};

export const Context = () => {
  return useContext(DataContext);
};