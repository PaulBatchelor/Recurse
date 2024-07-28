use std::collections::HashMap;

#[allow(dead_code)]
const DO: u8 = 0;
#[allow(dead_code)]
const RE: u8 = 2;
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

#[allow(dead_code)]
const KEY_C: u8 = 0;

type Chord = [u8; 3];

#[allow(dead_code)]
struct NoteTransitionTable {
    // 12 notes x 12 possible next notes
    // ignore the spaces that are the same
    transitions: [usize; 144],
    pub key: u8,
}

impl Default for NoteTransitionTable {
    fn default() -> Self {
        NoteTransitionTable {
            transitions: [0; 144],
            key: 0,
        }
    }
}

#[allow(dead_code)]
impl NoteTransitionTable {
    fn insert(&mut self, curnote: u8, nxtnote: u8, chord_ref: usize) {
        let curnote = (curnote - self.key) % 12;
        let nxtnote = (nxtnote - self.key) % 12;

        let pos = (12 * curnote + nxtnote) as usize;

        // adding 1 allows zero to be an empty value
        // I'm not using Option<T> because I don't know
        // what the overhead is like (not that that is
        // terribly important).
        self.transitions[pos] = chord_ref;
    }

    fn was_used_last(&self, curnote: u8, nxtnote: u8, chord_ref: usize) -> bool {
        let curnote = (curnote - self.key) % 12;
        let nxtnote = (nxtnote - self.key) % 12;

        let pos = (12 * curnote + nxtnote) as usize;

        self.transitions[pos] == chord_ref
    }
}

#[derive(Default)]
#[allow(dead_code)]
struct CandidatesTable {
    candidates: [usize; 16],
    ncandidates: u8,
}

impl CandidatesTable {
    pub fn reset(&mut self) {
        self.ncandidates = 0;
    }

    pub fn append_chord(&mut self, chord_ref: usize) {
        self.candidates[self.ncandidates as usize] = chord_ref;
        self.ncandidates += 1;
    }

    #[allow(dead_code)]
    pub fn get_chord(&self, pos: usize) -> Option<usize> {
        let chord = self.candidates[pos];

        if chord == 0 {
            return None;
        }

        Some(chord)
    }

    #[allow(dead_code)]
    pub fn get_first_chord(&self) -> Option<usize> {
        if self.ncandidates == 0 {
            return None;
        }

        // iterate through candidates until first non-zero
        for i in 0..self.ncandidates as usize {
            let chord = self.get_chord(i);
            if chord.is_some() {
                return chord;
            }
        }

        None
    }

    #[allow(dead_code)]
    pub fn remove_previous_transition(
        &mut self,
        note_transitions: &NoteTransitionTable,
        prev: u8,
        next: u8,
    ) {
        // only attempt if there is more than one candidate
        if self.ncandidates < 2 {
            return;
        }
        for i in 0..self.ncandidates as usize {
            if note_transitions.was_used_last(prev, next, self.candidates[i]) {
                self.candidates[i] = 0;
            }
        }
    }
}

#[derive(Default)]
#[allow(dead_code)]
struct ChordStates {
    chords: Vec<Chord>,
    transitions: HashMap<usize, Vec<usize>>,
    // candidates: [usize; 16],
    // ncandidates: u8,
    // TODO: pull this out of ChordStates?
    pub note_transitions: NoteTransitionTable,
    pub fallback_chords: [usize; 12],
}

#[allow(dead_code)]
impl ChordStates {
    pub fn add_chord(&mut self, chord: &Chord) -> usize {
        self.chords.push(*chord);
        self.chords.len()
    }

    pub fn get_chord(&self, chord_ref: usize) -> &Chord {
        &self.chords[chord_ref - 1]
    }

    pub fn add_transition(&mut self, from_chord: usize, to_chord: usize) -> Option<usize> {
        if from_chord > self.chords.len() {
            return None;
        }

        if to_chord > self.chords.len() {
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
            // Confusing, but these are zero-indexed
            Some(0)
        }
    }

    pub fn add_fallback_chord(&mut self, scale_degree: u8, chord_ref: usize) {
        self.fallback_chords[scale_degree as usize] = chord_ref;
    }

    pub fn query(&self, curchord: usize, next_note: u8, key: u8, candidates: &mut CandidatesTable) {
        // extract scale degree from note and key
        // TODO: this won't work for most notes <12, problem?
        let scale_degree = (next_note - key) % 12;

        candidates.reset();

        if curchord > self.chords.len() {
            return;
        }

        let potentials = self.transitions.get(&curchord);

        if potentials.is_none() {
            return;
        }

        let potentials = potentials.unwrap();

        // let ncandidates = &mut candidates.ncandidates;
        // let candidates = &mut candidates.candidates;
        for chord_idx in potentials {
            //let chord: &Chord = &self.chords[*chord_idx];
            let chord: &Chord = self.get_chord(*chord_idx);

            if chord.contains(&scale_degree) {
                candidates.append_chord(*chord_idx);
            }
        }

        // Attempt a fallback chord if there aren't any
        // candidates

        if candidates.ncandidates == 0 {
            let chord = self.fallback_chords[scale_degree as usize];
            if chord > 0 {
                candidates.append_chord(chord);
            }
        }
    }
}

#[allow(dead_code)]
fn find_nearest_upper(chord: &Chord, lead_pitch: u16, key: u8) -> u16 {
    for i in 1..12 {
        let test_pitch = lead_pitch + i;
        let scale_degree = ((test_pitch - key as u16) % 12) as u8;

        if chord.contains(&scale_degree) {
            return test_pitch;
        }
    }

    // As a fallback, return itself.
    lead_pitch
}

#[allow(dead_code)]
fn find_nearest_lower(chord: &Chord, lead_pitch: u16, key: u8) -> u16 {
    for i in 1..12 {
        let test_pitch = lead_pitch - i;
        let scale_degree = ((test_pitch - key as u16) % 12) as u8;

        if chord.contains(&scale_degree) {
            return test_pitch;
        }
    }

    // As a fallback, return itself.
    lead_pitch
}

#[derive(Default)]
pub struct ChordManager {
    //states: ChordStates,
}

#[allow(dead_code)]
impl ChordManager {
    pub fn populate(&mut self) {}
    pub fn change(&mut self, _pitch: u16) {}
    pub fn find_upper_pitch(&self) -> u16 {
        0
    }
    pub fn find_lower_pitch(&self) -> u16 {
        0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_chord_transitions() {
        let mut states = ChordStates::default();
        let tonic = states.add_chord(&[DO, MI, SO]);
        assert_eq!(tonic, 1);
        let subdominant = states.add_chord(&[DO, FA, LA]);
        assert_eq!(subdominant, 2);
        let dominant = states.add_chord(&[RE, SO, TI]);
        assert_eq!(dominant, 3);

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

    #[test]
    fn test_query() {
        let mut states = ChordStates::default();
        let tonic = states.add_chord(&[DO, MI, SO]);
        let subdominant = states.add_chord(&[DO, FA, LA]);
        let dominant = states.add_chord(&[RE, SO, TI]);
        let supertonic = states.add_chord(&[RE, FA, LA]);
        let mut candidates = CandidatesTable::default();

        states.add_transition(tonic, dominant);
        states.add_transition(tonic, subdominant);
        states.add_transition(tonic, supertonic);

        states.add_transition(subdominant, dominant);
        states.add_transition(subdominant, tonic);
        states.add_transition(dominant, tonic);

        // Query all possible chord transitions
        // for subdominant given a the note B
        // (7th scale degree TI)
        states.query(subdominant, 71, KEY_C, &mut candidates);

        // Expectation: only one chord possible (dominant)

        assert_eq!(candidates.ncandidates, 1);

        // Do another query on tonic going to F.
        // Two results expected
        states.query(tonic, 65, KEY_C, &mut candidates);
        assert_eq!(candidates.ncandidates, 2);

        let mut contains_subdominant = false;
        let mut contains_supertonic = false;

        for i in 0..candidates.ncandidates as usize {
            if let Some(c) = candidates.get_chord(i) {
                if c == subdominant {
                    contains_subdominant = true;
                }
                if c == supertonic {
                    contains_supertonic = true;
                }
            }
        }

        assert!(contains_supertonic);
        assert!(contains_subdominant);
    }

    #[test]
    fn test_note_transition_table() {
        let mut nt = NoteTransitionTable {
            key: KEY_C,
            ..Default::default()
        };

        let tonic = 1;
        let subdominant = 2;

        // transition chord from D4 -> C4 is C major
        nt.insert(62, 60, tonic);

        assert!(nt.was_used_last(62, 60, tonic));
        assert!(!nt.was_used_last(62, 60, subdominant));

        // transition chord from D4 -> C4 is F major
        nt.insert(62, 60, subdominant);

        assert!(nt.was_used_last(62, 60, subdominant));

        // test a note transition that wasn't used yet
        assert!(!nt.was_used_last(65, 60, tonic));
    }

    #[test]
    fn test_note_transitions() {
        let mut states = ChordStates::default();
        let tonic = states.add_chord(&[DO, MI, SO]);
        let subdominant = states.add_chord(&[DO, FA, LA]);
        let dominant = states.add_chord(&[RE, SO, TI]);
        let supertonic = states.add_chord(&[RE, FA, LA]);
        let mut candidates = CandidatesTable::default();

        // Populate transitions
        states.add_transition(tonic, subdominant);
        states.add_transition(tonic, dominant);
        states.add_transition(tonic, supertonic);
        states.add_transition(dominant, tonic);
        states.add_transition(subdominant, tonic);
        states.add_transition(supertonic, tonic);

        // expect dominant to be top result
        states.query(tonic, 62, KEY_C, &mut candidates);
        assert_eq!(candidates.ncandidates, 2);
        candidates.remove_previous_transition(&states.note_transitions, 60, 62);

        let chord = candidates.get_first_chord().unwrap();
        assert_eq!(chord, dominant);
        states.note_transitions.insert(60, 62, chord);
        assert!(states.note_transitions.was_used_last(60, 62, chord));

        // expect supertonic to be top result
        states.query(tonic, 62, KEY_C, &mut candidates);
        candidates.remove_previous_transition(&states.note_transitions, 60, 62);

        let chord = candidates.get_first_chord().unwrap();
        states.note_transitions.insert(60, 62, chord);
        assert_eq!(chord, supertonic);

        // expect dominant to be top result again
        states.query(tonic, 62, KEY_C, &mut candidates);
        candidates.remove_previous_transition(&states.note_transitions, 60, 62);
        states.note_transitions.insert(60, 62, chord);

        let chord = candidates.get_first_chord().unwrap();
        assert_eq!(chord, dominant);

        // Try again with subdominant
        states.query(subdominant, 60, KEY_C, &mut candidates);
        candidates.remove_previous_transition(&states.note_transitions, 65, 60);
        let chord = candidates.get_first_chord().unwrap();
        states.note_transitions.insert(65, 60, chord);
        assert_eq!(chord, tonic);

        states.query(subdominant, 60, KEY_C, &mut candidates);
        candidates.remove_previous_transition(&states.note_transitions, 65, 60);
        let chord = candidates.get_first_chord();
        assert!(chord.is_some());
        let chord = chord.unwrap();
        states.note_transitions.insert(65, 60, chord);
        assert_eq!(chord, tonic);
    }

    #[test]
    fn test_fallback_chords() {
        let mut states = ChordStates::default();
        let tonic = states.add_chord(&[DO, MI, SO]);
        let subdominant = states.add_chord(&[DO, FA, LA]);
        let dominant = states.add_chord(&[RE, SO, TI]);
        let supertonic = states.add_chord(&[RE, FA, LA]);
        let mut candidates = CandidatesTable::default();

        states.add_transition(tonic, subdominant);
        states.add_transition(tonic, dominant);
        states.add_transition(tonic, supertonic);
        states.add_transition(dominant, tonic);
        states.add_transition(subdominant, tonic);
        states.add_transition(supertonic, tonic);

        // add a fallback for B
        states.add_fallback_chord(TI, dominant);

        // The current state machine does not have an option for
        // B (scale degree TI)
        states.query(supertonic, 59, KEY_C, &mut candidates);

        assert!(candidates.ncandidates > 0);

        let chord = candidates.get_first_chord().unwrap();

        assert_eq!(chord, dominant);
    }

    #[test]
    fn test_voice_finder() {
        let tonic = [DO, MI, SO];
        let lead_pitch = 60;
        let key = KEY_C;

        let upper_pitch = find_nearest_upper(&tonic, lead_pitch, key);
        let lower_pitch = find_nearest_lower(&tonic, lead_pitch, key);

        // Upper should be MI (E4)
        assert_eq!(upper_pitch, 64, "Upper voice failed");

        // Lower shold be So (G3)
        assert_eq!(lower_pitch, 55, "Lower voice failed");

        // If lead pitch is part of the chord, just chose closest
        // notes for upper and lower

        // C#4/Db4: di or ra, b2, etc. This is not in a major chord
        let lead_pitch = 61;

        let upper_pitch = find_nearest_upper(&tonic, lead_pitch, key);
        let lower_pitch = find_nearest_lower(&tonic, lead_pitch, key);

        // Lower/upper pitch should be MI (E4)
        assert_eq!(lower_pitch, 60, "Wrong lower voice found");
        assert_eq!(upper_pitch, 64, "Wrong upper voice failed");
    }

    #[test]
    fn test_chord_manager() {
        let mut cm = ChordManager::default();

        cm.populate();

        // Lead: C4
        cm.change(60);

        // Lower: G3
        assert_eq!(cm.find_lower_pitch(), 55, "Expected lower to be G3");

        // upper: E4
        assert_eq!(cm.find_upper_pitch(), 64, "Expected upper to be E4");

        // TODO: Do some more pitch changes to make sure state machine seems functional
    }
}
