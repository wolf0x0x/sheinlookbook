#!/usr/bin/env python3
from __future__ import annotations
from common import *

PROMOS = [
    {'flag':'🇺🇸','code':'DAILY22','discount':'-22% OFF','site':{'zh':'美国站','en':'US','es':'EE. UU.','pt':'EUA','fr':'États-Unis','de':'USA','ja':'米国'}},
    {'flag':'🇪🇸','code':'HOLA18','discount':'-18% OFF','site':{'zh':'西班牙站','en':'Spain','es':'España','pt':'Espanha','fr':'Espagne','de':'Spanien','ja':'スペイン'}},
    {'flag':'🇬🇧','code':'UK12NOW','discount':'£12 OFF','site':{'zh':'英国站','en':'UK','es':'Reino Unido','pt':'Reino Unido','fr':'Royaume-Uni','de':'UK','ja':'英国'}},
    {'flag':'🇦🇺','code':'AUS20','discount':'-20% OFF','site':{'zh':'澳洲站','en':'Australia','es':'Australia','pt':'Austrália','fr':'Australie','de':'Australien','ja':'豪州'}},
    {'flag':'🇯🇵','code':'JP800','discount':'¥800 OFF','site':{'zh':'日本站','en':'Japan','es':'Japón','pt':'Japão','fr':'Japon','de':'Japan','ja':'日本'}},
    {'flag':'🇫🇷','code':'PARIS15','discount':'-15% OFF','site':{'zh':'法国站','en':'France','es':'Francia','pt':'França','fr':'France','de':'Frankreich','ja':'フランス'}},
    {'flag':'🇩🇪','code':'DEALDE16','discount':'-16% OFF','site':{'zh':'德国站','en':'Germany','es':'Alemania','pt':'Alemanha','fr':'Allemagne','de':'Deutschland','ja':'ドイツ'}},
    {'flag':'🇧🇷','code':'BRMODA17','discount':'-17% OFF','site':{'zh':'巴西站','en':'Brazil','es':'Brasil','pt':'Brasil','fr':'Brésil','de':'Brasilien','ja':'ブラジル'}},
]

def section(lang, date_s):
    L=LANG[lang]; valid=add_days(date_s,30); cards=[]
    for p in rotate(PROMOS,date_s,5,1):
        site=p['site'].get(lang,p['site']['en'])
        cards.append(f'''    <div class="flex-none w-64 bg-white rounded-xl soft-shadow p-4 snap-start border border-outline-variant/20 flex items-center gap-4">
      <div class="w-12 h-12 bg-surface-variant rounded-full flex items-center justify-center text-xl shrink-0">{p['flag']}</div>
      <div>
        <p class="font-label-caps text-on-surface-variant mb-1">{esc(site)}</p>
        <p class="font-title-sm text-primary font-bold">{esc(p['discount'])}</p>
        <p class="text-xs text-outline mt-1 border border-dashed border-outline-variant px-2 py-0.5 rounded inline-block">{esc(p['code'])}</p>
        <button type="button" data-copy-code="{esc(p['code'])}" data-copy-label="{esc(L['copy'])}" data-copied-label="{esc(L['copied'])}" class="mt-2 text-xs font-bold text-primary hover:underline">{esc(L['copy'])}</button>
        <p class="text-[10px] text-outline mt-1">{esc(L['valid'])} {valid} · {esc(L['verified'])} {date_s} · {esc(L['checkout'])}</p>
      </div>
    </div>''')
    return f'''<section>
  <div class="flex items-center justify-between mb-6">
    <h2 class="font-headline-md text-on-surface">{esc(PROMO_TITLE[lang])}</h2>
    <a href="shopping-guide.html" class="text-primary text-sm font-semibold hover:underline flex items-center gap-1">{esc(L['view_all'])} <span class="material-symbols-outlined text-sm">arrow_forward</span></a>
  </div>
  <div class="flex gap-4 overflow-x-auto pb-4 snap-x hide-scrollbar">
{chr(10).join(cards)}
  </div>
</section>'''

def run(date_s):
    changed=False
    for lang,path in index_pages():
        s=read(path)
        if '<!-- Trending Promo Codes -->' not in s: continue
        s=replace_section(s,'Trending Promo Codes',section(lang,date_s))
        s=update_dates(s,date_s)
        changed |= write_if_changed(path,s)
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
