"""Audio for the domain reel: warm minimal electronic bed (90 BPM), soft scene whooshes, typing clicks, stamp, alert ping, narration on top with ducking."""
import json, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve, resample_poly
from scipy.io import wavfile

D = '/tmp/claude-0/-home-claude/e62978b1-6b0f-5cfc-86fb-8d2eec1af1df/scratchpad/day1/r2/'
TL = json.load(open(D + 'timeline.json'))
SR = 44100; TOTAL = TL['total']; N = int(SR * TOTAL)
BEAT = 60 / 90; BAR = 4 * BEAT
rng = np.random.default_rng(5)
flt = lambda x, k, f, o=2: sosfilt(butter(o, f, k, fs=SR, output='sos'), x)


def place(buf, sig, t):
    i = int(t * SR)
    if i < 0 or i >= len(buf): return
    j = min(len(buf), i + len(sig)); buf[i:j] += sig[:j - i]


# Am9 - Fmaj7 - C - G6 (soft pads + plucks)
PROG = [[220.0, 261.63, 329.63, 493.88], [174.61, 220.0, 261.63, 329.63], [196.0, 261.63, 329.63, 392.0], [196.0, 246.94, 293.66, 329.63]]
BASS = [55.0, 43.65, 65.41, 49.0]
pad = np.zeros(N); pl = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N); fx = np.zeros(N)
nb = int(TOTAL // BAR) + 1
for b in range(nb):
    ch = PROG[b % 4]; t0 = b * BAR
    n = int(BAR * SR * 1.1); t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * 0.3 * t)) + 0.3 * np.sin(2 * np.pi * f * 2.001 * t) for f in ch) / 4
    env = np.minimum(1, t / 0.6) * np.exp(-t * 0.35)
    place(pad, s * env * 0.35, t0)
    for k, st in enumerate([0, 3, 6, 8, 11, 14]):  # pluck arpeggio on 16ths
        f = ch[k % 4] * 2; m = int(0.35 * SR); tt = np.arange(m) / SR
        place(pl, (np.sin(2 * np.pi * f * tt) + 0.4 * np.sin(2 * np.pi * 2 * f * tt)) * np.exp(-tt * 9) * 0.22, t0 + st * BEAT / 4)
    m = int(BAR * SR); tt = np.arange(m) / SR
    place(bass, np.sin(2 * np.pi * BASS[b % 4] * tt) * np.minimum(1, tt / 0.05) * np.exp(-tt * 0.8) * 0.5, t0)
    if b >= 1:
        for st in range(16):
            tt0 = t0 + st * BEAT / 4
            if st in (0, 10):
                m = int(0.25 * SR); tt = np.arange(m) / SR
                place(drums, np.sin(2 * np.pi * np.cumsum(48 + 70 * np.exp(-tt * 28)) / SR) * np.exp(-tt * 10) * 0.7, tt0)
            if st in (4, 12):
                m = int(0.18 * SR); tt = np.arange(m) / SR
                place(drums, flt(rng.standard_normal(m), 'band', [1500, 8000]) * np.exp(-tt * 24) * 0.22, tt0)  # soft clap
            m = int(0.03 * SR); tt = np.arange(m) / SR
            place(drums, flt(rng.standard_normal(m), 'high', 9000) * np.exp(-tt * 90) * (0.10 if st % 2 == 0 else 0.05), tt0)
ir = flt(rng.standard_normal(int(1.2 * SR)), 'low', 5000) * np.exp(-np.arange(int(1.2 * SR)) / SR * 4); ir /= np.sqrt((ir ** 2).sum())
music = pad + pl + bass * 0.8 + drums + fftconvolve(pad + pl, ir)[:N] * 0.35
music = flt(music, 'high', 30); music /= np.abs(music).max() + 1e-9
fade_in = np.minimum(1, np.arange(N) / (SR * 1.0)); music *= fade_in

C = TL['clauses']; S = {int(k): v for k, v in TL['scenes'].items()}
for k in range(2, 7):  # scene whoosh
    m = int(0.5 * SR); tt = np.arange(m) / SR
    place(fx, flt(rng.standard_normal(m), 'band', [400, 4000]) * np.sin(np.pi * tt / tt[-1]) ** 2 * 0.18, S[k] - 0.3)
ts = C[3]['start'] - 0.1  # typing clicks while the address types (18 chars over 1.5 s)
for i in range(18):
    m = int(0.03 * SR); tt = np.arange(m) / SR
    place(fx, flt(rng.standard_normal(m), 'band', [2000, 7000]) * np.exp(-tt * 140) * (0.25 + 0.1 * rng.random()), ts + i * 1.5 / 18 + 0.02 * rng.random())
st = C[7]['start'] + 1.6  # stamp thud
m = int(0.35 * SR); tt = np.arange(m) / SR
place(fx, (np.sin(2 * np.pi * (55 + 70 * np.exp(-tt * 22)) * tt) * np.exp(-tt * 13) + flt(rng.standard_normal(m), 'low', 1800) * np.exp(-tt * 30) * 0.5) * 0.7, st)
at = C[9]['start']  # alert ping (two soft tones)
for j, f in enumerate([880, 660]):
    m = int(0.5 * SR); tt = np.arange(m) / SR
    place(fx, np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) * 0.2, at + j * 0.14)
m = int(0.25 * SR); tt = np.arange(m) / SR  # strike swipe on "não é seu"
place(fx, flt(rng.standard_normal(m), 'band', [1200, 6000]) * np.sin(np.pi * tt / tt[-1]) * 0.18, C[1]['start'])

voice = np.zeros(N)
for c in C:
    sr, v = wavfile.read(c['wav']); v = v.astype(np.float64) / 32767
    place(voice, resample_poly(v, 147, 80), c['start'])
voice = flt(voice, 'high', 90); voice = voice + 0.25 * flt(voice, 'band', [2800, 7000]) + 0.12 * flt(voice, 'band', [160, 380])
voice = np.tanh(voice * 1.4) / np.tanh(1.4)
env = np.convolve(np.abs(voice), np.ones(int(0.05 * SR)) / int(0.05 * SR), 'same'); env = np.clip(env / (env.max() + 1e-9) * 3, 0, 1)
sm = np.zeros(N); cur = 0.0
for i in range(0, N, 64):
    tg = env[i]; cur += (tg - cur) * (0.3 if tg > cur else 0.08); sm[i:i + 64] = cur
mix = music * 0.30 * (1 - 0.55 * sm) + fx * 0.8 + voice * 1.0
st2 = np.stack([mix, mix], 1); st2 /= np.abs(st2).max() + 1e-9; st2 = np.tanh(st2 * 1.2) / np.tanh(1.2) * 0.92
fo = int(1.6 * SR); st2[-fo:] *= np.linspace(1, 0, fo)[:, None]
wavfile.write(D + 'mix.wav', SR, (st2 * 32767).astype(np.int16))
print('ok', TOTAL)
