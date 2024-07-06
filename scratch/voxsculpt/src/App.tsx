import React from 'react';
import './App.css';

interface SliderProps {
    name: string;
    minRange: number;
    maxRange: number;
    stepSize: number;
    defaultValue: number;
    label: string;
}

const parameters = [
    {
        name: "freq",
        label: "Frequency",
        minRange: 20.0,
        maxRange: 80.0,
        defaultValue: 63.0,
        stepSize: 0.01,
    },
    {
        name: "amp",
        label: "Amplitude",
        minRange: 0.0,
        maxRange: 1.0,
        defaultValue: 0.7,
        stepSize: 0.01,
    },
];

function Slider({ name, minRange, maxRange, stepSize, label, defaultValue }: SliderProps) {
    const [param, setParam] = React.useState(defaultValue);

    function handleChange(e: React.FormEvent<HTMLInputElement>) {
        setParam(parseFloat(e.currentTarget.value));
    }

    return (
        <>
            <div className="slider">
                <div className="slider-label">{label}</div>
                <div className="slider-slider"><input
                    type="range"
                    value={param}
                    onChange={handleChange}
                    min={minRange}
                    max={maxRange}
                    step={stepSize}
                /></div>
                <div className="slider-number">{param}</div>
            </div>
        </>
    );

}

function App() {
    var sliders: React.JSX.Element[] = [];

    parameters.forEach((param) => {
        sliders.push(
            <Slider
                key={param.name}
                name={param.name}
                minRange={param.minRange}
                maxRange={param.maxRange}
                stepSize={param.stepSize}
                label={param.label}
                defaultValue={param.defaultValue}
            />
        );
    })

    return (
        <div className="App">
            {sliders}
        </div>
    );
}

export default App;
