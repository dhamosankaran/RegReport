import React from 'react';

const LoadingSpinner = ({ size = 'small' }) => {
  const sizeClass = size === 'large' ? 'w-8 h-8' : 'w-5 h-5';
  
  return (
    <div className={`loading-spinner ${sizeClass}`}></div>
  );
};

export default LoadingSpinner; 