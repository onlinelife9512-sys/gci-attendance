from pathlib import Path
import base64,gzip

root=Path(__file__).parent
src=root/"source"
dist=root/"dist"
dist.mkdir(exist_ok=True)

blob="".join((src/f"part{i}.b64").read_text().strip() for i in range(1,6))
html=gzip.decompress(base64.b64decode(blob)).decode("utf-8")

patches=["map-patch.html","timesheet-patch.html","face-login-patch.html","gps-required-patch.html"]
for name in patches:
    p=src/name
    if p.exists():
        html=html.replace("</body>",p.read_text()+"\n</body>",1)

# Exact institute logo: use assets/gyanmanjari-logo.webp when present.
logo=Path("assets/gyanmanjari-logo.webp")
if logo.exists():
    branding='''<style id="gci-brand-logo-css">
.gciExactLogo{display:block;object-fit:contain;max-width:190px;height:auto}
.topbar .gciExactLogo{max-width:155px;max-height:48px}
#authView .gciExactLogo{max-width:220px;margin:0 auto 12px}
</style>
<script id="gci-brand-logo-js">
(function(){
 const src="/assets/gyanmanjari-logo.webp";
 document.querySelectorAll(".wordLogo").forEach(el=>{const img=document.createElement("img");img.src=src;img.alt="Gyanmanjari";img.className="gciExactLogo";el.replaceWith(img)});
 const a=document.querySelector("#authView .authLogo");
 if(a){const img=document.createElement("img");img.src=src;img.alt="Gyanmanjari";img.className="gciExactLogo";a.prepend(img)}
})();
</script>'''
    html=html.replace("</body>",branding+"\n</body>",1)

(dist/"index.html").write_text(html)
print("Built",dist/"index.html",len(html))
