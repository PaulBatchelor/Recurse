import React from 'react';
import './App.css';

function Slider() {
  const [freq, setFreq] = React.useState(20);
  function handleChange(e: React.FormEvent<HTMLInputElement>) {
    //setFreq(e.target.value);
    setFreq(parseInt(e.currentTarget.value));
  }

  return (
      <>
      <p>Hello
      <input type="range" value={freq} onChange={handleChange}/>
      {freq}</p>
      </>
  );

}

function App() {
  return (
    <div className="App">
        <Slider />
    </div>
  );
}

export default App;
