import React from 'react';
import ReactDOM from 'react-dom';
import App from './App'; // `App.js` があることを確認
import './index.css';    // `index.css` が存在しない場合はコメントアウト

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
