#!/usr/bin/env python3
from __future__ import annotations
import re
from common import *
PAGES=['index.html','shopping-guide.html','style-by-occasion.html','size-quality.html','global-sites.html','sustainability.html']
def run(date_s):
    changed=False
    for lang in LANGS:
        for page in PAGES:
            path=ROOT/lang/page
            if not path.exists(): continue
            s=read(path)
            s=re.sub(r'<!-- i18n-check: \d{4}-\d{2}-\d{2} lang=[^>]+ -->\n?','',s)
            marker=f'<!-- i18n-check: {date_s} lang={lang} page={page} -->'
            s=s.replace('</head>', marker+'\n</head>', 1)
            changed |= write_if_changed(path,s)
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
