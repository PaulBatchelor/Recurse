lil([[
loadwav "finetrim_noise.wav"
tick
param 1.3
tsmp zz zz zz

env [tick] 0.001 0.001 0.06
mul zz zz

wavout zz snare.wav
computes 1
]])

