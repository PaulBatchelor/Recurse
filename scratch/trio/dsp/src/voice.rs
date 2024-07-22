#[allow(dead_code)]
#[derive(Default, Debug, PartialEq)]
pub struct SchedulerState {
    pitch: u32,
    time: u32,
    gate: bool,
}

#[allow(dead_code)]
#[derive(Default)]
pub struct VoiceScheduler {
    state: SchedulerState,
}

#[allow(dead_code)]
impl VoiceScheduler {
    pub fn on(&mut self) {
        let state = &mut self.state;
        state.gate = true;
        state.time = 0;
    }

    pub fn off(&mut self) {
        let state = &mut self.state;
        state.gate = false;
        state.time = 0;

        // TODO: There needs to eb a way to
        // shut off other voices
    }

    pub fn tick(&mut self) {
        let state = &mut self.state;

        if state.gate {
            state.time += 1;
        }
    }

    pub fn change(&mut self, pitch: u32) {
        let state = &mut self.state;
        if state.gate && state.pitch != pitch {
            state.pitch = pitch;
            state.time = 0;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_defaults() {
        let ss = SchedulerState::default();

        let cmp = SchedulerState {
            pitch: 0,
            time: 0,
            gate: false,
        };

        assert_eq!(&ss, &cmp);
    }

    #[test]
    fn test_on() {
        let mut vs = VoiceScheduler::default();

        let cmp = SchedulerState {
            pitch: 0,
            time: 0,
            gate: true,
        };

        vs.on();
        assert_eq!(&vs.state, &cmp);

        // make sure time resets when "on" is called

        vs.state.time = 4;

        vs.on();
        assert_eq!(&vs.state, &cmp);
    }

    #[test]
    fn test_tick() {
        let mut vs = VoiceScheduler::default();

        let cmp = SchedulerState {
            pitch: 0,
            time: 0,
            gate: false,
        };

        // only tick when gate is on
        vs.tick();
        assert_eq!(&vs.state, &cmp);

        let mut vs = VoiceScheduler::default();
        let cmp = SchedulerState {
            pitch: 0,
            time: 1,
            gate: true,
        };

        vs.on();
        vs.tick();
        assert_eq!(&vs.state, &cmp);
    }

    #[test]
    fn test_off() {
        let mut vs = VoiceScheduler::default();

        let cmp = SchedulerState {
            pitch: 0,
            time: 0,
            gate: false,
        };

        vs.on();
        vs.tick();
        vs.tick();
        vs.tick();

        vs.off();
        assert_eq!(&vs.state, &cmp);
    }

    #[test]
    fn test_change() {
        let mut vs = VoiceScheduler::default();

        let cmp = SchedulerState {
            pitch: 0,
            time: 0,
            gate: false,
        };

        // do not change on gate off
        vs.change(60);
        assert_eq!(&vs.state, &cmp, "Should not set pitch on gate off");

        // note on and change
        let cmp = SchedulerState {
            pitch: 60,
            time: 0,
            gate: true,
        };
        vs.on();
        vs.change(60);
        assert_eq!(&vs.state, &cmp, "Note on change didn't work");

        // attempts to change pitch to current pitch shouldn't change
        // clock
        let cmp = SchedulerState {
            pitch: 60,
            time: 3,
            gate: true,
        };
        vs.tick();
        vs.tick();
        vs.tick();
        vs.change(60);
        assert_eq!(&vs.state, &cmp, "don't change clock if pitch is the same");

        let cmp = SchedulerState {
            pitch: 62,
            time: 0,
            gate: true,
        };
        vs.change(62);
        assert_eq!(&vs.state, &cmp, "did not change pitch as expected");

        // TODO: retriggers should work somehow, more state needed?
    }
}
