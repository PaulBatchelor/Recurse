use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::str;

fn main() -> io::Result<()> {
    let mut f = File::open("../small.it")?;
    let mut buffer = Vec::new();

    f.read_to_end(&mut buffer)?;

    println!("{}", buffer.len());

    dbg!(&buffer[0..4]);

    let str = str::from_utf8(&buffer[0..4]).unwrap();
    dbg!(str);

    let title = str::from_utf8(&buffer[0x4..0xf]).unwrap();
    dbg!(title);

    // OrdNum
    dbg!(&buffer[0x20..0x22]);
    let ord_num: u16 = buffer[0x20] as u16 | ((buffer[0x21] as u16) << 8);
    dbg!(ord_num);
    let ins_num: u16 = buffer[0x22] as u16 | ((buffer[0x23] as u16) << 8);
    dbg!(ins_num);
    let smp_num: u16 = buffer[0x24] as u16 | ((buffer[0x25] as u16) << 8);
    dbg!(smp_num);
    let pat_num: u16 = buffer[0x26] as u16 | ((buffer[0x27] as u16) << 8);
    dbg!(pat_num);
    let cwt_v: u16 = buffer[0x28] as u16 | ((buffer[0x29] as u16) << 8);
    dbg!(cwt_v);
    //let ord_num = &buffer[0x20..0x22].from_le();

    // dbg!(&buffer[0x20..0x22]);

    // dbg!(&buffer[0xC0..0xCF]);
    // dbg!(&buffer[0xD0..0xDF]);

    Ok(())
}
