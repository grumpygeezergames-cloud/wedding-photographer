from pathlib import Path
import sys
source = Path("Index.html")
assert source.is_file(), "Missing Index.html"
html = source.read_text(encoding="utf-8")
style = """
<style id="mobile-game-layout">
html,body{margin:0;overflow-x:hidden;background:#241c2b}
.app{max-width:none;width:100%;padding:0}
.top{padding:5px 12px;background:#241c2b;color:#fff}
.top h1{font-size:16px;margin:2px 0}
.top small{font-size:11px;color:#e6d6e5}
.top #newBtn{display:none}
.panel{margin:0;border-radius:0;box-shadow:none;padding:0;background:#241c2b}
.panel:has(.stage){position:relative}
.panel:has(.stage)>.controls{display:none}
.panel:has(.stage)>.hud{display:none}
.stage{width:100%;border-radius:0;overflow:hidden;background:#b8ddc4}
.stage canvas{display:block;width:100%;height:auto;aspect-ratio:16/9}
.stage .hud{position:absolute;top:0;left:0;right:0;z-index:3;padding:7px 12px;margin:0;background:linear-gradient(#201527aa,#20152700);color:white;pointer-events:none;justify-content:flex-start}
.stage .hud strong{font-size:12px;text-shadow:0 1px 3px #000}
.stage .hud .hint{color:white;font-size:11px;text-shadow:0 1px 3px #000}
.stage .bottom{position:absolute;left:0;right:0;bottom:0;z-index:4;display:flex;align-items:flex-end;justify-content:center;gap:12px;margin:0;padding:20px 12px 8px;background:linear-gradient(transparent,#20152788);pointer-events:none}
.stage .bottom>*{display:none!important}
.stage .bottom>.controls{display:none}
.stage .shutter{width:66px;height:66px;flex:none;box-shadow:0 2px 8px #0006}
.stage #next{display:none;position:absolute;right:10px;bottom:12px;max-width:34%;padding:9px 10px;font-size:11px;line-height:1.1}
.legend,.footer{display:none}
.panel:has(.photo-strip){background:#fff;padding:9px 12px}
.viewfinder{width:46%;height:69%}
@media(orientation:landscape) and (max-height:550px){
.top{padding:2px 9px}.top h1{font-size:13px}.top small{display:none}
.stage{width:min(100vw,calc((100dvh - 40px)*16/9));margin:auto}
.stage .bottom{padding-bottom:4px}.stage .shutter{width:54px;height:54px}
.stage .hud{padding:4px 10px}
}
@media(orientation:portrait) and (max-width:600px){
.top{padding:6px 10px}.stage .hud .hint{display:none}
.stage #next{font-size:10px;padding:7px;max-width:33%}
}
</style>
"""
js = """
<script id="mobile-game-controls">
(()=>{
 const stage=document.getElementById('stage');
 const hud=document.querySelector('.panel .hud');
 const bottom=document.querySelector('.panel .bottom');
 if(!stage||!hud||!bottom)return;
 stage.appendChild(hud);
 stage.appendChild(bottom);
 for(const btn of bottom.querySelectorAll('button')){
   btn.addEventListener('pointerdown',e=>e.stopPropagation());
   btn.addEventListener('pointerup',e=>e.stopPropagation());
   btn.addEventListener('dblclick',e=>e.stopPropagation());
 }
})();
</script>
"""
assert "</head>" in html and "</body>" in html
# Replace double-tap-to-shoot with single tap/click, while preserving drag-to-aim.
old = """  if(e.pointerType!=='mouse'&&!dragMoved){
    const now=performance.now();
    if(now-lastTap<350&&Math.hypot(e.clientX-lastTapX,e.clientY-lastTapY)<45){take();lastTap=0;}
    else {lastTap=now;lastTapX=e.clientX;lastTapY=e.clientY;}
  }"""
new = """  if(!dragMoved && (e.pointerType!=='mouse'||e.button===0))take();"""
assert old in html, "Could not locate existing tap handler"
html=html.replace(old,new,1)
old_double = """$('stage').addEventListener('dblclick',e=>{e.preventDefault();take()});"""
assert old_double in html, "Could not locate double-click handler"
html=html.replace(old_double,"",1)
html=html.replace("</head>",style+"</head>",1)
html=html.replace("</body>",js+"</body>",1)
out=Path("site")
out.mkdir(exist_ok=True)
(out/"index.html").write_text(html,encoding="utf-8")
print("Prepared mobile-first game:",(out/"index.html").stat().st_size,"bytes")
