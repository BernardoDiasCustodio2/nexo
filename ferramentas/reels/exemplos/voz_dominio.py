"""Narration for the 'domain' reel (pf_dora), clause by clause, with a timeline JSON for video + captions."""
import json, os, unicodedata
import numpy as np, onnxruntime as rt
from scipy.io import wavfile

SP = '/tmp/claude-0/-home-claude/e62978b1-6b0f-5cfc-86fb-8d2eec1af1df/scratchpad/'
T = SP + 'tts/'
OUT = SP + 'day1/r2/'
os.makedirs(OUT + 'v', exist_ok=True)
vocab = json.load(open('/home/claude/thewh1teagle/kokoro-onnx/src/kokoro_onnx/config.json'))['vocab']
voices = np.load(T + 'voices-v1.0.bin')
sess = rt.InferenceSession(T + 'kokoro-v1.0.onnx', providers=['CPUExecutionProvider'])
VOICE, SPEED, SR = 'pf_dora', 1.08, 24000

# (scene, caption, phonemes, gap_after)
LINES = [
 (1, 'Se o domínio do seu site está no nome de outra pessoa…', 'si ʊ domˈinju dʊ sˈew sˈajʧɪ istˈa nʊ nˈomɪ ʤɪ ˈowtɾɐ pesˈoɐ…', 0.25),
 (1, 'o site não é seu.', 'ʊ sˈajʧɪ nˈɐ̃w ˈɛ sˈew.', 0.55),
 (2, 'Domínio é o endereço da sua empresa na internet.', 'domˈinju ˈɛ ʊ ẽdeɾˈesʊ dɐ sˈuɐ ẽpɾˈezɐ nɐ ĩteɾnˈɛʧɪ.', 0.2),
 (2, 'Tipo: padariadoze.com.br', 'ʧˈipʊ: padaɾˈiɐ dˈozɪ, pˈõtʊ kˈõ, pˈõtʊ bˈe ˈɛʁɪ.', 0.45),
 (3, 'O site é a casa. O domínio é o endereço.', 'ʊ sˈajʧɪ ˈɛ ɐ kˈazɐ. ʊ domˈinju ˈɛ ʊ ẽdeɾˈesʊ.', 0.2),
 (3, 'Sem endereço, ninguém chega.', 'sẽj ẽdeɾˈesʊ, nĩɡˈẽj ʃˈeɡɐ.', 0.5),
 (4, 'Domínio .com.br é registrado no Registro.br, com CPF ou CNPJ.', 'domˈinju pˈõtʊ kˈõ pˈõtʊ bˈe ˈɛʁɪ ˈɛ ʁeʒistɾˈadʊ nʊ ʁeʒˈistɾʊ pˈõtʊ bˈe ˈɛʁɪ, kˈõ sˈe pˈe ˈɛfɪ ˈow sˈe ˈɛnɪ pˈe ʒˈɔtɐ.', 0.2),
 (4, 'Confira se está no seu nome, e não no de quem fez o site.', 'kõfˈiɾɐ si istˈa nʊ sˈew nˈomɪ, i nˈɐ̃w nʊ ʤɪ kˈẽj fˈejs ʊ sˈajʧɪ.', 0.5),
 (5, 'E fique de olho na renovação:', 'i fˈikɪ ʤɪ ˈoʎʊ nɐ ʁenovasˈɐ̃w:', 0.15),
 (5, 'domínio vencido pode tirar o site do ar.', 'domˈinju vẽsˈidʊ pˈɔʤɪ ʧiɾˈaʁ ʊ sˈajʧɪ dʊ ˈaʁ.', 0.55),
 (6, 'Não sabe em nome de quem está o seu?', 'nˈɐ̃w sˈabɪ ẽj nˈomɪ ʤɪ kˈẽj istˈa ʊ sˈew?', 0.15),
 (6, 'Manda “DOMÍNIO” no direct que a gente confere com você.', 'mˈɐ̃dɐ domˈinju nʊ dajɾˈɛkʧɪ, ki ɐ ʒˈẽʧɪ kõfˈɛɾɪ kˈõ vosˈe.', 0.2),
]


def synth(ph):
    ph = unicodedata.normalize('NFD', ph)
    toks = [vocab[c] for c in ph if c in vocab]
    bad = sorted({c for c in ph if c not in vocab})
    if bad: print('  dropped', bad)
    style = voices[VOICE][len(toks) - 1].reshape(1, -1).astype(np.float32)
    a = sess.run(None, {'tokens': np.array([[0, *toks, 0]], dtype=np.int64), 'style': style, 'speed': np.array([SPEED], dtype=np.float32)})[0].ravel()
    idx = np.where(np.abs(a) > 0.012)[0]
    a = a[max(0, idx[0] - 120): min(len(a), idx[-1] + 1200)]
    return (a / (np.abs(a).max() + 1e-9) * 0.9).astype(np.float32)


clauses = []; t = 0.45; scenes = {}
for k, (sc, cap, ph, gap) in enumerate(LINES):
    a = synth(ph); fn = OUT + 'v/c%02d.wav' % k
    wavfile.write(fn, SR, (a * 32767).astype(np.int16))
    d = len(a) / SR
    scenes.setdefault(sc, round(t - (0.15 if sc > 1 else 0.45), 3))
    clauses.append({'i': k, 'scene': sc, 'text': cap, 'start': round(t, 3), 'end': round(t + d, 3), 'wav': fn})
    print(k, sc, round(d, 2), cap)
    t += d + gap
total = round(t + 2.4, 3)
json.dump({'clauses': clauses, 'scenes': scenes, 'total': total}, open(OUT + 'timeline.json', 'w'), ensure_ascii=False, indent=1)
print('total', total, scenes)
