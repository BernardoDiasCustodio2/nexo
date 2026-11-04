"""Audio for the POV reel: clock tick while loading, cheesy chiptune when the old site opens, tap click, error buzz,
crickets at '2019', swipe + 1 s of silence, then a clean warm chord + beat on the NEXO end card."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

D = '/tmp/claude-0/-home-claude/e62978b1-6b0f-5cfc-86fb-8d2eec1af1df/scratchpad/day1/r1/'
SR = 44100; TOTAL = 20.0; N = int(SR * TOTAL)
rng = np.random.default_rng(9)
flt = lambda x, k, f, o=2: sosfilt(butter(o, f, k, fs=SR, output='sos'), x)
out = np.zeros(N)


def place(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if 0 <= i < N: out[i:j] += sig[:j - i] * g


def tone(f, d, kind='sine', decay=6.0):
    t = np.arange(int(d * SR)) / SR
    w = np.sin(2 * np.pi * f * t) if kind == 'sine' else np.sign(np.sin(2 * np.pi * f * t)) * 0.6
    return w * np.exp(-t * decay) * np.minimum(1, t / 0.004)


# 0-3.2 ticking clock
for k in range(7):
    place(flt(rng.standard_normal(int(.02 * SR)), 'band', [2500, 6000]) * np.exp(-np.arange(int(.02 * SR)) / SR * 200), .2 + k * .45, .5)
# 3.2 cheesy chiptune fanfare (square wave), loops softly under the old site
mel = [(523.25, .14), (659.25, .14), (783.99, .14), (1046.5, .3), (987.77, .14), (783.99, .14), (880, .3)]
t0 = 3.2
for rep in range(4):
    tt = t0 + rep * 1.5
    for f, d in mel:
        place(tone(f, d, 'square', 5), tt, .16 if rep == 0 else .08); tt += d * .7
for k in range(12):  # oom-pah bass under it
    place(tone(130.81 if k % 2 == 0 else 196.0, .18, 'square', 9), 3.2 + k * .5, .08)
# 6.5 tap click
place(flt(rng.standard_normal(int(.03 * SR)), 'band', [1500, 5000]) * np.exp(-np.arange(int(.03 * SR)) / SR * 150), 6.5, .5)
# 7.0 error buzz
place(tone(110, .45, 'square', 3) + tone(116, .45, 'square', 3), 7.0, .12)
# 9.4 scroll swish + crickets
place(flt(rng.standard_normal(int(.4 * SR)), 'band', [800, 3000]) * np.hanning(int(.4 * SR)), 9.4, .12)
for k in range(5):
    tt = 10.5 + k * .42
    for j in range(3):
        place(tone(4300, .05, 'sine', 40), tt + j * .06, .07)
# 12.9 swipe up, then silence to 15.8
place(flt(rng.standard_normal(int(.5 * SR)), 'band', [500, 6000]) * np.sin(np.linspace(0, np.pi, int(.5 * SR))) ** 2, 13.9, .3)
# 15.8 end card: warm chord + soft beat
chord = [220.0, 277.18, 329.63, 415.30]
t = np.arange(int(4.2 * SR)) / SR
pad = sum(np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t) for f in chord) / 4 * np.minimum(1, t / .08) * np.exp(-t * .5)
ir = flt(rng.standard_normal(int(1.0 * SR)), 'low', 5000) * np.exp(-np.arange(int(1.0 * SR)) / SR * 4); ir /= np.sqrt((ir ** 2).sum())
place(pad + fftconvolve(pad, ir)[:len(pad)] * .3, 15.8, .35)
for k in range(8):
    bt = 15.8 + k * .5
    m = int(.22 * SR); tt = np.arange(m) / SR
    if k % 2 == 0: place(np.sin(2 * np.pi * np.cumsum(50 + 80 * np.exp(-tt * 28)) / SR) * np.exp(-tt * 10), bt, .55)
    else: place(flt(rng.standard_normal(m), 'band', [1500, 8000]) * np.exp(-tt * 22), bt, .15)
mix = flt(out, 'high', 30)
st = np.stack([mix, mix], 1); st /= np.abs(st).max() + 1e-9; st = np.tanh(st * 1.2) / np.tanh(1.2) * .9
fo = int(1.2 * SR); st[-fo:] *= np.linspace(1, 0, fo)[:, None]
wavfile.write(D + 'mix.wav', SR, (st * 32767).astype(np.int16)); print('ok')
