use voxbox::*;

struct SmoothParam {
    pub value: f32,
    pub smoother: Smoother,
}

#[repr(C)]
pub struct VoxData {
    testvar: f32,
    voice: Voice,
    pitch: SmoothParam,
    gain: SmoothParam,
    reverb: BigVerb,
    dcblk: DCBlocker,

    is_running: bool,
    pub x_axis: f32,
    px_axis: f32,
    pitches: Vec<i16>,
}

impl VoxData {
    pub fn new(sr: usize) -> Self {
        let tract_len_cm = 13.0;
        let oversample = 2;
        let shape1 = [1.011, 0.201, 0.487, 0.440, 1.297, 2.368, 1.059, 2.225];
        let mut vd = VoxData {
            testvar: 12345.0,
            voice: Voice::new(sr, tract_len_cm, oversample),
            // listener: OSCServer::new("127.0.0.1:8001"),
            is_running: true,
            pitch: SmoothParam::new(sr, 60.),
            gain: SmoothParam::new(sr, 0.0),
            reverb: BigVerb::new(sr),
            dcblk: DCBlocker::new(sr),
            x_axis: 0.,
            px_axis: -1.,
            pitches: vec![0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19],
        };

        vd.gain.smoother.set_smooth(0.005);
        vd.pitch.smoother.set_smooth(0.04);
        vd.voice.pitch = 60.;
        vd.voice.tract.drm(&shape1);
        vd
    }

    pub fn tick(&mut self) -> f32 {
        if self.x_axis != self.px_axis {
            self.px_axis = self.x_axis;
            let pitch = (self.x_axis * self.pitches.len() as f32) as usize;
            let pitch = pitch.clamp(0, self.pitches.len() - 1);
            let pitch = 60.0 + self.pitches[pitch] as f32;
            self.pitch.value = pitch;
        }

        self.voice.pitch = self.pitch.tick();
        let gain = self.gain.tick();

        self.voice.vibrato_depth(0.3);
        self.voice.vibrato_rate(6.1);
        let v = self.voice.tick() * 0.7 * gain;

        let (r, _) = self.reverb.tick(v, v);
        let r = self.dcblk.tick(r);

        (v + r * 0.1) * 0.6
    }

    pub fn running(&mut self) -> u8 {
        let mut state = 1;

        if self.is_running == false {
            state = 0;
        }

        return state;
    }
}

impl Drop for VoxData {
    fn drop(&mut self) {
        println!("dropping");
    }
}

impl SmoothParam {
    pub fn new(sr: usize, ival: f32) -> Self {
        let mut sp = SmoothParam {
            value: ival,
            smoother: Smoother::new(sr),
        };
        sp.smoother.set_smooth(0.07);
        sp
    }

    pub fn tick(&mut self) -> f32 {
        self.smoother.tick(self.value)
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

#[no_mangle]
pub extern "C" fn vox_poll(_vd: &mut VoxData) {
    // vd.poll();
}

#[no_mangle]
pub extern "C" fn vox_running(vd: &mut VoxData) -> u8 {
    vd.running()
}

#[no_mangle]
pub extern "C" fn vox_free(vd: &mut VoxData) {
    let ptr = unsafe { Box::from_raw(vd) };
    drop(ptr);
}

#[no_mangle]
pub extern "C" fn vox_pitch(vd: &mut VoxData, pitch: f32) {
    vd.pitch.value = pitch;
}

#[no_mangle]
pub extern "C" fn vox_gate(vd: &mut VoxData, gate: f32) {
    vd.gain.value = gate * 0.8;
}

#[no_mangle]
pub extern "C" fn vox_tongue_shape(vd: &mut VoxData, x: f32, y: f32) {
    vd.voice.tract.tongue_shape(x, y);
}

#[no_mangle]
pub extern "C" fn vox_x_axis(vd: &mut VoxData, x: f32) {
    vd.x_axis = x;
}
