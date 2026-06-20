#!/usr/bin/env python3
from __future__ import annotations
import re
from common import *
def run(date_s):
    changed=False
    for lang,path in pages_named('global-sites.html'):
        s=read(path); L=LANG[lang]
        sep='：' if lang in ('zh','ja') else ':'
        note=f"{L['updated']}{sep}{date_s} · {L['source']}"
        s=re.sub(r'(<p class="text-xs text-outline mt-2">).*?(</p>)', r'\1'+esc(note)+r'\2', s, count=1, flags=re.S)
        changed |= write_if_changed(path,update_dates(s,date_s))
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
