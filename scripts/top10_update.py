#!/usr/bin/env python3
from __future__ import annotations
import re
from common import *
GOOD=[('DAZY 纯棉 T 恤','DAZY cotton tee','sw210324','4.9/5','100%棉'),('MOTF 真丝衬衫','MOTF silk blouse','swblouse','4.8/5','高级面料'),('SHEIN BASICS 直筒牛仔裤','SHEIN BASICS straight jeans','swdenim','4.8/5','版型稳定'),('LUNE 亚麻衬衫裙','LUNE linen shirt dress','swdress','4.7/5','透气'),('Glowmode 高腰瑜伽裤','Glowmode high-rise leggings','swactive','4.8/5','回弹好'),('Dazy 西装阔腿裤','Dazy tailored wide pants','swpants','4.7/5','垂坠感'),('MOTF 针织开衫','MOTF knit cardigan','swknit','4.7/5','不起球'),('SHEIN MOD 纯色衬衫','SHEIN MOD solid shirt','swshirt','4.6/5','不透'),('VCAY 度假罩衫','VCAY resort cover-up','swvacay','4.6/5','轻薄'),('SHEIN Clasi 西装外套','SHEIN Clasi blazer','swblazer','4.6/5','挺括'),('亚麻混纺阔腿裤','Linen blend wide pants','swlinen','4.6/5','清爽'),('高支棉基础衬衫','Premium cotton shirt','swcotton','4.7/5','耐洗')]
BAD=[('EZwear 罗纹针织衫','EZwear ribbed knit top','sw220912','偏透','过薄'),('VCAY 碎花连衣裙','VCAY floral dress','swdress','尺码偏小','版型偏小'),('PU 皮机车夹克','PU moto jacket','swjacket','异味','异味明显'),('白色罗纹背心','White ribbed tank','swtank','透肤','偏透'),('亮片迷你裙','Sequin mini skirt','swparty','扎皮肤','扎肤'),('低腰阔腿裤','Low-rise wide pants','swpants','腰松','腰围偏大'),('网纱打底衫','Mesh base layer','swmesh','易勾丝','易破'),('仿羊羔绒外套','Faux shearling coat','swcoat','掉毛','掉毛'),('松紧腰短裤','Elastic waist shorts','swshort','卷边','易变形'),('薄款针织裙','Thin knit dress','swknitdress','起球','易起球'),('透明感衬衫','Sheer blouse','swsheer','偏透','需打底'),('亮面 PU 短裤','Glossy PU shorts','swpu','闷热','不透气')]
def nm(r,lang): return r[0] if lang=='zh' else r[1]
def gli(r,i,lang):
    return f'<li class="flex items-center justify-between p-3 bg-white rounded-lg soft-shadow border border-outline-variant/20"><div class="flex items-center gap-3"><span class="font-bold text-tertiary">{i}</span><div><p class="text-xs font-bold">{esc(nm(r,lang))}</p><p class="text-xs text-on-surface-variant">{esc(r[2])} | {esc(r[3])}</p></div></div><span class="px-2 py-1 rounded bg-[#FFF0F5] text-primary text-xs font-bold">{esc(r[4])}</span></li>'
def bli(r,i,lang):
    return f'<li class="flex items-center justify-between p-3 bg-white rounded-lg soft-shadow border border-outline-variant/20"><div class="flex items-center gap-3"><span class="font-bold text-error">{i}</span><div><p class="text-xs font-bold">{esc(nm(r,lang))}</p><p class="text-xs text-on-surface-variant">{esc(r[2])} | {esc(r[3])}</p></div></div><span class="px-2 py-1 rounded bg-error-container text-on-error-container text-xs font-bold">{esc(r[4])}</span></li>'
def run(date_s):
    changed=False
    for lang,path in pages_named('size-quality.html'):
        s=read(path); pos=s.find('<!-- Quality Lists -->')
        if pos<0: continue
        good='<ul class="space-y-3">\n'+'\n'.join('            '+gli(r,i+1,lang) for i,r in enumerate(rotate(GOOD,date_s,10,5)))+'\n          </ul>'
        bad='<ul class="space-y-3">\n'+'\n'.join('            '+bli(r,i+1,lang) for i,r in enumerate(rotate(BAD,date_s,10,7)))+'\n          </ul>'
        head,tail=s[:pos],s[pos:]
        tail=re.sub(r'<ul class="space-y-3">.*?</ul>',good,tail,count=1,flags=re.S)
        tail=re.sub(r'<ul class="space-y-3">.*?</ul>',bad,tail,count=1,flags=re.S)
        changed |= write_if_changed(path,update_dates(head+tail,date_s))
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
