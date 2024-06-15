use voxbox::*;
//use std::mem;
//

#[repr(C)]
pub struct GestureDemo<'a> {
    voice: Voice,
    reverb: BigVerb,
    clk: Phasor,
    gst: LinearGesture<'a>,
    gpath: Vec<GestureVertex>,
}

fn vtx (val: f32, dur: &[u32], bhvr: Behavior) -> GestureVertex {
    GestureVertex{val:val, num:dur[1], den:dur[0], bhvr:bhvr}
}

impl<'a> GestureDemo<'a> {
    pub fn new(sr: u32) -> GestureDemo<'a> {
        let tract_size_cm = 13.0;
        let oversample = 2;
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

        let _gpath = vec![
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

        let mut gd = GestureDemo {
            voice: Voice::new(sr as usize, tract_size_cm, oversample),
            reverb: BigVerb::new(sr as usize),
            clk: Phasor::new(sr as usize, 0.0),
            gpath: vec![],
            gst: LinearGesture::new(),
        };

        // TODO: how to make this work?
        //gd.gst.path = Some(&gd.gpath);
        gd
    }

    pub fn tick(&mut self) -> f32 {
        0.0
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
// pub extern "C" fn newdsp(sr: u32) -> Box<GestureDemo> {
//     Box::new(GestureDemo::new(sr))
// }

// adapted from Glicol
// https://github.com/chaosprint/glicol/blob/7ece81d6fadfc5a8873df2a3ac04f8f915fa1998/rs/wasm/src/lib.rs#L9-L15
#[no_mangle]
pub extern "C" fn alloc(size: usize) -> *mut f32 {
    let mut buf = Vec::<f32>::with_capacity(size);
    let ptr = buf.as_mut_ptr();
    std::mem::forget(buf);
    ptr as *mut f32
}

// #[no_mangle]
// pub extern "C" fn process(dsp: &mut GestureDemo, outbuf: *mut f32, sz: usize) {
//     dsp.process(outbuf, sz);
// }

// #[no_mangle]
// pub extern "C" fn set_pitch(dsp: &mut GestureDemo, pitch: f32) {
//     dsp.set_pitch(pitch);
// }

