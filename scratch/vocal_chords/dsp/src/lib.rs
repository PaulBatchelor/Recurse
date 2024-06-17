use voxbox::*;

fn db2lin(db: f32) -> f32 {
    (10.0_f32).powf(db / 20.)
}

struct PitchSmoother {
    smoother: Smoother,
    pitch: f32,
    pub bias: f32,
}

impl PitchSmoother {
    pub fn new(sr: usize, pitch: f32) -> Self {
        let mut p = PitchSmoother {
            pitch: pitch,
            smoother: Smoother::new(sr),
            bias: 0.0,
        };

        p.smoother.set_smooth(0.1);

        p
    }

    pub fn set_pitch(&mut self, pitch: f32) {
        if pitch < 0. {
            self.pitch = pitch.abs() + self.bias;
            self.smoother.snap_to_value(self.pitch + self.bias);
        }
        self.pitch = pitch + self.bias;
    }

    pub fn tick(&mut self) -> f32 {
        self.smoother.tick(self.pitch)
    }
}

#[repr(C)]
pub struct VocalChords {
    soprano: Voice,
    alto: Voice,
    tenor: Voice,
    bass: Voice,
    base_pitch: u16,
    reverb: BigVerb,
    hp1: ButterworthHighPass,
    hp2: ButterworthHighPass,
    dcblk: DCBlocker,
    sm_sop: PitchSmoother,
    sm_alt: PitchSmoother,
    sm_ten: PitchSmoother,
    sm_bas: PitchSmoother,
}

impl VocalChords {
    pub fn new(sr: u32) -> VocalChords {
        let oversample = 2;

        let tract_cm_tenor = 16.0;
        let tract_cm_bass = 18.3;
        let tract_cm_alto = 14.;
        let tract_cm_soprano = 12.9;

        let sr = sr as usize;
        let mut vc = VocalChords {
            soprano: Voice::new(sr, tract_cm_soprano, oversample),
            alto: Voice::new(sr, tract_cm_alto, oversample),
            tenor: Voice::new(sr, tract_cm_tenor, oversample),
            bass: Voice::new(sr, tract_cm_bass, oversample),
            base_pitch: 63,
            reverb: BigVerb::new(sr),
            hp1: ButterworthHighPass::new(sr),
            hp2: ButterworthHighPass::new(sr),
            dcblk: DCBlocker::new(sr),
            sm_sop: PitchSmoother::new(sr, 73.),
            sm_alt: PitchSmoother::new(sr, 70.),
            sm_ten: PitchSmoother::new(sr, 68.),
            sm_bas: PitchSmoother::new(sr, 66.),
        };

        let shape_ah_alto = [0.768, 0.5, 0.5, 0.5, 1.454, 3.368, 3.082, 2.74];

        let shape_ah_sop = [1.773, 0.225, 0.392, 0.5, 1.868, 1.987, 0.392, 3.249];

        let shape_ah_tenor = [0.225, 0.059, 0.059, 0.082, 0.701, 3.701, 1.725, 1.082];

        let shape_ah_bass = [0.225, 0.63, 0.844, 0.5, 0.5, 3.701, 0.82, 2.106];

        let chord = [0, 7, 0, 4];

        vc.bass.tract.drm(&shape_ah_bass);
        vc.bass.vibrato_rate(6.0);
        vc.bass.glottis.set_shape(0.3);
        vc.bass.glottis.srand(54321);
        vc.bass.glottis.set_aspiration(0.01);
        vc.bass.pitch = vc.base_pitch as f32 + chord[0] as f32 - 12.0;
        vc.sm_bas.bias = -12.0;

        vc.tenor.tract.drm(&shape_ah_tenor);
        vc.tenor.glottis.set_shape(0.4);
        vc.tenor.glottis.srand(12345);
        vc.tenor.vibrato_rate(6.1);
        vc.tenor.vibrato_depth(0.2);
        vc.tenor.pitch = vc.base_pitch as f32 + chord[1] as f32 - 12.0;
        vc.sm_ten.bias = -12.0;

        vc.alto.tract.drm(&shape_ah_alto);
        vc.alto.vibrato_rate(6.0);
        vc.alto.glottis.set_shape(0.3);
        vc.alto.glottis.set_aspiration(0.1);
        vc.alto.glottis.srand(330303);
        vc.alto.pitch = vc.base_pitch as f32 + chord[2] as f32;

        vc.soprano.tract.drm(&shape_ah_sop);
        vc.soprano.glottis.set_shape(0.5);
        vc.soprano.glottis.set_aspiration(0.1);
        vc.soprano.glottis.srand(111111);
        vc.soprano.vibrato_rate(6.5);
        vc.soprano.vibrato_depth(0.1);

        //vc.soprano.pitch = vc.base_pitch as f32 + chord[3] as f32;

        vc.reverb.size = 0.95;
        vc.hp1.set_freq(600.0);
        vc.hp2.set_freq(300.0);

        vc
    }

    pub fn tick(&mut self) -> f32 {
        let hp1 = &mut self.hp1;
        let hp2 = &mut self.hp2;
        let reverb = &mut self.reverb;
        let dcblk = &mut self.dcblk;
        let bass = &mut self.bass;
        let soprano = &mut self.soprano;
        let alto = &mut self.alto;
        let tenor = &mut self.tenor;

        soprano.pitch = self.sm_sop.tick();
        alto.pitch = self.sm_alt.tick();
        tenor.pitch = self.sm_ten.tick();
        bass.pitch = self.sm_bas.tick();

        let b = bass.tick() * db2lin(3.);
        let t = tenor.tick() * db2lin(-1.);
        let a = alto.tick() * db2lin(0.);
        let s = soprano.tick() * db2lin(5.);

        let sa = hp1.tick(a + s);
        let sum = (sa + b + t) * db2lin(-15.);
        let rvbin = hp2.tick(sum);
        let (rvb, _) = reverb.tick(rvbin, rvbin);
        let rvb = dcblk.tick(rvb);

        let out = sum + rvb * db2lin(-14.);
        let out = out * db2lin(-1.);

        out
    }

    pub fn process(&mut self, outbuf: *mut f32, sz: usize) {
        let outbuf: &mut [f32] = unsafe { std::slice::from_raw_parts_mut(outbuf, sz) };

        for n in 0..sz {
            outbuf[n] = self.tick();
        }
    }
}

#[no_mangle]
pub extern "C" fn newdsp(sr: u32) -> Box<VocalChords> {
    Box::new(VocalChords::new(sr))
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
pub extern "C" fn process(dsp: &mut VocalChords, outbuf: *mut f32, sz: usize) {
    dsp.process(outbuf, sz);
}

#[no_mangle]
pub extern "C" fn set_pitch(dsp: &mut VocalChords, voice: u8, pitch: f32) {

    let voice = match voice {
        3 => &mut dsp.sm_sop,
        2 => &mut dsp.sm_alt,
        1 => &mut dsp.sm_ten,
        0 => &mut dsp.sm_bas,
        _ => &mut dsp.sm_sop,
    };

    voice.set_pitch(pitch);
}
