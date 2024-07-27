lil([[
wavin "pulsereps.wav"
rephasor zz 1
hold zz
regset zz 1

regget 1
phsclk zz 1
hold zz
regset zz 0
]])

lil([[
loadwav "finetrim_click.wav"
regget 0
]])

lil("regget 1")
g = gesture.new()

qrt = {1, 1}
qrt2 = {1, 2}
gliss = 4
linear = 1
zero = 7
gate = 9

gpath = {
    {2, qrt, gliss},
    {1, qrt2, gliss},
    {1.5, qrt, gliss},
    {1, qrt, gliss},
    {1.5, qrt, gliss},
    {1.0, qrt, gliss}
}

for _, v in pairs(gpath) do
    local val = v[1]
    local dur = v[2]
    local bhvr = v[3]
    gesture.append(g, val, dur[1], dur[2], bhvr) 
end

gesture.done(g)
gesture.loop(g)

lil([[
tsmp zz zz zz

regget 0
env zz 0.0001 0.0001 0.01
mul zz zz

buthp zz 2000
]])

lil([[loadwav "snare.wav"]])

-- lil([[
-- regget 0
-- tdiv zz 3 2
-- ]])

lil([[regget 1]])

snare_clock = gesture.new()
gesture.loop(snare_clock)
gesture.alpha(snare_clock)

dotq = {1, 3}

snare_pat = {
    {qrt2, zero},
    {qrt2, gate},
    {dotq, gate},

    {dotq, gate},
    {qrt2, zero},
    {qrt2, zero},
}

for _, v in pairs(snare_pat) do
    local dur = v[1]
    local bhvr = v[2]
    local val = 0
    gesture.append(snare_clock, val, dur[1], dur[2], bhvr) 
end

gesture.done(snare_clock)

lil("gtick zz")

lil([[
param 1.0
tsmp zz zz zz
add zz zz
]])


lil([[
wavout zz "clicker.wav"

computes 10
]])
