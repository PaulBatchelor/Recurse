use voxbox::*;

fn gliss_it(phs: f32, glisspos: f32) -> f32 {
    let mut a;
    if phs < glisspos {
        a = 0.0;
    } else {
        a = phs - glisspos;
        if a < 0.0 {
            a = 0.0;
        }
        a /= 1.0 - glisspos;
        a = a * a * a;
    }
    a
}

pub struct ChatterBox {
    voice: Voice,
    shape_morpher: RandomPhasor,
    chooser: LinearCongruentialGenerator,
    drm: [f32; 8],
    jit_freq: Jitter,
    jit_velum: Jitter,
    tgate: TriggerGate,
    tgate_pitch: TriggerGate,
    env: Envelope,
    shapes: Vec<[f32; 8]>,
    pub cur: usize,
    pub nxt: usize,
    pub pphs: f32,
    gate: u8,
    pgate: u8,
    env_pitch: Envelope,
    pub mouth_open: f32,
    hpfilt: ButterworthHighPass,
    reverb: BigVerb,
    pressure: Envelope,
    pressure_gate: TriggerGate,
    balloon: Balloon,
}

impl ChatterBox {
    pub fn new(sr: usize) -> Self {
        let oversample = 2;
        let tract_len = 8.7;
        let mut cb = ChatterBox {
            voice: Voice::new(sr, tract_len, oversample),
            shape_morpher: RandomPhasor::new(sr, 0.),
            chooser: LinearCongruentialGenerator::new(),
            drm: [0.5; 8],
            jit_freq: Jitter::new(sr),
            tgate: TriggerGate::new(sr),
            tgate_pitch: TriggerGate::new(sr),
            env: Envelope::new(sr),
            env_pitch: Envelope::new(sr),
            shapes: generate_shape_table(),
            pphs: -1.,
            cur: 0,
            nxt: 1,
            gate: 0,
            pgate: 0,
            mouth_open: 0.,
            jit_velum: Jitter::new(sr),
            hpfilt: ButterworthHighPass::new(sr),
            reverb: BigVerb::new(sr),
            pressure: Envelope::new(sr),
            balloon: Balloon::new(sr),
            pressure_gate: TriggerGate::new(sr),
        };

        cb.shape_morpher.min_freq = 3.0;
        cb.shape_morpher.max_freq = 10.0;
        cb.chooser.seed(4444);
        cb.jit_freq.seed(43438, 5555);
        cb.jit_freq.range_amplitude(-5., 1.);
        cb.jit_freq.range_rate(3., 10.);
        cb.tgate.duration = 0.9;
        cb.env.set_attack(0.01);
        cb.env.set_release(0.1);
        cb.voice.pitch = 63.;

        cb.env_pitch.set_attack(0.4);
        cb.env_pitch.set_release(1.5);
        cb.tgate_pitch.duration = 0.2;
        cb.jit_velum.seed(12345, 54321);
        cb.jit_velum.range_amplitude(0., 2.);
        cb.jit_velum.range_rate(1., 4.);

        cb.hpfilt.set_freq(800.);
        cb.reverb.size = 0.6;
        cb.reverb.cutoff = 4000.;

        cb.pressure.set_attack(0.01);
        cb.pressure.set_release(1.5);
        cb.balloon.inflation = 5.0;
        cb.balloon.deflation = 6.0;
        cb.pressure_gate.duration = 0.4;

        cb
    }

    pub fn poke(&mut self) {
        self.gate = !self.gate;
    }

    pub fn tick(&mut self) -> f32 {
        let voice = &mut self.voice;
        let shape_morpher = &mut self.shape_morpher;

        let chooser = &mut self.chooser;
        let drm = &mut self.drm;
        let jit_freq = &mut self.jit_freq;
        let jit_velum = &mut self.jit_velum;
        let tgate = &mut self.tgate;
        let env = &mut self.env;

        let shapes = &mut self.shapes;
        let cur = &mut self.cur;
        let nxt = &mut self.nxt;
        let pphs = &mut self.pphs;
        let gate = &self.gate;
        let pgate = &mut self.pgate;
        let env_pitch = &mut self.env_pitch;
        let tgate_pitch = &mut self.tgate_pitch;
        let hpfilt = &mut self.hpfilt;
        let reverb = &mut self.reverb;

        let t = if *pgate != *gate { 1.0 } else { 0.0 };
        let gt = tgate.tick(t);
        let ev = env.tick(gt);
        let gtp = tgate_pitch.tick(t);
        let evpch = env_pitch.tick(gtp);

        let pg = self.pressure_gate.tick(t);
        let pr = self.pressure.tick(pg);
        self.balloon.pressure = pr;
        let bal = self.balloon.tick();

        shape_morpher.min_freq = 2.0 + 6. * evpch;
        shape_morpher.max_freq = 3.0 + 6. * evpch;

        let phs = shape_morpher.tick();
        if phs < *pphs {
            *cur = *nxt;
            *nxt = (chooser.randf() * shapes.len() as f32) as usize;
            *cur %= shapes.len();
            *nxt %= shapes.len();
        }

        let shp_a = shapes[*cur];
        let shp_b = shapes[*nxt];

        jit_freq.range_amplitude(-3., 3. + 5. * evpch);
        jit_freq.range_rate(3. + 9. * evpch, 10. + 7. * evpch);

        let jf = jit_freq.tick();
        let jv = jit_velum.tick();

        voice.pitch = 62.0 + jf + 7.0 * evpch + 12. * bal;
        //voice.pitch = 62.0 + 16. * bal;

        let alpha = gliss_it(phs, 0.8);
        for i in 0..8 {
            drm[i] = (1. - alpha) * shp_a[i] + alpha * shp_b[i];
        }

        voice.nose.set_velum(jv);
        voice.tract.drm(drm);
        let out = voice.tick() * 0.5 * ev;
        //let out = voice.tick() * 0.5;
        let out = hpfilt.tick(out);
        let (rvb, _) = reverb.tick(out, out);
        let out = out + rvb * 0.1;

        *pphs = phs;
        *pgate = *gate;

        self.mouth_open = ev;
        out * 0.5
    }

    pub fn process(&mut self, outbuf: *mut f32, sz: usize) {
        let outbuf: &mut [f32] = unsafe { std::slice::from_raw_parts_mut(outbuf, sz) };

        for n in 0..sz {
            outbuf[n] = self.tick();
        }
    }
}

fn generate_shape_table() -> Vec<[f32; 8]> {
    let tiny_ah = [0.77, 0.855, 1.435, 0.728, 1.067, 3.217, 0.671, 2.892];

    let tiny_ieh = [0.6, 1.081, 4., 3.741, 0.954, 0.572, 0.487, 1.704];

    let tiny_r4mod1 = [0.53, 1.435, 0.303, 3.798, 2.383, 0.374, 2.807, 0.685];

    let tiny_r4mod2 = [0.53, 1.435, 0.303, 0.1, 2.383, 0.374, 2.807, 0.685];
    let shapes = vec![tiny_ah, tiny_ieh, tiny_r4mod2, tiny_r4mod1];

    shapes
}

#[no_mangle]
pub extern "C" fn newdsp(sr: u32) -> Box<ChatterBox> {
    Box::new(ChatterBox::new(sr as usize))
}

#[no_mangle]
pub extern "C" fn alloc(size: usize) -> *mut f32 {
    let mut buf = Vec::<f32>::with_capacity(size);
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);
    ptr as *mut f32
}

#[no_mangle]
pub extern "C" fn process(dsp: &mut ChatterBox, outbuf: *mut f32, sz: usize) {
    dsp.process(outbuf, sz);
}

#[no_mangle]
pub extern "C" fn poke(dsp: &mut ChatterBox) {
    dsp.poke();
}

#[no_mangle]
pub extern "C" fn mouth_open(dsp: &mut ChatterBox) -> f32 {
    dsp.mouth_open
}

#[no_mangle]
pub extern "C" fn mouth_curshape(dsp: &mut ChatterBox) -> u8 {
    dsp.cur as u8
}

#[no_mangle]
pub extern "C" fn mouth_nxtshape(dsp: &mut ChatterBox) -> u8 {
    dsp.nxt as u8
}
#[no_mangle]
pub extern "C" fn mouth_pos(dsp: &mut ChatterBox) -> f32 {
    dsp.pphs
}
