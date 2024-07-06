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

interface SliderGroupProps {
    label: string;
    sliders: SliderProps[];
}

const glottis_parameters = [
    {
        name: "freq",
        label: "Frequency",
        minRange: 26.0,
        maxRange: 86.0,
        defaultValue: 65.0,
        stepSize: 1,
    },
    {
        name: "aspiration",
        label: "Aspiration",
        minRange: 0.0,
        maxRange: 1.0,
        defaultValue: 0.03,
        stepSize: 0.001,
    },
    {
        name: "noise_floor",
        label: "Noise Floor",
        minRange: 0.0,
        maxRange: 1.0,
        defaultValue: 0.01,
        stepSize: 0.001,
    },
    {
        name: "shape",
        label: "Shape",
        minRange: 0.1,
        maxRange: 0.9,
        defaultValue: 0.4,
        stepSize: 0.001,
    },
    {
        name: "velum",
        label: "Velum",
        minRange: 0.0,
        maxRange: 4.0,
        defaultValue: 0.0,
        stepSize: 0.001,
    },
];

const tract_parameters = [
    {
        name: "length",
        label: "Tract Length",
        minRange: 8.0,
        maxRange: 30.0,
        defaultValue: 14.0,
        stepSize: 0.1,
    },
];

function generateRegionParams() {
    let p = []


    for (let i = 1; i <= 8; i++) {
        p.push({
            name: "region" + i,
            label: "Region " + i,
            minRange: 0.0,
            maxRange: 4.0,
            defaultValue: 0.5,
            stepSize: 0.001,
        });
    }


    return p;
}

const tract_region_params = generateRegionParams();

function Slider({ minRange, maxRange, stepSize, label, defaultValue }: SliderProps) {
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

function SliderGroup({ label, sliders }: SliderGroupProps) {

    var slidersJSX: React.JSX.Element[] = [];

    slidersJSX.push(
        <h2>{label}</h2>
    );

    sliders.forEach((param) => {
        slidersJSX.push(
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
            {slidersJSX}
        </div>
    );
}

function App() {
    return (
        <div className="App">
            <SliderGroup
                label="Glottis"
                sliders={glottis_parameters}
            />
            <SliderGroup
                label="Tract"
                sliders={tract_parameters}
            />
            <SliderGroup
                label="Tract Regions"
                sliders={tract_region_params}
            />
        </div>
    );
}

export default App;
