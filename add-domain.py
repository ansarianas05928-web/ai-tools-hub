#!/usr/bin/env python3
"""Usage: python3 add-domain.py https://yourdomain.com
Copies ./site to ./dist and adds canonical, og:url, sitemap.xml and the robots.txt Sitemap line."""
import re, sys, shutil, datetime, pathlib
if len(sys.argv)!=2 or not re.fullmatch(r'https://[a-z0-9]([a-z0-9.-]*[a-z0-9])?\.[a-z]{2,}',sys.argv[1].rstrip('/').lower()):
    sys.exit('Give your full domain, e.g.  python3 add-domain.py https://yourdomain.com')
D=sys.argv[1].rstrip('/').lower(); root=pathlib.Path(__file__).parent
src,dst=root/'site',root/'dist'
shutil.rmtree(dst,ignore_errors=True); shutil.copytree(src,dst)
today=datetime.date.today().isoformat(); urls=[]
for f in sorted(dst.glob('*.html')):
    url=D+'/' if f.name=='index.html' else f'{D}/{f.name}'; urls.append(url)
    h=f.read_text(encoding='utf8')
    if 'rel="canonical"' in h: continue
    h=h.replace('</head>',f'<link rel="canonical" href="{url}">\n<meta property="og:url" content="{url}">\n</head>',1)
    f.write_text(h,encoding='utf8')
(dst/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)+'</urlset>\n',encoding='utf8')
r=(dst/'robots.txt'); r.write_text(r.read_text()+f'\nSitemap: {D}/sitemap.xml\n',encoding='utf8')
print('Done ->',dst,'|',len(urls),'pages in sitemap')
