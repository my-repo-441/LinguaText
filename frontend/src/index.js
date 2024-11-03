import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import App from './App'; // `App.js` があることを確認
import './index.css';    // `index.css` が存在しない場合はコメントアウト

const rootElement = document.getElementById("root");
const root = createRoot(rootElement);

root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
