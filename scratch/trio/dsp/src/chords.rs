use std::collections::HashMap;

#[allow(dead_code)]
const DO: u8 = 0;
#[allow(dead_code)]
const RE: u8 = 4;
#[allow(dead_code)]
const MI: u8 = 4;
#[allow(dead_code)]
const FA: u8 = 5;
#[allow(dead_code)]
const SO: u8 = 7;
#[allow(dead_code)]
const LA: u8 = 9;
#[allow(dead_code)]
const TI: u8 = 11;

type Chord = [u8; 3];

#[derive(Default)]
#[allow(dead_code)]
struct ChordStates {
    chords: Vec<Chord>,
    transitions: HashMap<usize, Vec<usize>>,
}

#[allow(dead_code)]
impl ChordStates {
    pub fn add_chord(&mut self, chord: &Chord) -> usize {
        self.chords.push(*chord);
        self.chords.len() - 1
    }

    pub fn add_transition(&mut self, from_chord: usize, to_chord: usize) -> Option<usize> {
        if from_chord >= self.chords.len() {
            return None;
        }

        if to_chord >= self.chords.len() {
            return None;
        }

        let transitions = &mut self.transitions;

        let entry = &mut transitions.get_mut(&from_chord);

        if entry.is_some() {
            let chordlist = &mut entry.as_mut().unwrap();
            for chord in chordlist.iter() {
                if to_chord == *chord {
                    return None;
                }
            }
            chordlist.push(to_chord);
            Some(chordlist.len() - 1)
        } else {
            transitions.insert(from_chord, vec![to_chord]);
            Some(0)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_chord_transitions() {
        let mut states = ChordStates::default();
        let tonic = states.add_chord(&[DO, MI, SO]);
        assert_eq!(tonic, 0);
        let subdominant = states.add_chord(&[DO, FA, LA]);
        assert_eq!(subdominant, 1);
        let dominant = states.add_chord(&[RE, SO, TI]);
        assert_eq!(dominant, 2);

        let result = states.add_transition(tonic, dominant);
        assert!(result.is_some());
        assert_eq!(result.unwrap(), 0);
        let result = states.add_transition(tonic, subdominant);
        assert!(result.is_some());
        assert_eq!(result.unwrap(), 1);
        let result = states.add_transition(tonic, subdominant);
        assert!(result.is_none());

        // make sure out of bounds work
        let result = states.add_transition(500, subdominant);
        assert!(result.is_none());
        let result = states.add_transition(tonic, 999);
        assert!(result.is_none());
    }
}
