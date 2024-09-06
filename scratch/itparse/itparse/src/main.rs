use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::str;

struct ImpulseTrackerModule {}

impl ImpulseTrackerModule {
    pub fn load_from_buffer(buffer: &[f32]) -> Self {}
}

fn main() -> io::Result<()> {
    let mut f = File::open("../small2.it")?;
    let mut buffer = Vec::new();

    f.read_to_end(&mut buffer)?;

    println!("{}", buffer.len());

    dbg!(&buffer[0..4]);

    let str = str::from_utf8(&buffer[0..4]).unwrap();
    dbg!(str);

    let title = str::from_utf8(&buffer[0x4..0xf]).unwrap();
    dbg!(title);

    // OrdNum
    //dbg!(&buffer[0x20..0x22]);
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

    let pat_off = 0x00C0 + ord_num + ins_num * 4 + smp_num * 4;
    let pat_off = pat_off as usize;
    //let pat_off = buffer[pat_off]
    //    | (buffer[pat_off + 1] << 8)
    //    | (buffer[pat_off + 2] << 16)
    //    | (buffer[pat_off + 3] << 24);

    dbg!(&buffer[pat_off..(pat_off + 4)]);
    let pat_off = u32::from_le_bytes([
        buffer[pat_off],
        buffer[pat_off + 1],
        buffer[pat_off + 2],
        buffer[pat_off + 3],
    ]) as usize;
    dbg!(pat_off);
    // // dbg!(&buffer[0x20..0x22]);

    dbg!(&buffer[pat_off..(pat_off + 8)]);
    let pat_len = buffer[pat_off] as u16 | ((buffer[pat_off + 1] as u16) << 8);
    dbg!(pat_len);
    let pat_rows = buffer[pat_off + 2] as u16 | ((buffer[pat_off + 3] as u16) << 8);
    dbg!(pat_rows);
    // dbg!(&buffer[0xC0..0xCF]);
    // dbg!(&buffer[0xD0..0xDF]);
    //

    // read pattern 1 data

    let mut i = 0;
    let pat_start = pat_off + 8;
    let mut prev_mask_variable = 0;

    let mut last_note: [u8; 4] = [0; 4];
    let mut last_instr = 0;
    let mut last_volpan = 0;
    let mut last_command = 0;
    let mut row_pos = 0;
    while i < pat_len as usize {
        let channel_variable = buffer[pat_start + i];
        i += 1;

        if channel_variable == 0 {
            row_pos += 1;
            //println!("new row: {}", row_pos);
            continue;
        }

        let mask_variable;

        if (channel_variable & 128) > 0 {
            mask_variable = buffer[pat_start + i];
            i += 1;
        } else {
            mask_variable = prev_mask_variable;
        }

        let channel = ((channel_variable - 1) & 63) as usize;

        if (mask_variable & 1) > 0 {
            let note = buffer[pat_start + i];
            last_note[channel] = note;
            i += 1;
            dbg!(channel, note);
        }

        if (mask_variable & 2) > 0 {
            let instr = buffer[pat_start + i];
            last_instr = instr;
            i += 1;
            dbg!(instr);
        }

        if (mask_variable & 4) > 0 {
            let volpan = buffer[pat_start + i];
            last_volpan = volpan;
            i += 1;
            dbg!(volpan);
        }

        if (mask_variable & 8) > 0 {
            let command = buffer[pat_start + i];
            i += 1;
            last_command = command;
            dbg!(command);
        }

        if (mask_variable & 16) > 0 {
            dbg!(last_note);
        }

        if (mask_variable & 32) > 0 {
            dbg!(last_instr);
        }

        if (mask_variable & 64) > 0 {
            dbg!(last_volpan);
        }

        if (mask_variable & 128) > 0 {
            dbg!(last_command);
        }

        prev_mask_variable = mask_variable;
    }

    Ok(())
}

#[test]
fn test_load_buffer() {
    let mut f = File::open("../small2.it").unwrap();
    let mut buffer = Vec::new();
    f.read_to_end(&mut buffer).unwrap();
    let it = ImpulseTrackerModule::load_from_buffer(&buffer);
}
