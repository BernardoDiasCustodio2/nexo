"""Day 1 feed arts for NEXO, 1080x1350 JPEG, site identity (Syne / Manrope / Plex Mono, orange-gold on #13121F)."""
import asyncio, base64, os
from playwright.async_api import async_playwright

SP = '/tmp/claude-0/-home-claude/e62978b1-6b0f-5cfc-86fb-8d2eec1af1df/scratchpad/'
OUT = SP + 'day1/out/'
os.makedirs(OUT, exist_ok=True)
FOX = 'data:image/jpeg;base64,' + base64.b64encode(open(SP + 'nexo/assets/fox560.jpg', 'rb').read()).decode()

BASE = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#13121F;--bg2:#1A1930;--fg:#F4EFE6;--muted:#ABA6BD;--acc:#E0663A;--gold:#F7B267;--line:rgba(244,239,230,.12);
--glow:linear-gradient(180deg,#FFF4E6 0%,#F7B267 55%,#E0663A 100%);
--d:'Syne',sans-serif;--b:'Manrope',sans-serif;--m:'IBM Plex Mono',monospace}
html,body{width:1080px;height:1350px;background:var(--bg);color:var(--fg);font-family:var(--b);-webkit-font-smoothing:antialiased;overflow:hidden}
.frame{position:relative;width:1080px;height:1350px;padding:72px 76px;overflow:hidden}
.top{display:flex;justify-content:space-between;align-items:center;font:500 22px/1 var(--m);letter-spacing:.24em;text-transform:uppercase;color:var(--muted)}
.brand{display:flex;align-items:center;gap:14px;color:var(--fg)}
.brand img{width:44px;height:44px;border-radius:50%;object-fit:cover;border:1.5px solid rgba(247,178,103,.5)}
.grad{background:var(--glow);-webkit-background-clip:text;background-clip:text;color:transparent}
.eyebrow{display:inline-flex;align-items:center;gap:14px;font:500 22px/1 var(--m);letter-spacing:.22em;text-transform:uppercase;color:var(--gold)}
.eyebrow::before{content:"";width:12px;height:12px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 6px rgba(224,102,58,.18),0 0 18px var(--acc)}
"""

# ---------------- P1: blueprint anatomy (single image) ----------------
P1 = """
<style>
.bp{position:absolute;inset:0;background:
 linear-gradient(rgba(247,178,103,.06) 1px,transparent 1px) 0 0/36px 36px,
 linear-gradient(90deg,rgba(247,178,103,.06) 1px,transparent 1px) 0 0/36px 36px,
 radial-gradient(70% 55% at 50% 58%,rgba(224,102,58,.16),transparent 70%),#111020}
h1{font:800 76px/1.02 var(--d);letter-spacing:-.035em;margin-top:30px}
.sub{font:500 27px/1.45 var(--b);color:var(--muted);margin-top:18px;max-width:820px}
.phone{position:absolute;left:390px;top:570px;width:300px;height:600px;border:3px solid rgba(247,178,103,.75);border-radius:44px;padding:22px 18px;
 box-shadow:0 0 0 10px rgba(247,178,103,.06),0 30px 80px -20px rgba(224,102,58,.35)}
.phone .notch{width:90px;height:16px;border-radius:10px;background:rgba(247,178,103,.35);margin:0 auto 18px}
.ph-url{height:26px;border:1.5px dashed rgba(247,178,103,.6);border-radius:13px;font:500 13px/23px var(--m);color:var(--gold);padding-left:12px}
.ph-h{margin-top:22px;height:16px;border-radius:5px;background:var(--fg);width:92%}
.ph-h2{margin-top:9px;height:16px;border-radius:5px;background:var(--fg);width:70%}
.ph-img{margin-top:22px;height:150px;border-radius:14px;border:1.5px dashed rgba(244,239,230,.45);display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.ph-img i{border-radius:8px;background:rgba(244,239,230,.13)}
.ph-info{margin-top:20px;height:12px;border-radius:4px;background:rgba(244,239,230,.35);width:80%}
.ph-info2{margin-top:8px;height:12px;border-radius:4px;background:rgba(244,239,230,.35);width:58%}
.ph-btn{position:absolute;left:18px;right:18px;bottom:26px;height:56px;border-radius:28px;background:#C24E26;font:700 18px/56px var(--b);text-align:center;color:#fff}
.call{position:absolute;display:flex;align-items:flex-start;gap:16px;width:330px}
.call b{flex:none;width:46px;height:46px;border-radius:50%;border:2px solid var(--gold);color:var(--gold);font:600 22px/42px var(--m);text-align:center;background:#111020}
.call h3{font:700 27px/1.15 var(--d);letter-spacing:-.01em}
.call p{font:500 20px/1.35 var(--b);color:var(--muted);margin-top:6px}
.call.r{flex-direction:row}
svg.lines{position:absolute;inset:0}
.foot{position:absolute;left:76px;right:76px;bottom:62px;display:flex;justify-content:space-between;align-items:center;font:500 21px/1 var(--m);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.foot span:last-child{color:var(--gold)}
</style>
<div class="frame"><div class="bp"></div>
 <div style="position:relative">
  <div class="top"><span class="brand"><img src="FOX">Nexo Web</span><span>Raio-X</span></div>
  <h1 style="margin-top:56px">Anatomia de um site<br><span class="grad">que vende.</span></h1>
  <p class="sub">Seis peças que não podem faltar. Confira se o site da sua empresa tem todas.</p>
 </div>
 <svg class="lines" viewBox="0 0 1080 1350"><g transform="translate(0,130)"><g fill="none" stroke="rgba(247,178,103,.55)" stroke-width="2" stroke-dasharray="6 6">
  <path d="M420 491 H360 V520 H340"/><path d="M420 560 H360 V650"/><path d="M420 700 H360 V800 H340"/>
  <path d="M660 491 H720 V520 H740"/><path d="M660 790 H720 V700 H740"/><path d="M660 1012 H720 V900 H740"/>
 </g><g fill="#F7B267"><circle cx="420" cy="491" r="6"/><circle cx="420" cy="560" r="6"/><circle cx="420" cy="700" r="6"/><circle cx="660" cy="491" r="6"/><circle cx="660" cy="790" r="6"/><circle cx="660" cy="1012" r="6"/></g></g></svg>
 <div class="phone"><div class="notch"></div><div class="ph-url">🔒 seunegocio.com.br</div><div class="ph-h"></div><div class="ph-h2"></div>
  <div class="ph-img"><i></i><i></i><i></i><i></i></div><div class="ph-info"></div><div class="ph-info2"></div><div class="ph-btn">Chamar no WhatsApp</div></div>
 <div class="call" style="left:20px;top:600px;flex-direction:row-reverse;text-align:right;width:330px"><b>01</b><div><h3>Domínio próprio e cadeado</h3><p>Endereço com o nome da empresa e https.</p></div></div>
 <div class="call" style="left:20px;top:760px;flex-direction:row-reverse;text-align:right;width:330px"><b>02</b><div><h3>Título que se explica</h3><p>O que você faz e onde, lido em segundos.</p></div></div>
 <div class="call" style="left:20px;top:920px;flex-direction:row-reverse;text-align:right;width:330px"><b>03</b><div><h3>Fotos reais</h3><p>Do seu trabalho, não de banco de imagem.</p></div></div>
 <div class="call" style="left:740px;top:600px;width:300px"><b>04</b><div><h3>Abre rápido no 4G</h3><p>Ninguém espera página carregar.</p></div></div>
 <div class="call" style="left:740px;top:810px;width:300px"><b>05</b><div><h3>Endereço e horário</h3><p>Fáceis de achar, sem rolar muito.</p></div></div>
 <div class="call" style="left:740px;top:1010px;width:300px"><b>06</b><div><h3>WhatsApp à vista</h3><p>Um toque e o cliente já está falando com você.</p></div></div>
 <div class="foot"><span>@nexo.web.b</span><span>Salve para revisar o seu ↗</span></div>
</div>"""

# ---------------- P2: A or B (single image, split) ----------------
P2 = """
<style>
.bgP2{position:absolute;inset:0;background:radial-gradient(60% 40% at 50% 100%,rgba(224,102,58,.18),transparent 70%),var(--bg)}
h1{font:800 84px/1 var(--d);letter-spacing:-.04em;text-align:center;margin-top:40px}
.sub{font:500 26px/1.4 var(--b);color:var(--muted);text-align:center;margin-top:16px}
.cols{position:absolute;left:60px;right:60px;top:450px;display:grid;grid-template-columns:1fr 1fr;gap:28px}
.opt{position:relative;border-radius:30px;border:1.5px solid var(--line);background:#1A1930;padding:66px 26px 26px;height:660px}
.tag{position:absolute;top:-46px;left:50%;transform:translateX(-50%);width:92px;height:92px;border-radius:50%;font:800 52px/88px var(--d);text-align:center;border:3px solid var(--gold);background:var(--bg);color:var(--gold)}
.opt.b .tag{background:var(--acc);border-color:var(--acc);color:#fff}
.mock{border-radius:18px;overflow:hidden;background:#F4EFE6;color:#2a2633;height:568px;position:relative}
.mbar{height:44px;background:#e6e0d6;display:flex;align-items:center;gap:7px;padding:0 14px}
.mbar i{width:10px;height:10px;border-radius:50%;background:#c9c2b6}
/* A: photo-first, vague */
.a-hero{height:280px;background:linear-gradient(135deg,#d9a46b,#b8674a 60%,#7a3f3a);position:relative}
.a-hero::after{content:"";position:absolute;left:50%;top:50%;width:150px;height:110px;transform:translate(-50%,-50%);border-radius:50% 50% 46% 46%;background:radial-gradient(circle at 50% 35%,#fff4e6,#f3c9a1 60%,#e9a77b);box-shadow:0 18px 30px rgba(0,0,0,.25)}
.a-txt{padding:24px 22px}
.a-txt h4{font:700 30px/1.15 var(--d);letter-spacing:-.02em}
.a-txt p{font:500 17px/1.45 var(--b);color:#6b6577;margin-top:10px}
.a-btn{display:inline-block;margin-top:18px;padding:10px 22px;border:2px solid #2a2633;border-radius:24px;font:700 16px var(--b)}
/* B: offer-first */
.b-txt{padding:30px 22px 0}
.b-k{font:600 13px/1 var(--m);letter-spacing:.18em;text-transform:uppercase;color:#b0532f}
.b-txt h4{font:800 33px/1.08 var(--d);letter-spacing:-.025em;margin-top:12px}
.b-txt p{font:500 17px/1.45 var(--b);color:#6b6577;margin-top:12px}
.b-btn{margin:20px 22px 0;height:58px;border-radius:30px;background:#1FAF57;color:#fff;font:700 19px/58px var(--b);text-align:center}
.b-row{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:22px 22px 0}
.b-row i{height:92px;border-radius:12px;background:linear-gradient(135deg,#e9c49b,#c97d57)}
.b-row i:nth-child(2){background:linear-gradient(135deg,#f3d6c4,#d99a8a)}
.b-row i:nth-child(3){background:linear-gradient(135deg,#e0b98f,#a9694c)}
.note{position:absolute;left:0;right:0;bottom:118px;text-align:center;font:500 20px/1 var(--m);letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.cta{position:absolute;left:76px;right:76px;bottom:46px;display:flex;justify-content:center;font:700 30px/1 var(--d)}
</style>
<div class="frame"><div class="bgP2"></div>
 <div style="position:relative"><div class="top"><span class="brand"><img src="FOX">Nexo Web</span><span>Teste rápido</span></div>
  <h1>Qual você <span class="grad">clicaria?</span></h1>
  <p class="sub">Duas versões do mesmo site de confeitaria. Você é o cliente.</p></div>
 <div class="cols">
  <div class="opt"><div class="tag">A</div><div class="mock"><div class="mbar"><i></i><i></i><i></i></div><div class="a-hero"></div>
   <div class="a-txt"><h4>Bem-vindo ao nosso site</h4><p>Paixão por doces desde sempre. Qualidade e carinho em cada detalhe.</p><span class="a-btn">Saiba mais</span></div></div></div>
  <div class="opt b"><div class="tag">B</div><div class="mock"><div class="mbar"><i></i><i></i><i></i></div>
   <div class="b-txt"><div class="b-k">Taguatinga · DF</div><h4>Bolos de festa sob encomenda</h4><p>Escolha o sabor, a data e receba em casa.</p></div>
   <div class="b-btn">Encomendar no WhatsApp</div><div class="b-row"><i></i><i></i><i></i></div></div></div>
 </div>
 <p class="note">Confeitaria fictícia, criada para o teste</p>
 <div class="cta"><span>Comente <span class="grad">A</span> ou <span class="grad">B</span> 👇</span></div>
</div>"""

# ---------------- P3: plan finder carousel (5 slides, flowchart concept) ----------------
P3_CSS = """
<style>
.bgP3{position:absolute;inset:0;background:radial-gradient(55% 45% at 85% 10%,rgba(247,178,103,.13),transparent 70%),radial-gradient(60% 50% at 0% 100%,rgba(224,102,58,.14),transparent 70%),var(--bg)}
.rail{position:absolute;left:118px;top:300px;bottom:230px;width:3px;background:linear-gradient(var(--gold),rgba(247,178,103,.15))}
.qn{font:600 24px/1 var(--m);letter-spacing:.2em;text-transform:uppercase;color:var(--gold)}
.q{font:800 64px/1.06 var(--d);letter-spacing:-.035em;margin-top:22px}
.yes{display:flex;align-items:center;gap:18px;margin-top:56px;font:600 26px/1 var(--m);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.yes i{width:90px;height:3px;background:var(--gold);position:relative}
.yes i::after{content:"";position:absolute;right:-2px;top:-7px;border:8px solid transparent;border-left:13px solid var(--gold)}
.card{margin-top:30px;border-radius:30px;padding:40px 44px;background:linear-gradient(160deg,rgba(247,178,103,.10),rgba(224,102,58,.05));border:1.5px solid rgba(247,178,103,.35)}
.card h3{font:800 54px/1 var(--d);letter-spacing:-.03em}
.price{font:600 30px/1 var(--m);color:var(--gold);margin-top:16px;letter-spacing:.02em}
.card ul{list-style:none;margin-top:26px;display:grid;gap:14px}
.card li{font:600 27px/1.25 var(--b);display:flex;gap:14px}
.card li::before{content:"";flex:none;width:12px;height:12px;margin-top:10px;border-radius:50%;background:var(--acc)}
.no{position:absolute;left:76px;right:76px;bottom:120px;font:600 24px/1.4 var(--m);letter-spacing:.06em;color:var(--muted)}
.no b{color:var(--fg);font-weight:600}
.pg{position:absolute;left:76px;right:76px;bottom:56px;display:flex;justify-content:space-between;font:500 21px/1 var(--m);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.dots{display:flex;gap:10px}.dots i{width:12px;height:12px;border-radius:50%;background:rgba(244,239,230,.2)}.dots i.on{background:var(--gold)}
</style>"""

def dots(n):
    return '<span class="dots">' + ''.join(f'<i class="{"on" if i == n else ""}"></i>' for i in range(5)) + '</span>'

def qslide(n, q, plan, price, items, no):
    return P3_CSS + f"""<div class="frame"><div class="bgP3"></div><div style="position:relative">
<div class="top"><span class="brand"><img src="FOX">Nexo Web</span><span>{n + 1} / 5</span></div>
<div style="margin-top:96px"><div class="qn">Pergunta {n}</div><div class="q">{q}</div>
<div class="yes"><span>Se a resposta é sim</span><i></i></div>
<div class="card"><h3>{plan}</h3><div class="price">{price}</div><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul></div></div></div>
<div class="no">{no}</div>
<div class="pg"><span>@nexo.web.b</span>{dots(n)}</div></div>"""

P3 = [
 P3_CSS + """<div class="frame"><div class="bgP3"></div>
<div style="position:relative"><div class="top"><span class="brand"><img src="FOX">Nexo Web</span><span>1 / 5</span></div>
<div class="eyebrow" style="margin-top:120px">Guia rápido</div>
<div style="font:800 104px/.98 var(--d);letter-spacing:-.045em;margin-top:34px">Qual site<br>a sua empresa<br><span class="grad">precisa?</span></div>
<p style="font:500 32px/1.45 var(--b);color:var(--muted);margin-top:40px;max-width:820px">Responda 3 perguntas e descubra o plano certo, sem pagar por o que você não vai usar.</p></div>
<svg style="position:absolute;right:70px;bottom:190px" width="330" height="250" viewBox="0 0 330 250" fill="none">
 <rect x="2" y="95" width="96" height="60" rx="16" stroke="#F7B267" stroke-width="3"/><path d="M98 125 H140 M140 40 V210 M140 40 H180 M140 125 H180 M140 210 H180" stroke="#F7B267" stroke-width="3"/>
 <rect x="180" y="12" width="146" height="56" rx="16" fill="rgba(247,178,103,.12)" stroke="#F7B267" stroke-width="2"/>
 <rect x="180" y="97" width="146" height="56" rx="16" fill="rgba(224,102,58,.25)" stroke="#E0663A" stroke-width="2"/>
 <rect x="180" y="182" width="146" height="56" rx="16" fill="rgba(247,178,103,.12)" stroke="#F7B267" stroke-width="2"/></svg>
<div class="pg"><span>Arraste para começar →</span>""" + dots(0) + "</div></div>",
 qslide(1, 'Você precisa de <span class="grad">uma página só</span>, para divulgar um produto ou captar contatos?', 'Essencial', 'R$ 400 a R$ 600',
        ['Landing page de 1 página', 'Botão de WhatsApp', 'Versão para celular', 'Certificado de segurança (SSL)'], 'Precisa de mais páginas? <b>Arraste →</b>'),
 qslide(2, 'Quer apresentar <span class="grad">a empresa inteira</span> e aparecer no Google?', 'Profissional', 'R$ 700 a R$ 1.200',
        ['Até 5 páginas', 'Design exclusivo', 'Otimização para o Google', 'Formulário de contato', 'Integração com Instagram'], 'Vai publicar novidades sempre? <b>Arraste →</b>'),
 qslide(3, 'Vai publicar <span class="grad">novidades sempre</span> e quer alguém cuidando do site todo mês?', 'Premium', 'R$ 1.700 a R$ 2.500',
        ['Tudo do Profissional', 'Páginas ilimitadas', 'Blog ou catálogo', 'Manutenção mensal'], 'Valores de referência. O valor final vem na proposta.'),
 P3_CSS + """<div class="frame"><div class="bgP3"></div>
<div style="position:relative;text-align:center"><div class="top"><span class="brand"><img src="FOX">Nexo Web</span><span>5 / 5</span></div>
<img src="FOX" style="width:230px;height:230px;border-radius:50%;object-fit:cover;margin-top:120px;border:2px solid rgba(247,178,103,.5);box-shadow:0 0 0 14px rgba(224,102,58,.08),0 30px 90px -20px rgba(224,102,58,.6)">
<div style="font:800 84px/1.02 var(--d);letter-spacing:-.04em;margin-top:60px">Ficou em dúvida<br>entre dois?</div>
<p style="font:500 32px/1.5 var(--b);color:var(--muted);margin:30px auto 0;max-width:760px">Mande <b style="color:var(--fg)">PLANO</b> no direct. A gente entende o seu negócio e indica o melhor caminho.</p>
<div style="display:inline-block;margin-top:54px;padding:24px 46px;border-radius:999px;background:#C24E26;font:700 32px/1 var(--b);color:#fff">Enviar “PLANO” no direct</div></div>
<div class="pg"><span>@nexo.web.b</span>""" + dots(4) + "</div></div>",
]

JOBS = [('p1-anatomia', P1), ('p2-a-ou-b', P2)] + [(f'p3-plano-{i + 1}', s) for i, s in enumerate(P3)]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1350})
        for name, body in JOBS:
            await pg.set_content('<html><head><style>' + BASE + '</style></head><body>' + body.replace('FOX', FOX).replace('src="FOX"', '') + '</body></html>')
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(150)
            await pg.screenshot(path=OUT + name + '.jpg', type='jpeg', quality=92)
        await b.close()
asyncio.run(main())
print('ok')
