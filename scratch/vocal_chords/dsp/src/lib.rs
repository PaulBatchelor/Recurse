use voxbox::*;

fn db2lin(db: f32) -> f32 {
    (10.0_f32).powf(db / 20.)
}

fn pitch_gestures(chords: &[[i16;4]]) -> Vec<Vec<GestureVertex>>
{
    let mut sop = vec![];
    let mut alt = vec![];
    let mut ten = vec![];
    let mut bas = vec![];
    let mut paths = vec![];

    for chord in chords.iter() {
        bas.push(GestureVertex {
            val: chord[0] as f32,
            num: 1,
            den: 4,
            bhvr: Behavior::GlissMedium
        });

        ten.push(GestureVertex {
            val: chord[1] as f32,
            num: 1,
            den: 4,
            bhvr: Behavior::GlissMedium
        });

        alt.push(GestureVertex {
            val: chord[2] as f32,
            num: 1,
            den: 4,
            bhvr: Behavior::GlissMedium
        });

        sop.push(GestureVertex {
            val: chord[3] as f32,
            num: 1,
            den: 4,
            bhvr: Behavior::GlissMedium
        });
    }

    paths.push(bas);
    paths.push(ten);
    paths.push(alt);
    paths.push(sop);

    paths
}

#[repr(C)]
pub struct VocalChords {
    soprano: Voice,
    alto: Voice,
    tenor: Voice,
    bass: Voice,
    base_pitch: u16,
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
        };

        let shape_ah_alto = [
            0.768,
            0.5,
            0.5,
            0.5,
            1.454,
            3.368,
            3.082,
            2.74
        ];

        let shape_ah_sop = [
            1.773,
            0.225,
            0.392,
            0.5,
            1.868,
            1.987,
            0.392,
            3.249
        ];

        let shape_ah_tenor = [
            0.225,
            0.059,
            0.059,
            0.082,
            0.701,
            3.701,
            1.725,
            1.082
        ];

        let shape_ah_bass = [
            0.225,
            0.63,
            0.844,
            0.5,
            0.5,
            3.701,
            0.82,
            2.106
        ];

        let chord = [0, 7, 0, 4];

        vc.bass.tract.drm(&shape_ah_bass);
        vc.bass.vibrato_rate(6.0);
        vc.bass.glottis.set_shape(0.3);
        vc.bass.glottis.srand(54321);
        vc.bass.glottis.set_aspiration(0.01);
        vc.bass.pitch = vc.base_pitch as f32 + chord[0] as f32;

        vc.tenor.tract.drm(&shape_ah_tenor);
        vc.tenor.glottis.set_shape(0.4);
        vc.tenor.glottis.srand(12345);
        vc.tenor.vibrato_rate(6.1);
        vc.tenor.vibrato_depth(0.2);
        vc.tenor.pitch = vc.base_pitch as f32 + chord[1] as f32;

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
        vc.soprano.pitch = vc.base_pitch as f32 + chord[3] as f32;

        vc
    }

    pub fn tick(&mut self) -> f32 {
        let b = self.bass.tick() * db2lin(3.);
        let t = self.tenor.tick() * db2lin(-1.);
        let a = self.alto.tick() * db2lin(0.);
        let s = self.soprano.tick() * db2lin(5.);

        s + a + t + b
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

// #[no_mangle]
// pub extern "C" fn genseq() -> Box<Vec<GestureVertex>> {
//     Box::new(generate_sequence())
// }

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

// #[no_mangle]
// pub extern "C" fn set_tempo(dsp: &mut VocalChords, tempo: f32) {
//     dsp.tempo = tempo;
// }

