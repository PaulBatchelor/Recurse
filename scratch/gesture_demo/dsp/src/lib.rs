use voxbox::*;
//use std::mem;
//

#[repr(C)]
pub struct GestureDemo<'a> {
    voice: Voice,
    reverb: BigVerb,
    clk: Phasor,
    gst: LinearGesture<'a>,
    gpath: &'a Vec<GestureVertex>,
    tempo: f32,
    tempo_smoother: Smoother,
}

fn vtx (val: f32, dur: &[u32], bhvr: Behavior) -> GestureVertex {
    GestureVertex{val:val, num:dur[1], den:dur[0], bhvr:bhvr}
}

fn generate_sequence() -> Vec<GestureVertex>
{
    let gm = Behavior::GlissMedium;
    let gl = Behavior::GlissLarge;
    let gh = Behavior::GlissHuge;
    let base = 66.0;
    let e = &[1, 2];
    let s = &[1, 4];
    let edot = &[3, 4];


    let nt = |nn: u16, dur| -> GestureVertex {
        vtx(base + nn as f32, dur, gm)
    };

    let ntb = |nn: u16, dur, bvr| -> GestureVertex {
        vtx(base + nn as f32, dur, bvr)
    };

    let gpath = vec![
        nt(0, e),
        nt(2, e),
        nt(3, e),
        nt(7, e),

        nt(0, e),
        nt(2, s),
        nt(3, edot),
        nt(7, e),

        ntb(0, e, gh),
        nt(7, e),
        nt(5, e),
        nt(3, e),

        nt(5, e),
        nt(3, s),
        nt(5, edot),
        ntb(3, e, gl),
    ];

    gpath
}

impl<'a> GestureDemo<'a> {
    pub fn new(sr: u32, gpath: &Vec<GestureVertex>) -> GestureDemo {
        let tract_size_cm = 13.0;
        let oversample = 2;

        let mut gd = GestureDemo {
            voice: Voice::new(sr as usize, tract_size_cm, oversample),
            reverb: BigVerb::new(sr as usize),
            clk: Phasor::new(sr as usize, 0.0),
            gpath: gpath,
            gst: LinearGesture::new(),
            tempo: 100.0,
            tempo_smoother: Smoother::new(sr as usize),
        };

        let shape1 = [
            1.011, 0.201, 0.487, 0.440,
            1.297, 2.368, 1.059, 2.225
        ];

        gd.voice.tract.drm(&shape1);
        gd.reverb.size = 0.8;
        gd.tempo_smoother.snap_to_value(gd.tempo);
        gd.tempo_smoother.set_smooth(0.01);

        gd.gst.init(gpath);
        gd
    }

    pub fn tick(&mut self) -> f32 {
        let tempo = self.tempo_smoother.tick(self.tempo);
        self.clk.set_freq(tempo / 60.0);
        let c = self.clk.tick();
        let pitch = self.gst.tick(c);
        self.voice.pitch = pitch;
        let out = self.voice.tick() * 0.5;
        let (rvb, _) = self.reverb.tick(out, out);
        out + rvb*0.08
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
pub extern "C" fn genseq() -> Box<Vec<GestureVertex>> {
    Box::new(generate_sequence())
}

#[no_mangle]
pub extern "C" fn newdsp(sr: u32, gpath: &Vec<GestureVertex>) -> Box<GestureDemo> {
    Box::new(GestureDemo::new(sr, gpath))
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
pub extern "C" fn process(dsp: &mut GestureDemo, outbuf: *mut f32, sz: usize) {
    dsp.process(outbuf, sz);
}

#[no_mangle]
pub extern "C" fn set_tempo(dsp: &mut GestureDemo, tempo: f32) {
    dsp.tempo = tempo;
}

