use voxbox::*;

#[repr(C)]
pub struct VoxData {
    testvar: f32,
    voice: Voice,
}

impl VoxData {
    pub fn new(sr: usize) -> Self {
        let tract_len_cm = 13.0;
        let oversample = 2;
        let shape1 = [
            1.011, 0.201, 0.487, 0.440,
            1.297, 2.368, 1.059, 2.225
        ];
        let mut vd = VoxData {
            testvar: 12345.0,
            voice: Voice::new(sr, tract_len_cm, oversample),
        };

        vd.voice.tract.drm(&shape1); 
        vd
    }

    pub fn tick(&mut self) -> f32 {
        self.voice.pitch = 63.;
        self.voice.tick() * 0.8
    }
}

#[no_mangle]
pub extern "C" fn testfunction() -> f32 {
    return 330.0;
}


#[no_mangle]
pub extern "C" fn newdsp(sr: u32) -> Box<VoxData> {
    let sr = sr as usize;
    println!("samplerate: {}", sr);
    Box::new(VoxData::new(sr))
}

#[no_mangle]
pub extern "C" fn testgetter(vd: &mut VoxData) -> f32 {
    vd.testvar 
}

#[no_mangle]
pub extern "C" fn vox_tick(vd: &mut VoxData) -> f32 {
    vd.tick()
}
