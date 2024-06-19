extern crate rosc;
use voxbox::*;
use rosc::{OscPacket, OscMessage};
use rosc::address::{Matcher, OscAddress};
use std::net::{SocketAddrV4, UdpSocket};
use std::str::FromStr;

#[repr(C)]
pub struct VoxData {
    testvar: f32,
    voice: Voice,
    pitch: f32,
    pitch_smoother: Smoother,
    listener: OSCServer,
    is_running: bool,
}

pub struct OSCServer {
    sock: UdpSocket,
    buf: [u8; rosc::decoder::MTU],
}

impl OSCServer {
    pub fn new(addr_str: &str) -> Self {
        let addr = match SocketAddrV4::from_str(&addr_str) {
            Ok(addr) => addr,
            Err(_) => panic!("oops"),
        };

        let sock = UdpSocket::bind(addr).unwrap();
        OSCServer {
            sock: sock,
            buf: [0u8; rosc::decoder::MTU],
        }
    }
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
            listener: OSCServer::new("127.0.0.1:8001"),
            is_running: true,
            pitch: 60.,
            pitch_smoother: Smoother::new(sr),
        };

        vd.pitch_smoother.set_smooth(0.07);
        vd.voice.pitch = 60.;
        vd.voice.tract.drm(&shape1);
        vd
    }

    pub fn tick(&mut self) -> f32 {
        self.voice.pitch = self.pitch_smoother.tick(self.pitch);
        self.voice.tick() * 0.8
    }

    pub fn poll(&mut self) {
        let sock = &self.listener.sock;
        let buf = &mut self.listener.buf;
        match sock.recv_from(buf) {
            Ok((size, addr)) => {
                println!("Received packet with size {} from: {}", size, addr);
                let (_, packet) = rosc::decoder::decode_udp(&self.listener.buf[..size]).unwrap();
                self.handle_packet(packet);
            }
            Err(e) => {
                println!("Error receiving from socket: {}", e);
            }
        };
    }

    fn handle_packet(&mut self, packet: OscPacket) {
        match packet {
            OscPacket::Message(msg) => {
                // println!("OSC address: {}", msg.addr);
                // println!("OSC arguments: {:?}", msg.args);
                self.handle_message(msg);
            }
            OscPacket::Bundle(bundle) => {
                println!("OSC Bundle: {:?}", bundle);
            }
        }
    }

    fn handle_message(&mut self, msg: OscMessage) {
        let quit = Matcher::new("/quit").unwrap();
        let voxparams = Matcher::new("/vox/{pitch}").unwrap();

        let addr = OscAddress::new(msg.addr.to_string()).unwrap();
        if quit.match_address(&addr) {
            println!("gonna quit now");
            self.is_running = false;
        }

        if voxparams.match_address(&addr) {
            let path: Vec<_> = msg.addr.split("/").collect();
            dbg!(&path);

            match path[2] {
                "pitch" => {
                    let val = msg.args[0].clone().float().unwrap();
                    self.pitch = val;
                    println!("setting pitch");
                }
                _ => { },
            }
            //println!("setting pitch: {:?}", msg.args);
            //self.voice.pitch = val;
        }

        println!("OSC address: {}", msg.addr);
        println!("OSC arguments: {:?}", msg.args);
    }

    pub fn running(&mut self)->u8 {
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
pub extern "C" fn vox_poll(vd: &mut VoxData) {
    vd.poll();
}

#[no_mangle]
pub extern "C" fn vox_running(vd: &mut VoxData) -> u8 {
    vd.running()
}

#[no_mangle]
pub extern "C" fn vox_free(vd: &mut VoxData) {
    let ptr = unsafe {Box::from_raw(vd)};
    drop(ptr);
}
