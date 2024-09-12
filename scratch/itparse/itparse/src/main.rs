use serde::Serialize;
use std::fs::File;
use std::io;
use std::io::prelude::*;
use std::str;

#[allow(dead_code)]
struct ImpulseTrackerModule {
    title: String,
    ninstr: u16,
    nsamps: u16,
    npatts: u16,
    cwt: u16,
    cmwt: u16,
}

#[allow(dead_code)]
#[derive(Default, Debug, Serialize)]
struct PatternCell {
    #[serde(skip_serializing_if = "Option::is_none")]
    note: Option<u8>,
    #[serde(skip_serializing_if = "Option::is_none")]
    instr: Option<u8>,
    #[serde(skip_serializing_if = "Option::is_none")]
    volpan: Option<u8>,
    #[serde(skip_serializing_if = "Option::is_none")]
    cmd: Option<u8>,
}

#[derive(Debug, Serialize)]
struct PatternCellData {
    channel: u8,
    row: u8,
    cell: PatternCell,
}

pub fn mknum(buffer: &[u8], pos: usize) -> u16 {
    u16::from_le_bytes(buffer[pos..(pos + 2)].try_into().unwrap())
}

#[allow(dead_code)]
impl ImpulseTrackerModule {
    pub fn load_from_buffer(buffer: &[u8]) -> Self {
        // TODO: check header, validate for valid IT module
        let title = str::from_utf8(&buffer[0x4..0xf]).unwrap();
        let _ord_num: u16 = buffer[0x20] as u16 | ((buffer[0x21] as u16) << 8);
        let ninstr: u16 = mknum(buffer, 0x22);
        let nsamps: u16 = mknum(buffer, 0x24);
        let npatts: u16 = mknum(buffer, 0x26);
        let cwt: u16 = mknum(buffer, 0x28);
        let cmwt: u16 = mknum(buffer, 0x2a);
        ImpulseTrackerModule {
            title: title.to_string(),
            ninstr,
            nsamps,
            npatts,
            cwt,
            cmwt,
        }
    }
}

fn parse_pattern(
    buffer: &[u8],
    pat_num: u16,
    ord_num: u16,
    ins_num: u16,
    smp_num: u16,
) -> Vec<PatternCellData> {
    let pat_off = 0x00C0 + ord_num + ins_num * 4 + smp_num * 4 + pat_num * 4;
    let pat_off = pat_off as usize;

    let pat_off = u32::from_le_bytes(buffer[pat_off..(pat_off + 4)].try_into().unwrap()) as usize;

    let pat_len = buffer[pat_off] as u16 | ((buffer[pat_off + 1] as u16) << 8);
    let _pat_rows = buffer[pat_off + 2] as u16 | ((buffer[pat_off + 3] as u16) << 8);
    let mut i = 0;
    let pat_start = pat_off + 8;
    let mut prev_mask_variable = 0;

    // TODO: last_note should be sized based
    // on numbre of channels. I don't think this
    // is explicitely stated anywhere, so it might
    // have to be a growing vector.
    //let mut last_note: [u8; 4] = [0; 4];
    let mut last_note: Vec<u8> = vec![];
    // TODO: these "last" values are on a per-channel
    // basis
    let mut last_instr: Vec<u8> = vec![];
    let mut last_volpan: Vec<u8> = vec![];
    let mut last_command: Vec<u8> = vec![];
    let mut row_pos = 0;

    let mut max_chan = 0;
    let mut pat: Vec<PatternCellData> = vec![];

    while i < pat_len as usize {
        // Each iteration in this loop corresponds
        // to a single "cell" in the loop
        let mut pc = PatternCell::default();

        let channel_variable = buffer[pat_start + i];
        i += 1;

        if channel_variable == 0 {
            row_pos += 1;
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

        if channel > max_chan {
            max_chan = channel + 1;
        }

        if (mask_variable & 1) > 0 {
            let note = buffer[pat_start + i];
            if last_note.len() < (channel + 1) {
                last_note.resize(channel + 1, 0);
            }
            last_note[channel] = note;
            i += 1;
            pc.note = Some(note);
        }

        if (mask_variable & 2) > 0 {
            let instr = buffer[pat_start + i];
            if last_instr.len() < (channel + 1) {
                last_instr.resize(channel + 1, 0);
            }
            last_instr[channel] = instr;
            i += 1;
            pc.instr = Some(instr);
        }

        if (mask_variable & 4) > 0 {
            let volpan = buffer[pat_start + i];
            if last_volpan.len() < (channel + 1) {
                last_volpan.resize(channel + 1, 0);
            }
            last_volpan[channel] = volpan;
            i += 1;
        }

        if (mask_variable & 8) > 0 {
            let command = buffer[pat_start + i];
            if last_command.len() < (channel + 1) {
                last_command.resize(channel + 1, 0);
            }
            i += 1;
            last_command[channel] = command;
        }

        if (mask_variable & 16) > 0 {
            pc.note = Some(last_note[channel]);
        }

        if (mask_variable & 32) > 0 {
            pc.instr = Some(last_instr[channel]);
        }

        if (mask_variable & 64) > 0 {
            pc.volpan = Some(last_volpan[channel]);
        }

        if (mask_variable & 128) > 0 {
            pc.cmd = Some(last_command[channel]);
        }

        prev_mask_variable = mask_variable;
        pat.push(PatternCellData {
            channel: channel as u8,
            row: row_pos,
            cell: pc,
        });
    }

    pat
}

fn main() -> io::Result<()> {
    let mut f = File::open("../small2.it")?;
    let mut buffer = Vec::new();

    f.read_to_end(&mut buffer)?;

    let _str = str::from_utf8(&buffer[0..4]).unwrap();

    let _title = str::from_utf8(&buffer[0x4..0xf]).unwrap();

    // OrdNum
    let ord_num: u16 = buffer[0x20] as u16 | ((buffer[0x21] as u16) << 8);
    let ins_num: u16 = buffer[0x22] as u16 | ((buffer[0x23] as u16) << 8);
    let smp_num: u16 = buffer[0x24] as u16 | ((buffer[0x25] as u16) << 8);
    let pat_num: u16 = buffer[0x26] as u16 | ((buffer[0x27] as u16) << 8);
    let _cwt_v: u16 = buffer[0x28] as u16 | ((buffer[0x29] as u16) << 8);

    let mut patterns = vec![];
    for i in 0..pat_num {
        let pat = parse_pattern(&buffer, i, ord_num, ins_num, smp_num);
        patterns.push(pat);
    }

    let serialized = serde_json::to_string(&patterns).unwrap();

    println!("{}", serialized);

    Ok(())
}

#[test]
fn test_load_buffer() {
    let mut f = File::open("../small2.it").unwrap();
    let mut buffer = Vec::new();
    f.read_to_end(&mut buffer).unwrap();
    let it = ImpulseTrackerModule::load_from_buffer(&buffer);
    dbg!(&it.title);
    assert!(it.title == "pauls song\0");
    assert!(it.ninstr == 2);
    assert!(it.nsamps == 1);
    assert!(it.npatts == 1);
}

#[test]
fn test_pattern_cell_init() {
    let mut pc = PatternCell::default();
    assert!(pc.note.is_none());
    assert!(pc.instr.is_none());
    assert!(pc.volpan.is_none());
    assert!(pc.cmd.is_none());

    pc.note = Some(60);
}
