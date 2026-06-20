#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
LANGS = ["zh", "en", "es", "pt", "fr", "de", "ja"]

LANG = {
    "zh": {"copy":"复制","copied":"已复制","view_all":"查看全部","valid":"有效期至","verified":"最后验证","checkout":"结账页实时验证","updated":"最后更新","source":"数据来源：编辑样例、公开政策与页面交互记录，实时价格/库存以下单页为准。","details":"查看详情","scan":"最后检索时间"},
    "en": {"copy":"Copy","copied":"Copied","view_all":"View all","valid":"Valid until","verified":"Last verified","checkout":"Recheck at checkout","updated":"Last updated","source":"Sources: editorial samples, public policy pages, and on-page interaction logs. Recheck live price and stock at checkout.","details":"View Details","scan":"Last scanned"},
    "es": {"copy":"Copiar","copied":"Copiado","view_all":"Ver todo","valid":"Válido hasta","verified":"Última verificación","checkout":"Verificar al pagar","updated":"Última actualización","source":"Fuentes: muestras editoriales, páginas públicas de políticas y registros de interacción. Revisa precio y stock al pagar.","details":"Ver detalles","scan":"Última búsqueda"},
    "pt": {"copy":"Copiar","copied":"Copiado","view_all":"Ver tudo","valid":"Válido até","verified":"Última verificação","checkout":"Verifique no checkout","updated":"Última atualização","source":"Fontes: amostras editoriais, páginas públicas de políticas e registros de interação. Confira preço e estoque no checkout.","details":"Ver detalhes","scan":"Última busca"},
    "fr": {"copy":"Copier","copied":"Copié","view_all":"Tout voir","valid":"Valable jusqu'au","verified":"Dernière vérification","checkout":"À vérifier au paiement","updated":"Dernière mise à jour","source":"Sources : exemples éditoriaux, pages publiques de politique et interactions sur page. Vérifiez prix et stock au paiement.","details":"Voir détails","scan":"Dernière recherche"},
    "de": {"copy":"Kopieren","copied":"Kopiert","view_all":"Alle anzeigen","valid":"Gültig bis","verified":"Zuletzt geprüft","checkout":"Im Checkout prüfen","updated":"Zuletzt aktualisiert","source":"Quellen: redaktionelle Beispiele, öffentliche Richtlinienseiten und Seiteninteraktionen. Preis und Bestand im Checkout prüfen.","details":"Details ansehen","scan":"Zuletzt gesucht"},
    "ja": {"copy":"コピー","copied":"コピー済み","view_all":"すべて見る","valid":"有効期限","verified":"最終確認","checkout":"決済画面で再確認","updated":"最終更新","source":"出典：編集サンプル、公開ポリシーページ、ページ内操作ログ。価格と在庫は決済画面で再確認してください。","details":"詳細を見る","scan":"最終検索"},
}
PROMO_TITLE = {"zh":"热门优惠码","en":"Trending Promo Codes","es":"Códigos promo destacados","pt":"Códigos promocionais em destaque","fr":"Codes promo tendance","de":"Aktuelle Rabattcodes","ja":"注目プロモコード"}

def today_from_args(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--date')
    args, _ = parser.parse_known_args(argv)
    return args.date or os.environ.get('MAINTENANCE_DATE') or dt.date.today().isoformat()

def read(path):
    return Path(path).read_text(encoding='utf-8')

def write_if_changed(path, content):
    path = Path(path)
    old = path.read_text(encoding='utf-8') if path.exists() else None
    if old == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    return True

def index_pages():
    for lang in LANGS:
        yield lang, ROOT / lang / 'index.html'

def pages_named(name):
    for lang in LANGS:
        yield lang, ROOT / lang / name

def add_days(date_s, days):
    return (dt.date.fromisoformat(date_s) + dt.timedelta(days=days)).isoformat()

def rotate(items, date_s, count=None, salt=0):
    start = (dt.date.fromisoformat(date_s).toordinal() + salt) % len(items)
    out = items[start:] + items[:start]
    return out if count is None else out[:count]

def replace_section(text, comment, replacement):
    marker = f'<!-- {comment} -->'
    pattern = re.compile(re.escape(marker) + r'\s*<section>.*?</section>', re.S)
    new, n = pattern.subn(marker + '\n' + replacement.strip(), text, count=1)
    return new if n else text

def esc(value):
    return html.escape(str(value), quote=True)

def shein_url(name):
    return 'https://www.shein.com/pdsearch/' + quote(name) + '/'

def update_dates(text, date_s):
    pairs = ['最后更新','Last updated','Última actualización','Última atualização','Dernière mise à jour','Zuletzt aktualisiert','最終更新']
    for label in pairs:
        sep = '：' if label in ('最后更新','最終更新') else ':'
        text = re.sub(re.escape(label) + r'[：:]\s*\d{4}-\d{2}-\d{2}', f'{label}{sep}{date_s}', text)
    return text

def ensure_robots():
    return write_if_changed(ROOT/'robots.txt', 'User-agent: *\nAllow: /\nSitemap: https://sheinlookbook.xyz/sitemap.xml\n')

def update_sitemap(date_s):
    p = ROOT/'sitemap.xml'
    s = read(p)
    s = re.sub(r'<lastmod>\d{4}-\d{2}-\d{2}</lastmod>', f'<lastmod>{date_s}</lastmod>', s)
    return write_if_changed(p, s)

def git_commit_all(message):
    subprocess.run(['git','add','.'], cwd=ROOT, check=True)
    if subprocess.run(['git','diff','--cached','--quiet'], cwd=ROOT).returncode == 0:
        return False
    subprocess.run(['git','commit','-m',message], cwd=ROOT, check=True)
    return True
