#![allow(unused_imports)]
//use rodio::Source;
use std::sync::{Arc, Mutex};
//use xmrs::prelude::*;
//use xmrs::xm::xmmodule::XmModule;
use xmrsplayer::xmrsplayer::XmrsPlayer;

pub const BUFFER_SIZE: usize = 2048;

pub struct BufferedSource<'a> {
    pub player: Arc<Mutex<XmrsPlayer<'a>>>,
    buffer: [f32; BUFFER_SIZE],
    buffer_index: usize,
    sample_rate: u32,
}

impl<'a> BufferedSource<'a> {
    pub fn new(player: Arc<Mutex<XmrsPlayer<'a>>>, sample_rate: u32) -> Self {
        BufferedSource {
            player,
            buffer: [0.0; BUFFER_SIZE],
            buffer_index: 0,
            sample_rate,
        }
    }
}

// impl<'a> Source for BufferedSource<'a> {
//     fn current_frame_len(&self) -> Option<usize> {
//         Some(BUFFER_SIZE - self.buffer_index)
//     }
//     fn channels(&self) -> u16 {
//         2
//     }
//     fn sample_rate(&self) -> u32 {
//         self.sample_rate
//     }
//     fn total_duration(&self) -> Option<std::time::Duration> {
//         None
//     }
// }

impl<'a> Iterator for BufferedSource<'a> {
    type Item = f32;

    fn next(&mut self) -> Option<Self::Item> {
        if !self.player.lock().unwrap().is_samples() {
            return None;
        }

        self.buffer_index += 1;

        if self.buffer_index >= BUFFER_SIZE {
            self.player
                .lock()
                .unwrap()
                .generate_samples(&mut self.buffer);
            self.buffer_index = 0;
        }

        Some(self.buffer[self.buffer_index])
    }
}
