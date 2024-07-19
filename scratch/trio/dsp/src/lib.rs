use voxbox::*;

struct SmoothParam {
    pub value: f32,
    pub smoother: Smoother,
}

struct VoiceWithSmoother {
    pub voice: Voice,
    pub pitch: SmoothParam,
    pub gain: SmoothParam,
    pub gest: EventfulGesture,
}

impl VoiceWithSmoother {
    pub fn new(sr: usize, tract_len_cm: f32, oversample: u16) -> Self {
        let shape1 = [1.011, 0.201, 0.487, 0.440, 1.297, 2.368, 1.059, 2.225];
        let mut v = VoiceWithSmoother {
            voice: Voice::new(sr, tract_len_cm, oversample),
            pitch: SmoothParam::new(sr, 60.),
            gain: SmoothParam::new(sr, 0.0),
            gest: EventfulGesture::default(),
        };

        v.gain.smoother.set_smooth(0.005);
        v.pitch.smoother.set_smooth(0.04);
        v.voice.pitch = 60.;
        v.voice.tract.drm(&shape1);
        v.voice.vibrato_depth(0.3);
        v.voice.vibrato_rate(6.1);

        v
    }

    pub fn tick(&mut self) -> f32 {
        self.voice.pitch = self.pitch.tick();
        let gain = self.gain.tick();

        self.voice.tick() * 0.7 * gain
    }

    pub fn tick_with_gesture(&mut self, clk: f32) -> f32 {
        self.voice.pitch = self.gest.tick(clk);
        let gain = self.gain.tick();

        self.voice.tick() * 0.7 * gain
    }

    pub fn reset(&mut self) {
        self.pitch.reset();
    }

    pub fn set_pitch(&mut self, pitch: f32) {
        //self.pitch.value = pitch;
        self.gest.scalar(pitch);
        self.gest.behavior(Behavior::GlissHuge);
    }
}

#[repr(C)]
pub struct VoxData {
    testvar: f32,
    lead: VoiceWithSmoother,
    lower: VoiceWithSmoother,
    upper: VoiceWithSmoother,
    reverb: BigVerb,
    dcblk: DCBlocker,

    is_running: bool,
    pub x_axis: f32,
    px_axis: f32,
    pitches: Vec<i16>,
    base: u16,
    upper_lookup: [i16; 7],
    lower_lookup: [i16; 7],

    clk: Phasor,
    lphs: f32,
    last_pitch: f32,
    time: u32,
    pitch_changed: bool,
    pitch_last_changed: u32,
    cached_lead_pitch: f32,
    lower_has_changed: bool,
    lead_playing: bool,
    please_reset: bool,
}

//0  1  2  3  4  5  6  7  8  9 10  11
//0  0  1  1  2  3  3  4  4  5  5  6
//do di re ri mi fa fi so si la te ti
const PITCH_TO_DIATONIC: [i16; 12] = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6];

impl VoxData {
    pub fn new(sr: usize) -> Self {
        let tract_len_cm = 13.0;
        let oversample = 2;
        let mut vd = VoxData {
            testvar: 12345.0,
            lead: VoiceWithSmoother::new(sr, tract_len_cm, oversample),
            lower: VoiceWithSmoother::new(sr, tract_len_cm * 1.05, oversample),
            upper: VoiceWithSmoother::new(sr, tract_len_cm * 0.95, oversample),
            is_running: true,
            reverb: BigVerb::new(sr),
            dcblk: DCBlocker::new(sr),
            x_axis: 0.,
            px_axis: -1.,
            pitches: vec![0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19],
            base: 60,
            lower_lookup: [-5, -3, -1, 0, 2, 4, 5],
            upper_lookup: [4, 5, 7, 9, 11, 12, 14],
            clk: Phasor::new(sr, 0.),
            lphs: -1.,
            cached_lead_pitch: -1.,
            last_pitch: -1.,
            time: 0,
            pitch_last_changed: 0,
            pitch_changed: false,
            lower_has_changed: false,
            lead_playing: true,
            please_reset: false,
        };

        vd.clk.set_freq(1.0);
        vd.upper.voice.vibrato_depth(0.1);
        vd.upper.voice.vibrato_rate(6.2);
        vd.upper.gain.smoother.set_smooth(0.03);
        vd.upper.pitch.smoother.set_smooth(0.08);

        vd.lower.voice.vibrato_depth(0.1);
        vd.lower.voice.vibrato_rate(6.0);
        vd.lower.gain.smoother.set_smooth(0.02);
        vd.lower.pitch.smoother.set_smooth(0.09);
        vd
    }

    fn get_scale_degree(&self, pitch: u16, base: u16) -> (usize, f32) {
        //let pitch = self.lead.pitch.value as u16 - self.base;
        let pitch = pitch - base;
        let octave = pitch / 12;
        let pitch = pitch % 12;
        let pitch = PITCH_TO_DIATONIC[pitch as usize];
        (pitch as usize, octave as f32)
    }

    fn check_for_pitch_changes(&mut self) {
        let pitch = (self.x_axis * self.pitches.len() as f32) as usize;
        let pitch = pitch.clamp(0, self.pitches.len() - 1);
        let pitch = 60.0 + self.pitches[pitch] as f32;

        let did_pitch_change = self.last_pitch > 0. && self.last_pitch != pitch;

        if did_pitch_change {
            println!("changed {} -> {} at {}", self.last_pitch, pitch, self.time);
            self.last_pitch = pitch;
            self.pitch_last_changed = self.time;
        }

        // instantaneous update of lead pitch
        self.lead.pitch.value = pitch;

        if self.please_reset {
            println!("resetting THE LEAD PITCH");
            self.lead.reset();
        }
    }

    pub fn tick(&mut self) -> f32 {
        if self.please_reset {
            println!("RESETTING");
            self.clk.reset();
            self.last_pitch = -1.;
            self.time = 0;
            self.pitch_last_changed = 0;
            self.lower_has_changed = false;
            //self.lower.reset();
            //self.lead.reset();
            //self.upper.reset();
        }

        let clk = self.clk.tick();

        if self.lphs >= 0. && self.lphs > clk {
            self.time += 1;
            println!("tick {}", self.time);
            //self.pitch_changed = false;

            let did_pitch_change =
                self.last_pitch > 0. && self.cached_lead_pitch != self.last_pitch;

            let held_long_enough_low = (self.time - self.pitch_last_changed) > 0;
            let held_long_enough_upper = (self.time - self.pitch_last_changed) > 1;

            if did_pitch_change && held_long_enough_low {
                //self.lead.pitch.value = self.last_pitch;
                println!("lower: pitch changed and held long enough");
                self.cached_lead_pitch = self.last_pitch;
                //self.update_pitches();

                let pitch = self.lead.pitch.value;
                let (idx, octave) = self.get_scale_degree(pitch as u16, self.base);

                let pitch = self.base as f32 + 12.0 * octave + self.lower_lookup[idx] as f32;
                //self.lower.pitch.value = pitch;
                self.lower.set_pitch(pitch);
                //self.upper.pitch.value =
                //    self.base as f32 + 12.0 * octave + self.upper_lookup[idx] as f32;
                self.lower_has_changed = true;

                if self.lead_playing {
                    if self.lower.gain.value == 0. {
                        self.lower.reset();
                    }
                    self.lower.gain.value = 0.8;
                }
            }

            if self.lower_has_changed && held_long_enough_upper {
                //self.lead.pitch.value = self.last_pitch;
                println!("upper: pitch changed and held long enough");
                self.cached_lead_pitch = self.last_pitch;
                //self.update_pitches();

                let pitch = self.lead.pitch.value;
                let (idx, octave) = self.get_scale_degree(pitch as u16, self.base);

                // self.lower.pitch.value =
                //     self.base as f32 + 12.0 * octave + self.lower_lookup[idx] as f32;
                let pitch = self.base as f32 + 12.0 * octave + self.upper_lookup[idx] as f32;
                //self.upper.pitch.value = pitch;
                self.upper.set_pitch(pitch);
                self.lower_has_changed = false;

                if self.lead_playing {
                    if self.upper.gain.value == 0. {
                        self.upper.reset();
                    }
                    self.upper.gain.value = 0.8;
                }
            }
            self.last_pitch = self.lead.pitch.value;
        }

        if self.x_axis != self.px_axis {
            self.px_axis = self.x_axis;
            self.check_for_pitch_changes();
        }

        self.please_reset = false;
        self.lphs = clk;

        let lead = self.lead.tick();
        let lower = self.lower.tick_with_gesture(clk);
        let upper = self.upper.tick_with_gesture(clk);

        let voices = (lead + lower + upper) * 0.33;
        let (r, _) = self.reverb.tick(voices, voices);
        let r = self.dcblk.tick(r);

        (voices + r * 0.1) * 0.6
    }

    pub fn running(&mut self) -> u8 {
        let mut state = 1;

        if !self.is_running {
            state = 0;
        }

        state
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

    pub fn reset(&mut self) {
        self.smoother.snap_to_value(self.value);
    }
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
    vd.lead.pitch.value = pitch;
}

#[no_mangle]
pub extern "C" fn vox_gate(vd: &mut VoxData, gate: f32) {
    println!("gate: {gate}");
    if gate == 0.0 {
        vd.lead.gain.value = 0.;
        vd.upper.gain.value = 0.;
        vd.lower.gain.value = 0.;
        vd.lead_playing = false;
    } else {
        vd.please_reset = true;
        vd.lead.gain.value = gate * 0.8;
        vd.lead.reset();
        vd.lead_playing = true;
    }
}

#[no_mangle]
pub extern "C" fn vox_tongue_shape(vd: &mut VoxData, x: f32, y: f32) {
    vd.lead.voice.tract.tongue_shape(x, y);
}

#[no_mangle]
pub extern "C" fn vox_x_axis(vd: &mut VoxData, x: f32) {
    vd.x_axis = x;
}
