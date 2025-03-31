import React, { useEffect, useState } from "react";
import "./SummaryStream.css";

export default function SummaryStream({ text }) {
     const [displayedText, setDisplayedText] = useState("");
     const [isTyping, setIsTyping] = useState(true);

     useEffect(() => {
          let index = 0;

          const interval = setInterval(() => {
               setDisplayedText(prev => prev + text[index]);
               index++;

               if (index >= text.length) {
                    clearInterval(interval);
                    setIsTyping(false);
               } 
          }, 50); 

     return () => clearInterval(interval);
     }, [text]);

     // return (
     //      <div className="stream-wrapper">
     //           {isTyping && <div className="spinner"></div>}
     //           <pre className="stream-text">
     //                {displayedText}
     //                {isTyping && <span className="cursor">|</span>}
     //           </pre>
     //      </div>
     // );

     return (
          <div className="stream-wrapper">
               {displayedText}
               {isTyping && <span className="cursor">|</span>}
          </div>
     );
}