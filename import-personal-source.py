"""Extract the requested factual skill fields from an Entertainment14 snapshot.

Usage: python import-personal-source.py source-entertainment14.html
Requires beautifulsoup4 for this optional import step; build.py remains stdlib-only.
"""
import json, pathlib, sys
from bs4 import BeautifulSoup

root=pathlib.Path(__file__).parent
source='https://www.entertainment14.net/blog/post/111011676-fire-emblem-%E8%90%AC%E7%B8%B7%E5%8D%83%E7%B5%B2-%E8%A7%92%E8%89%B2%E8%B3%87%E6%96%99%E6%95%B4%E7%90%86'
mapping='''Cai|凱伊
Dietrich|迪托利希
Theodora|賽奧朵拉
Leda|蕾達
Tialla|媞雅拉
Peter|皮特魯
Ultand|烏爾坦德
Fabio|法畢歐
Esmeralda|艾絲梅拉爾達
Mikaela|米迦艾拉
Bonaventure|波拿帕爾特
Tobias|托比亞斯
Lilian|莉利安
Lysander|萊桑達
Buccar|巴卡尼亞
Sirocco|西洛可
Olympia|奧琳琵婭
Mu|穆
Ursula|烏修拉
Diego|迪雅各
Sha Lan|沙蘭
Dante|丹提
Simon|希蒙
Ninae|妮涅
Nezha|哪吒
Guzran|古紮嵐
Nydine|努蒂奴
Io|伊歐
Catania|卡塔妮雅
Benditz|班迪茲
Alexandra|亞歷山卓
Noctula|諾克裘拉
Yang Jie|楊界
Sofia|索緋雅
Nuzzuo|努佐
Majide|馬吉迪
Zarcone|劄可捏
Goliath|哥萊亞斯
Jester|傑斯塔
Ludia|魯魯迪婭
Fianna|菲亞娜
Dadao|大刀
Halvin|哈爾溫
Seteth|西提司
Loretta|羅蕾塔
Kiroc|基羅伊卡
Inyoni|易尼奧尼
Peppe|佩佩'''
name_map=dict(line.split('|') for line in mapping.splitlines())
soup=BeautifulSoup(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'),'html.parser')
entry=soup.select_one('.entry-content')
assert entry is not None
sections={}
for heading in entry.find_all('h3'):
    table=heading.find_next_sibling('table')
    assert table is not None, heading.get_text(strip=True)
    fields={}
    for row in table.find_all('tr'):
        cells=row.find_all(['td','th'])
        if len(cells)==2:
            fields[cells[0].get_text(strip=True)]=cells[1].get_text(' ',strip=True)
    sections[heading.get_text(strip=True)]=fields

units=json.loads((root/'characters.json').read_text(encoding='utf-8'))
result={}
for unit in units:
    name=unit['name']; zh=name_map.get(name,''); fields=sections.get(zh)
    personal=fields.get('個人技能') if fields is not None else None
    status='documented' if personal and personal!='調查中' else 'investigating' if personal=='調查中' else 'omitted' if fields is not None else 'character_missing'
    crests=[dict(label=label,effect=fields[label]) for label in ['血印','血印2'] if fields and fields.get(label)]
    proficiencies=fields.get('擅長技能') if fields is not None else None
    result[name]=dict(zh=zh,personal=personal,personalStatus=status,crests=crests,crestStatus='documented' if crests else 'not_listed',proficiencies=proficiencies,source=source,checked='2026-09-18')
assert len(result)==50
assert sum(v['personalStatus']=='documented' for v in result.values())==44
assert sum(bool(v['crests']) for v in result.values())==10
(root/'personal-skills.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('50 records: 44 documented personal effects; 10 characters / 12 crest effects; 6 personal gaps labelled.')
