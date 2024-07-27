use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::io::BufRead;
use std::io::Write;

fn main() {
    let filename = "pulse.txt";
    let outfile = "pulse.bin";

    let f = File::open(filename).unwrap();

    let reader = BufReader::new(f);

    let mut times: Vec<f32> = vec![];

    for line in reader.lines() {
        if line.is_ok() {
            let time = line.unwrap().parse::<f32>();
            if time.is_ok() {
                times.push(time.unwrap());
            }
        }
    }

    let mut deltas: Vec<f32> = vec![];

    let mut prev = times[0];
    for (pos, time) in times.into_iter().enumerate() {
        if pos > 0 {
            let delta = time - prev;
            deltas.push(delta);
            prev = time;
        }
    }

    dbg!(&deltas);

    let out = File::create(outfile).unwrap();
    let mut out = BufWriter::new(out);
    
    let sr = 44100;

    for delta in &deltas {
    // let delta = &deltas[0];
        let delta_samps = (*delta * sr as f32) as u32;

        for i in 0..delta_samps {
            let ramp = i as f32 / delta_samps as f32;
            let _ = out.write_all(&ramp.to_le_bytes());
        }
    }
}
