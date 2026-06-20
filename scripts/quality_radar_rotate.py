#!/usr/bin/env python3
from __future__ import annotations
import re
from common import *
BAD=[('PU 皮机车夹克','PU moto jacket','异味明显','Strong odor'),('白色罗纹背心','White ribbed tank','偏透','See-through'),('亮片迷你裙','Sequin mini skirt','扎皮肤','Scratchy'),('网纱打底衫','Mesh base layer','易勾丝','Snags easily'),('低腰阔腿裤','Low-rise wide pants','腰围偏大','Loose waist')]
GOOD=[('无缝瑜伽裤','Seamless yoga leggings','柔软亲肤','Soft feel'),('宽松纯棉 T 恤','Loose cotton tee','面料厚实','Dense cotton'),('缎面吊带裙','Satin slip dress','垂坠感好','Good drape'),('亚麻衬衫裙','Linen shirt dress','透气','Breathable'),('高腰直筒牛仔裤','High-rise straight jeans','版型稳定','Stable fit')]
def row(item,lang,bad,last=False):
    name=item[0] if lang=='zh' else item[1]; tag=item[2] if lang=='zh' else item[3]
    border='' if last else ' pb-3 border-b border-surface-container-low'
    cls='text-error bg-error-container' if bad else 'text-tertiary-container bg-tertiary-fixed'
    return f'<li class="flex items-center justify-between{border}"><span class="text-sm text-on-surface-variant">{esc(name)}</span><span class="text-xs font-bold {cls} px-2 py-1 rounded">{esc(tag)}</span></li>'
def run(date_s):
    changed=False
    for lang,path in index_pages():
        s=read(path); pos=s.find('<!-- Quality Radar & Price Index -->')
        if pos<0: continue
        bad='<ul class="space-y-3">\n'+'\n'.join('          '+row(x,lang,True,i==2) for i,x in enumerate(rotate(BAD,date_s,3,2)))+'\n        </ul>'
        good='<ul class="space-y-3">\n'+'\n'.join('          '+row(x,lang,False,i==2) for i,x in enumerate(rotate(GOOD,date_s,3,4)))+'\n        </ul>'
        head,tail=s[:pos],s[pos:]
        tail=re.sub(r'<ul class="space-y-3">.*?</ul>',bad,tail,count=1,flags=re.S)
        tail=re.sub(r'<ul class="space-y-3">.*?</ul>',good,tail,count=1,flags=re.S)
        changed |= write_if_changed(path,update_dates(head+tail,date_s))
    return changed
if __name__=='__main__': print('changed='+str(run(today_from_args())).lower())
