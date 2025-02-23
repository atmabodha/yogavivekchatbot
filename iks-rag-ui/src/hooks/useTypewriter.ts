import { useState, useEffect } from 'react';

export const useTypewriter = (text: string, speed: number = 10, isSummaryComplete: boolean = false) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isComplete, setIsComplete] = useState(false);


  useEffect(() => {
    let index = 0;
    setDisplayedText('');
    setIsComplete(false);

    const timer = setInterval(() => {
      if (index < text.length ) {
        setDisplayedText((current) => current + text.charAt(index));
        index++;
      } else {
        setIsComplete(true);
        clearInterval(timer);
      }
    }, speed);

    return () => clearInterval(timer);
  }, [text, speed]);

  return { displayedText, isComplete };
}; 