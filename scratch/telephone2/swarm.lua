lil("wavin pulsereps.wav")
lil("hold zz")
lil("regset zz 2")


lil("regget 2")

gesture_pitch = gesture.new()

gliss = 4
glisshuge = 6
glisslarge = 5
linear = 1

gpath = {
    {0.5, {1, (7 * 4)}, linear},
    {1, {1, (7 * 4)}, glisslarge},
    {0.6, {1, (7 * 4)}, gliss},
}

for _, v in pairs(gpath) do
    local val = v[1]
    local dur = v[2]
    local bhvr = v[3]
    gesture.append(gesture_pitch, val, dur[1], dur[2], bhvr) 
end

gesture.done(gesture_pitch)

lil([[
hold zz
regset zz 1
]])

lil ([[
loadwav cf_pulse.wav
regset zz 0

# calculated manually
set basepitch [expr (1/2.58) * 0.9]
]])

pitches = {
    0, 14, 13, 12, 11, 10, 9, 8, 7, 6, -12
}

ratios = {}

for _, p in pairs(pitches) do
    local nt = math.pow(3, (p - 13.0) / 13.0)
    table.insert(ratios, nt)
end

phases = {
    0, 0.1, 0.1, 0.2, 0.3, 0.5, 0.7
}

fmt = string.format
for k,v in pairs(ratios) do
    local phasepos = ((k - 1) % #phases) + 1
    local phs = phases[phasepos]
    lil("[regget 0]")
    lil("regget 1")
    lil(fmt("param [expr $basepitch * %g]", v))
    lil("mul zz zz")
    lil(fmt("[phasor zz %g]", phs))
    lil("oscfext zz zz zz")

    if k > 1 then
        lil("add zz zz")
    end
end

lil("mul zz [dblin -3]")

-- weird click in the beggining
-- smooth it out
lil("param 1")
lil("smoother zz 0.001")
lil("mul zz zz")

-- add gate to turn it off as well
lil("regget 2")
gesture_gate = gesture.new()

step = 0

gate_seq = {
    {1, {1, (7 * 8)}, step},
    {0, {1, (7 * 8)}, step},
}

for _, v in pairs(gate_seq) do
    local val = v[1]
    local dur = v[2]
    local bhvr = v[3]
    gesture.append(gesture_gate, val, dur[1], dur[2], bhvr) 
end

gesture.done(gesture_gate)

lil([[
envar zz 0.001 0.2
mul zz zz
]])

lil([[
dup
buthp zz 500
dup
bigverb zz zz 0.9 10000
drop
dcblocker zz
mul zz [dblin -10]
add zz zz
]])

lil([[
dup
vardelay zz 0.6 0.2 2.0
mul zz [dblin -6]
add zz zz
]])
lil([[
wavout zz swarm.wav
computes 20
]])

