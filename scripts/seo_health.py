#!/usr/bin/env python3
from __future__ import annotations
import re
from common import *
def run(date_s):
    changed=False
    changed |= ensure_robots()
    changed |= update_sitemap(date_s)
    pages=[ROOT/'index.html']+[p for lang in LANGS for p in (ROOT/lang).glob('*.html')]
    for path in pages:
        s=read(path)
        if '<meta name="description"' not in s:
            s=s.replace('<title>', '<meta name="description" content="SheinLookbook.xyz fashion shopping guide"/>\n<title>', 1)
        s=re.sub(r'<img([^>]*?)alt=""', r'<img\1alt="SheinLookbook fashion image"', s)
        changed |= write_if_changed(path,update_dates(s,date_s))
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
