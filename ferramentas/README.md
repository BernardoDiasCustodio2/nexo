# Ferramentas de produção da NEXO

Usadas pela rotina diária de conteúdo. Os caminhos dentro dos exemplos apontam para a pasta temporária
da sessão em que foram criados: ajuste para a pasta de trabalho atual.

## Reels (vídeo 1080x1920, 30 fps)
- `reels/render.py página.html segundos saída.mp4` — abre uma página HTML que define `window.seek(t)`,
  captura cada quadro com o Playwright e gera o MP4 (H.264) com ffmpeg. Sem áudio.
- `reels/stills.py página.html 1.5,4,8 saída.jpg` — quadros de conferência lado a lado, para revisar antes de renderizar.
- `reels/exemplos/cena_*.tpl.html` — três cenas completas (tipografia em movimento com legenda; tela de celular POV;
  unboxing). Marcadores: `__FOX__` (raposa em base64), `__TL__` (linha do tempo JSON da voz), `__SITE__` (captura do site).
  São referência de qualidade e de técnica, não modelos para copiar: cada Reel novo tem cena e roteiro próprios.
- `reels/exemplos/voz_dominio.py` — narração feminina pt-BR com Kokoro ONNX (voz pf_dora), fonemas IPA escritos à mão,
  gera os trechos WAV e a linha do tempo usada nas legendas.
  Modelo: kokoro-v1.0.onnx e voices-v1.0.bin (release model-files-v1.0 do repositório thewh1teagle/kokoro-onnx);
  vocabulário em src/kokoro_onnx/config.json do mesmo repositório.
- `reels/exemplos/audio_*.py` — trilha e efeitos sintetizados com numpy/scipy, voz por cima com ducking.
- Junte vídeo e áudio: `ffmpeg -i video.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -shortest final.mp4`.

## Posts (1080x1350 JPEG)
- `exemplo_artes_posts.py` — artes do dia 2026-11-04 em HTML/CSS renderizadas com Playwright.
