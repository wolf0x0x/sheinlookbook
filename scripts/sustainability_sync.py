#!/usr/bin/env python3
from __future__ import annotations
import re
from common import *
def run(date_s):
    changed=False
    for lang,path in pages_named('sustainability.html'):
        s=read(path); L=LANG[lang]; sep='：' if lang in ('zh','ja') else ':'
        note=f"{L['scan']}{sep}{date_s} · {L['source']}"
        tag=f'<p class="text-xs text-on-surface-variant mt-3" data-sustainability-scan>{esc(note)}</p>'
        if 'data-sustainability-scan' in s:
            s=re.sub(r'<p class="text-xs text-on-surface-variant mt-3" data-sustainability-scan>.*?</p>', tag, s, count=1, flags=re.S)
        else:
            s=re.sub(r'(</header>)', tag+r'\n  \1', s, count=1)
        changed |= write_if_changed(path,update_dates(s,date_s))
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
