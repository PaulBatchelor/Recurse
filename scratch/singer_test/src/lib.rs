use voxbox::*;
use std::f32::consts::PI;

#[repr(C)]
pub struct SingerSynth {
    zero: f32,
    counter: usize,
    glot: Glot,
    tract: Tract,
    shape1: [f32; 8],
    shape2: [f32; 8],
    shape: [f32; 8],
    vib: Phasor,
    shaper: Phasor,
    amp: Phasor,
    dcblk: DCBlocker,
}

// a simple sine wave generator
pub fn sin(phs: f32) -> f32 {
    let lfo = (phs * 2.0*PI).sin();
    let lfo = (lfo + 1.0) * 0.5;
    lfo
}

// midi-to-frequency converter
pub fn mtof(nn: f32) -> f32 {
    let freq = (2.0_f32).powf((nn - 69.0) / 12.0) * 440.0;
    freq
}

impl SingerSynth {
    pub fn new(sr: u32) -> SingerSynth {
        let mut ss = SingerSynth {
            zero: 0.0,
            counter: 0,
            glot: Glot::new(sr as usize),
            tract: Tract::new(sr as usize, 13.0, 1),
            shape1:  [
                2.0, 3.0, 9.0, 2.0,
                1.0, 1.0, 1.0, 1.0,
            ],
            shape2:  [
                1.0, 5.0, 5.0, 5.0,
                5.0, 3.0, 3.0, 1.0,
            ],
            shape:  [0.0; 8],
            vib: Phasor::new(sr as usize, 0.0),
            shaper: Phasor::new(sr as usize, 0.0),
            amp: Phasor::new(sr as usize, 0.0),
            dcblk: DCBlocker::new(sr as usize),
        };
        ss.glot.set_shape(0.4);
        ss.glot.set_aspiration(0.3);
        ss.glot.set_noise_floor(0.01);
        ss
    }

    pub fn tick(&mut self) -> f32 {
        self.vib.set_freq(6.0);
        self.shaper.set_freq(0.1);
        self.amp.set_freq(0.3);
        let vib = sin(self.vib.tick());
        let shaper = sin(self.shaper.tick());
        let amp = sin(self.amp.tick());

        for i in 0 .. 8 {
            self.shape[i] =
                shaper * self.shape1[i] +
                (1.0 - shaper)*self.shape2[i];
        }
        self.glot.set_freq(mtof(69.0 + 0.5*vib));
        self.tract.drm(&self.shape);
        let g = self.glot.tick();
        let tr = self.tract.tick(g);
        let tr = self.dcblk.tick(tr * 0.8);
        tr
    }

    pub fn process(&mut self, outbuf: *mut f32, sz: usize) {
        let outbuf: &mut [f32] = unsafe {
            std::slice::from_raw_parts_mut(outbuf, sz)
        };

        for n in 0..sz {
            outbuf[n] = self.tick();
        }

    }
}

#[no_mangle]
pub extern "C" fn newdsp(sr: u32) -> Box<SingerSynth> {
    Box::new(SingerSynth::new(sr))
}

// adapted from Glicol
// https://github.com/chaosprint/glicol/blob/7ece81d6fadfc5a8873df2a3ac04f8f915fa1998/rs/wasm/src/lib.rs#L9-L15
#[no_mangle]
pub extern "C" fn alloc(size: usize) -> *mut f32 {
    let mut buf = Vec::<f32>::with_capacity(size);
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);
    ptr as *mut f32
}

#[no_mangle]
pub extern "C" fn process(dsp: &mut SingerSynth, outbuf: *mut f32, sz: usize) {
    dsp.process(outbuf, sz);
}
