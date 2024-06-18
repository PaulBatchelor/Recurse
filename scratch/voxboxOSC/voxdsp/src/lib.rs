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
    listener: OSCServer,
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

    pub fn poll(&mut self) {
        let sock = &self.sock;
        let buf = &mut self.buf;
        match sock.recv_from(buf) {
            Ok((size, addr)) => {
                println!("Received packet with size {} from: {}", size, addr);
                let (_, packet) = rosc::decoder::decode_udp(&self.buf[..size]).unwrap();
                handle_packet(packet);
            }
            Err(e) => {
                println!("Error receiving from socket: {}", e);
            }
        };
    }
}

fn handle_message(msg: OscMessage) {
    let quit = Matcher::new("/quit").unwrap();

    let addr = OscAddress::new(msg.addr.to_string()).unwrap();
    if quit.match_address(&addr) {
        println!("gonna quit now");
    }

    println!("OSC address: {}", msg.addr);
    println!("OSC arguments: {:?}", msg.args);
}

fn handle_packet(packet: OscPacket) {
    match packet {
        OscPacket::Message(msg) => {
            // println!("OSC address: {}", msg.addr);
            // println!("OSC arguments: {:?}", msg.args);
            handle_message(msg);
        }
        OscPacket::Bundle(bundle) => {
            println!("OSC Bundle: {:?}", bundle);
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

#[no_mangle]
pub extern "C" fn vox_poll(vd: &mut VoxData) {
    vd.listener.poll();
}
