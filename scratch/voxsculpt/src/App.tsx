import React from 'react';
import './App.css';

interface SingerSynthParams {
    pitch: number;
    regions: number[];
    aspiration: number;
    noise_floor: number;
    shape: number;
    velum: number;
    length: number;
}

class SingerWorkletNode extends AudioWorkletNode {
    data: SingerSynthParams;

    constructor(context: BaseAudioContext,
        name: string, options: Object) {
        super(context, name, options);
        this.data = {
            pitch: 63.0,
            regions: new Array<number>(8),
            aspiration: 0.01,
            noise_floor: 0.01,
            shape: 0.4,
            velum: 0.0,
            length: 14.0,
        };
    }

    set_pitch(pitch: number) {
        this.data.pitch = pitch;
        this.port.postMessage({ type: "pitch", data: pitch });
    }

    set_region(region: number, value: number) {
        this.data.regions[region - 1] = value;
        this.port.postMessage({
            type: "regset",
            region: region,
            value: value,
        });
    }

    set_aspiration(aspiration: number) {
        this.data.aspiration = aspiration;
        this.port.postMessage({ type: "aspiration", data: aspiration });
    }

    set_noise_floor(noise_floor: number) {
        this.data.noise_floor = noise_floor;
        this.port.postMessage({ type: "noise_floor", data: noise_floor });
    }

    set_shape(shape: number) {
        this.data.shape = shape;
        this.port.postMessage({ type: "shape", data: shape });
    }

    set_velum(velum: number) {
        this.data.velum = velum;
        this.port.postMessage({ type: "velum", data: velum });
    }

    set_length(length: number) {
        this.data.length = length;
        this.port.postMessage({ type: "length", data: length });
    }

}

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
                    className="range-slider"
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
