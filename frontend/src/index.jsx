import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const LOCAL_API_ORIGIN = 'http://localhost:8000';
const originalFetch = window.fetch.bind(window);

// Keep legacy localhost URLs working in deployed environments.
window.fetch = (input, init) => {
  if (typeof input === 'string') {
    return originalFetch(input.replace(LOCAL_API_ORIGIN, ''), init);
  }

  if (input instanceof URL) {
    const rewritten = input.toString().replace(LOCAL_API_ORIGIN, '');
    return originalFetch(rewritten, init);
  }

  if (input instanceof Request && input.url.startsWith(LOCAL_API_ORIGIN)) {
    const rewrittenRequest = new Request(input.url.replace(LOCAL_API_ORIGIN, ''), input);
    return originalFetch(rewrittenRequest, init);
  }

  return originalFetch(input, init);
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
