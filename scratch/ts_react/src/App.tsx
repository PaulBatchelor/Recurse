import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [freq, setFreq] = React.useState(20);
  console.log(freq);

  function handleChange(e: React.FormEvent<HTMLInputElement>) {
    //setFreq(e.target.value);
    setFreq(parseInt(e.currentTarget.value));
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <input type="range" value={freq} onChange={handleChange}/>
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
