#!/usr/bin/env python3
from __future__ import annotations
import re
from common import *
OCC=[
('work','autumn','mid','elegant','workwear-blazer-photo.jpg',{'zh':'通勤','en':'Work','es':'Trabajo','pt':'Trabalho','fr':'Bureau','de':'Office','ja':'通勤'},[{'zh':'通勤轻熟风套装','en':'Chic Workwear Set','price':'$35.00','rating':'4.8'},{'zh':'奶油色西装马甲套装','en':'Cream vest suit set','price':'$39.90','rating':'4.7'}]),
('date','spring','mid','elegant','floral-midi-dress-photo.jpg',{'zh':'约会','en':'Date','es':'Cita','pt':'Encontro','fr':'Rendez-vous','de':'Date','ja':'デート'},[{'zh':'法式碎花连衣裙','en':'Floral Midi Dress','price':'$28.50','rating':'4.9'},{'zh':'方领茶歇碎花裙','en':'Square-neck tea dress','price':'$31.00','rating':'4.8'}]),
('vacation','summer','high','casual','linen-vacation-set-photo.jpg',{'zh':'度假','en':'Vacation','es':'Vacaciones','pt':'Férias','fr':'Vacances','de':'Urlaub','ja':'リゾート'},[{'zh':'海岛度假亚麻套装','en':'Linen Vacation Set','price':'$42.00','rating':'4.7'},{'zh':'海边罩衫短裤套装','en':'Beach cover-up short set','price':'$37.50','rating':'4.6'}]),
('sport','summer','mid','sport','yoga-set-photo.jpg',{'zh':'运动','en':'Sport','es':'Deporte','pt':'Esporte','fr':'Sport','de':'Sport','ja':'スポーツ'},[{'zh':'无缝高弹瑜伽套装','en':'Seamless Stretch Yoga Set','price':'$25.99','rating':'4.6'},{'zh':'奶茶色训练背心套装','en':'Mocha training set','price':'$29.00','rating':'4.7'}]),
('party','winter','high','elegant','party-sequin-dress-photo.jpg',{'zh':'派对','en':'Party','es':'Fiesta','pt':'Festa','fr':'Soirée','de':'Party','ja':'パーティー'},[{'zh':'亮片拼接西装裙','en':'Sequin Blazer Dress','price':'$48.50','rating':'4.9'},{'zh':'香槟色亮片长裙','en':'Champagne sequin maxi','price':'$52.00','rating':'4.8'}]),
('daily','spring','mid','casual','shirt-jeans-daily-photo.jpg',{'zh':'日常','en':'Daily','es':'Diario','pt':'Dia a dia','fr':'Quotidien','de':'Alltag','ja':'デイリー'},[{'zh':'纯棉宽松衬衫牛仔裤组合','en':'Cotton Shirt & Jeans Combo','price':'$32.00','rating':'4.5'},{'zh':'白衬衫直筒牛仔组合','en':'White shirt straight jeans combo','price':'$34.00','rating':'4.6'}])]
def card(o,item,lang):
    key,season,budget,style,img,label,_=o; name=item.get(lang,item['en']); lab=label.get(lang,label['en'])
    return f'''<article data-occasion="{key}" data-season="{season}" data-budget="{budget}" data-style="{style}" class="bg-white rounded-xl soft-shadow overflow-hidden group cursor-pointer border border-outline-variant/20 hover:border-primary/30 transition-colors">
  <div class="relative aspect-[3/4] overflow-hidden bg-surface-variant">
    <img src="/assets/images/{img}" alt="{esc(name)}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy"/>
    <div class="absolute top-2 left-2 bg-[#FFF0F5] text-primary px-2 py-1 rounded-lg text-xs font-bold">{esc(lab)}</div>
  </div>
  <div class="p-4"><h3 class="font-title-sm text-on-surface mb-2 truncate">{esc(name)}</h3><div class="flex justify-between items-center mb-3"><span class="font-bold text-primary">{esc(item['price'])}</span><div class="flex items-center gap-1 text-secondary-container text-sm"><span class="material-symbols-outlined text-sm">star</span><span>{esc(item['rating'])}</span></div></div><a href="{shein_url(name)}" target="_blank" rel="nofollow sponsored noopener" class="block text-center w-full py-2 border border-primary text-primary rounded-lg text-sm hover:bg-primary hover:text-white transition-colors">{esc(LANG[lang]['details'])}</a></div>
</article>'''
def run(date_s):
    changed=False; idx=0 if int(date_s[-2:])%2==0 else 1
    for lang,path in pages_named('style-by-occasion.html'):
        s=read(path); cards='\n\n'.join(card(o,o[6][idx],lang) for o in OCC)
        s2=re.sub(r'(<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">).*?(</div>\s*\n\s*<div class="mt-10 flex justify-center">)', r'\1\n\n'+cards+r'\n\n  \2', s, count=1, flags=re.S)
        changed |= write_if_changed(path,s2)
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
