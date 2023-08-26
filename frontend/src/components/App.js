import React from "react";
import ReactDOM from "react-dom";

export default function App() {
  return (
    <div>
      <h1>Chess App</h1>
    </div>
  );
}

const appDiv = document.getElementById("app");
ReactDOM.render(<App />, appDiv);
