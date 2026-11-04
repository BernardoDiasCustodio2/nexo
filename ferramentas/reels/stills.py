import asyncio,sys
from playwright.async_api import async_playwright
page,times,out=sys.argv[1],[float(x) for x in sys.argv[2].split(',')],sys.argv[3]
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
    await pg.goto('file://'+page); await pg.evaluate('document.fonts.ready')
    from PIL import Image; import io
    ims=[]
    for t in times:
      await pg.evaluate(f'window.seek({t})'); ims.append(Image.open(io.BytesIO(await pg.screenshot())).convert('RGB').resize((360,640)))
    W=len(ims)*370; o=Image.new('RGB',(W,640),'white')
    for i,im in enumerate(ims): o.paste(im,(i*370,0))
    o.save(out); await b.close()
asyncio.run(m())
