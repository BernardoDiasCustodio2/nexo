"""Unboxing reel audio: box landing thud, tape rip, lid creak + shimmer, a soft 'pop' and rising pluck per item,
a minimal lo-fi groove that swells on the final screen, and a stamp on the shipping label."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

D = '/tmp/claude-0/-home-claude/e62978b1-6b0f-5cfc-86fb-8d2eec1af1df/scratchpad/day1/r3/'
SR = 44100; TOTAL = 23.0; N = int(SR * TOTAL)
rng = np.random.default_rng(21)
flt = lambda x, k, f, o=2: sosfilt(butter(o, f, k, fs=SR, output='sos'), x)
fx = np.zeros(N); mus = np.zeros(N)


def place(buf, sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if 0 <= i < N: buf[i:j] += sig[:j - i] * g


def env_t(d): return np.arange(int(d * SR)) / SR


# thud as the box lands (~0.5 s)
t = env_t(.4); place(fx, np.sin(2 * np.pi * (45 + 60 * np.exp(-t * 25)) * t) * np.exp(-t * 12) + flt(rng.standard_normal(len(t)), 'low', 900) * np.exp(-t * 30) * .4, .45, .8)
# tape rip 1.4-2.3: crackly band noise with irregular amplitude
t = env_t(.9); crack = flt(rng.standard_normal(len(t)), 'band', [1800, 9000]) * (0.4 + 0.6 * (rng.random(len(t)) > .7)) * np.sin(np.pi * t / t[-1]) ** .5
place(fx, crack, 1.4, .35)
# lid: soft cardboard creak + shimmer
t = env_t(.8); place(fx, flt(rng.standard_normal(len(t)), 'band', [200, 900]) * np.sin(np.pi * t / t[-1]) * .5, 2.6, .5)
t = env_t(2.2); shimmer = sum(np.sin(2 * np.pi * f * t) for f in [1567.98, 2093.0, 2637.0, 3135.96]) / 4 * np.minimum(1, t / .4) * np.exp(-t * 1.5)
place(fx, shimmer, 2.8, .12)
# items: pop + rising pluck
notes = [523.25, 587.33, 659.25, 783.99, 880.0]
for k, s in enumerate([3.6, 6.4, 9.2, 12.0, 14.8]):
    t = env_t(.08); place(fx, np.sin(2 * np.pi * (500 + 900 * t / t[-1]) * t) * np.exp(-t * 50), s + .05, .45)
    t = env_t(.7); place(fx, (np.sin(2 * np.pi * notes[k] * t) + .4 * np.sin(2 * np.pi * 2 * notes[k] * t)) * np.exp(-t * 6), s + .1, .25)
    t = env_t(.35); place(fx, flt(rng.standard_normal(len(t)), 'band', [600, 3000]) * np.sin(np.pi * t / t[-1]) ** 2, s + 2.4, .12)  # tuck into the chip row
# stamp on the label at 20.0
t = env_t(.35); place(fx, (np.sin(2 * np.pi * (60 + 70 * np.exp(-t * 22)) * t) * np.exp(-t * 14) + flt(rng.standard_normal(len(t)), 'low', 1600) * np.exp(-t * 28) * .5), 20.0, .75)
# lo-fi groove from 3.4, swells at 17.6
BEAT = 60 / 84
chords = [[261.63, 329.63, 392.0, 493.88], [220.0, 261.63, 329.63, 392.0], [174.61, 220.0, 261.63, 329.63], [196.0, 246.94, 293.66, 349.23]]
start = 3.4; b = 0
while start + b * 4 * BEAT < TOTAL:
    t0 = start + b * 4 * BEAT; ch = chords[b % 4]
    t = env_t(4 * BEAT * 1.05)
    pad = sum(np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * f * 2.003 * t) for f in ch) / 4 * np.minimum(1, t / .3) * np.exp(-t * .35)
    place(mus, pad, t0, .3)
    for st in range(8):
        tt = t0 + st * BEAT / 2 + (0.03 if st % 2 else 0)
        if st in (0, 5):
            tk = env_t(.22); place(mus, np.sin(2 * np.pi * np.cumsum(48 + 60 * np.exp(-tk * 26)) / SR) * np.exp(-tk * 10), tt, .5)
        if st in (2, 6):
            tk = env_t(.16); place(mus, flt(rng.standard_normal(len(tk)), 'band', [1200, 7000]) * np.exp(-tk * 24), tt, .14)
        tk = env_t(.03); place(mus, flt(rng.standard_normal(len(tk)), 'high', 8000) * np.exp(-tk * 90), tt, .05)
    b += 1
ir = flt(rng.standard_normal(int(1.0 * SR)), 'low', 4500) * np.exp(-np.arange(int(1.0 * SR)) / SR * 4); ir /= np.sqrt((ir ** 2).sum())
mus = mus + fftconvolve(mus, ir)[:N] * .25
gain = np.where(np.arange(N) / SR < 17.6, .55, .9); gain = np.convolve(gain, np.ones(SR // 2) / (SR // 2), 'same')
mix = flt(fx + mus * gain * .6, 'high', 30)
st = np.stack([mix, mix], 1); st /= np.abs(st).max() + 1e-9; st = np.tanh(st * 1.2) / np.tanh(1.2) * .9
fo = int(1.3 * SR); st[-fo:] *= np.linspace(1, 0, fo)[:, None]
wavfile.write(D + 'mix.wav', SR, (st * 32767).astype(np.int16)); print('ok')
