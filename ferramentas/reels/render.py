"""Frame-accurate renderer: loads an HTML page exposing window.seek(t), screenshots every frame, pipes to ffmpeg.
usage: python3 render.py page.html seconds out.mp4 [fps]"""
import asyncio, subprocess, sys
from playwright.async_api import async_playwright

page_path, dur, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30


async def main():
    n = int(round(dur * fps))
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'mjpeg', '-i', '-',
                           '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + page_path)
        await pg.evaluate('document.fonts.ready')
        await pg.evaluate('window.ready ? window.ready() : null')
        for i in range(n):
            await pg.evaluate(f'window.seek({i / fps:.5f})')
            ff.stdin.write(await pg.screenshot(type='jpeg', quality=93))
            if i % 150 == 0: print('frame', i, '/', n, flush=True)
        await b.close()
    ff.stdin.close(); ff.wait()
    print('done', out)

asyncio.run(main())
