mod bufferedsource;
use bufferedsource::*;
use std::sync::Arc;
use std::sync::Mutex;
use voxbox::MonoWav;
use xmrs::prelude::*;
use xmrs::xm::xmmodule::XmModule;
use xmrsplayer::prelude::*;

fn render_module(wavout: &mut MonoWav, module: &mut Box<Module>) {
    let is_ft2 = module.comment == "FastTracker v2.00 (1.04)";

    let player = Arc::new(Mutex::new(XmrsPlayer::new(module, 44100_f32, is_ft2)));

    let mut buf = BufferedSource::new(player, 44100);

    for _ in 0..10 * 44100 {
        let out = buf.next().unwrap();
        _ = buf.next().unwrap();
        wavout.tick(out);
    }
}

fn main() {
    let sr = 44100;
    let mut wavout = MonoWav::new("test.wav");
    //let filename = "DEADLOCK.XM";
    let filename = "tempest-acidjazz.xm";

    let contents = std::fs::read(filename.trim()).unwrap();

    match XmModule::load(&contents) {
        Ok(xm) => {
            drop(contents); // cleanup memory
            print!("XM '{}' loaded...", xm.header.name);
            let module = xm.to_module();
            let mut module = Box::new(module);
            //let module_ref: &'static Module = Box::leak(module);
            drop(xm);
            println!("Playing {} !", module.name);
            render_module(&mut wavout, &mut module);
        }
        Err(e) => {
            panic!("{:?}", e);
        }
    }
}
