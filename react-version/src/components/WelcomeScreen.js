import React from 'react';

const WelcomeScreen = ({ message }) => {
  return (
    <div className="flex flex-col items-center justify-center text-center mb-8">
      <h1 className="text-[1.6rem] font-medium text-text-primary">
        {message}
      </h1>
    </div>
  );
};

export default WelcomeScreen; 