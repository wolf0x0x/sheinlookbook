#!/usr/bin/env python3
from __future__ import annotations
import argparse, importlib, subprocess
from common import ROOT, git_commit_all, today_from_args

TASKS = [
    ('seo_health', '[auto] SEO health {date}'),
    ('i18n_check', '[auto] i18n check {date}'),
    ('promo_sync', '[auto] promo sync {date}'),
    ('quality_radar_rotate', '[auto] quality radar rotate {date}'),
    ('style_rotation', '[auto] style rotation {date}'),
    ('top10_update', '[auto] top10 update {date}'),
    ('global_sites_verify', '[auto] global sites verify {date}'),
    ('sustainability_sync', '[auto] sustainability sync {date}'),
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date')
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    date_s = args.date or today_from_args([])
    committed = []
    for name, message in TASKS:
        mod = importlib.import_module(name)
        changed = mod.run(date_s)
        print(f'{name}: ' + ('changed' if changed else 'no-change'))
        if changed and args.commit and git_commit_all(message.format(date=date_s)):
            committed.append(name)
    if args.commit and committed:
        subprocess.run(['git','push','origin','HEAD:main'], cwd=ROOT, check=True)
    print('committed=' + ','.join(committed))

if __name__ == '__main__':
    main()
