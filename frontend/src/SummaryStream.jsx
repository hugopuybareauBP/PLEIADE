import React, { useEffect, useState } from "react";
import "./SummaryStream.css";

export default function SummaryStream({ text }) {
     const [displayedText, setDisplayedText] = useState("");
     const [isTyping, setIsTyping] = useState(true);

     useEffect(() => {
          if (!text) return;

          let index = 0;
          const interval = setInterval(() => {
               if (index < text.length) {
                    setDisplayedText(prev => prev + text[index]);
                    index++;
               } else {
                    clearInterval(interval);
                    setIsTyping(false);
                    }
          }, 20); 

     return () => clearInterval(interval);
     }, [text]);

     return (
          <div className="stream-wrapper">
               {isTyping && <div className="spinner"></div>}
               <pre className="stream-text">
                    {displayedText}
                    {isTyping && <span className="cursor">|</span>}
               </pre>
          </div>
     );
}