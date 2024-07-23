#[allow(dead_code)]
#[derive(Default, Debug, PartialEq)]
struct SchedulerState {
    pitch: u32,
    time: u32,
    gate: bool,
}

#[allow(dead_code)]
#[derive(Default)]
struct Trigger {
    trig: bool,
}

#[allow(dead_code)]
#[derive(Clone, Copy)]
pub enum EventType {
    Lower,
}

#[allow(dead_code)]
struct EventTrigger {
    evtype: EventType,
    trigger: Trigger,
}

impl EventTrigger {
    pub fn new(evtype: EventType) -> Self {
        EventTrigger {
            trigger: Trigger::default(),
            evtype,
        }
    }
}

#[allow(dead_code)]
struct Hooks {
    lower_voice: EventTrigger,
}

impl Default for Hooks {
    fn default() -> Self {
        Hooks {
            lower_voice: EventTrigger::new(EventType::Lower),
        }
    }
}

#[allow(dead_code)]
#[derive(Default)]
pub struct AutoVoiceState {
    upper: bool,
    lower: bool,
}

#[allow(dead_code)]
impl Trigger {
    pub fn fire(&mut self) {
        self.trig = true;
    }

    pub fn has_fired(&mut self) -> bool {
        self.trig
    }

    pub fn reset(&mut self) {
        self.trig = false;
    }

    pub fn check(&mut self) -> bool {
        let fired = self.has_fired();
        self.reset();
        fired
    }
}

#[allow(dead_code)]
#[derive(Default)]
pub struct VoiceScheduler {
    state: SchedulerState,
    autovoice: AutoVoiceState,
    hooks: Hooks,
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
        let av = &mut self.autovoice;

        state.gate = false;
        state.time = 0;

        av.upper = false;
        av.lower = false;
    }

    pub fn tick(&mut self) {
        let state = &mut self.state;

        if !state.gate {
            return;
        }

        let av = &mut self.autovoice;

        if state.time == 1 {
            av.lower = true;
            self.hooks.lower_voice.trigger.fire();
        } else if state.time == 2 {
            av.upper = true;
        }

        state.time += 1;
    }

    pub fn change(&mut self, pitch: u32) {
        let state = &mut self.state;
        if state.gate && state.pitch != pitch {
            state.pitch = pitch;
            state.time = 0;
        }
    }

    pub fn pop_next_event(&mut self) -> Option<EventType> {
        let hooks = &mut self.hooks;

        let s = hooks.lower_voice.trigger.check();

        if s {
            return Some(hooks.lower_voice.evtype);
        }

        None
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

    #[test]
    fn test_trigger() {
        let mut trig = Trigger::default();
        assert!(!trig.trig, "Default sanity check failed");

        assert!(!trig.has_fired(), "Trigger has not yet fired");

        trig.fire();

        assert!(trig.has_fired(), "Trigger was supposed to fire.");

        trig.reset();

        assert!(!trig.has_fired(), "Trigger did not reset as expected.");

        trig.fire();

        let fired = trig.check();

        assert!(fired, "Trigger was supposed to have fired");

        assert!(
            !trig.has_fired(),
            "Check() did not reset state as expected."
        );
    }

    #[test]
    fn test_autovoice() {
        let av = AutoVoiceState::default();

        assert!(!av.upper && !av.lower, "Sanity check failed");

        let mut vs = VoiceScheduler::default();

        vs.on();
        vs.tick();
        assert!(!av.lower, "Lower voice is supposed to be off");

        // two ticks needed for at least 1 full tick
        vs.tick();

        let av = &vs.autovoice;
        assert!(av.lower, "Lower voice is supposed to be on");
        assert!(!av.upper, "Upper voice is supposed to be off");

        vs.tick();
        let av = &vs.autovoice;

        assert!(av.lower, "Lower voice is supposed to be on");
        assert!(av.upper, "Upper voice is supposed to be on");

        vs.off();
        let av = &vs.autovoice;
        assert!(!av.lower, "Lower voice is supposed to be off");
        assert!(!av.upper, "Upper voice is supposed to be off");
    }

    #[test]
    fn test_initial_lower() {
        let mut vs = VoiceScheduler::default();

        vs.on();
        vs.tick();

        let mut nevents = 0;

        while let Some(_) = vs.pop_next_event() {
            nevents += 1;
        }

        assert_eq!(nevents, 0, "Expected no events on first tick");

        vs.tick();

        let mut found_lower = false;

        while let Some(evt) = vs.pop_next_event() {
            found_lower = matches!(evt, EventType::Lower);
        }

        assert!(found_lower, "Expected lower voice event");

        vs.tick();

        let mut found_lower = false;

        while let Some(evt) = vs.pop_next_event() {
            found_lower = matches!(evt, EventType::Lower);
        }

        assert!(!found_lower, "Expected not to find lower voice event");
    }
}
