"""Refresh the Chinese proficiency learnables snapshot from Redfreshet.

The generated JSON intentionally contains no Japanese display text.  Redfreshet
lists one row per character, so this script groups identical learnables and
keeps every confirmed owner.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
BASE = "https://redfreshet.com/game-tools/fe-banshisenko/proficiencies"

PROFICIENCIES = {
    "sword": "劍術",
    "lance": "槍術",
    "axe": "斧術",
    "bow": "弓術",
    "gauntlet": "格鬥術",
    "black_magic": "黑魔術",
    "white_magic": "白魔術",
    "command": "指揮術",
    "infantry": "步兵術",
    "riding": "馬術",
    "armor": "重裝術",
    "flying": "飛行術",
}

TYPE_ZH = {"スキル": "技能", "戦技": "戰技", "魔法": "魔法"}

NAME_ZH = {
    "クロスワイズ": "十字斬", "デストレッツァ": "德斯特雷扎", "両断": "兩斷",
    "剛撃": "剛擊", "剣術Lv.1": "劍術Lv.1", "影詰め": "影逼",
    "必閃の一撃": "必閃一擊", "燕返し": "燕返", "鎧通し": "穿甲", "霞切り": "霞斬",
    "守護旋風": "守護旋風", "守護突槍": "守護突槍", "旋風槍": "旋風槍",
    "槍術Lv.1": "槍術Lv.1", "槍術Lv.2": "槍術Lv.2", "流風槍": "流風槍",
    "烈風槍": "烈風槍", "突き押し": "突刺推擊", "金剛の一撃": "金剛一擊",
    "集中投擲+": "集中投擲+", "クラッシュ": "粉碎", "スパイク": "尖刺",
    "スマッシュ": "猛擊", "ハーフスパイク": "半尖刺", "レイジアップ": "狂怒提升",
    "斧術Lv.1": "斧術Lv.1", "斧術Lv.2": "斧術Lv.2", "見極めの一撃": "看破一擊",
    "囲いの矢": "包圍箭", "奇襲の矢": "奇襲箭", "弓術Lv.1": "弓術Lv.1",
    "弓術Lv.2": "弓術Lv.2", "影眩みの矢": "影眩箭", "急所射ち": "要害射擊",
    "曲射": "曲射", "警戒射撃": "警戒射擊", "離脱射撃": "脫離射擊",
    "バックブロー": "後退擊", "バトルラッシュ": "戰鬥連擊", "フェイント": "佯攻",
    "格闘術Lv.1": "格鬥術Lv.1", "格闘術Lv.2": "格鬥術Lv.2", "活殺一撃": "活殺一擊",
    "用心一撃": "謹慎一擊", "豪拳一撃": "豪拳一擊", "ウィンド": "風刃",
    "サンダー": "雷電", "スライムB": "史萊姆B", "ドーラΔ": "朵拉Δ",
    "ファイアー": "火焰", "ブリザー": "暴雪", "ボルガノン": "火山爆焰",
    "黒魔術Lv.1": "黑魔術Lv.1", "エマージス": "埃瑪吉斯", "エンジェル": "天使",
    "ライブ": "治療", "リザイア": "吸星術", "レスト": "復原", "白魔術Lv.1": "白魔術Lv.1",
    "入れ替え": "交換", "威嚇": "威嚇", "攻撃陣形": "攻擊陣形", "牽制": "牽制",
    "咄嗟の回避": "緊急迴避", "射撃安定": "射擊安定", "白兵の間合い": "近戰距離",
    "騎士の先陣": "騎士先鋒", "守備の構え": "守備架勢", "必殺守備": "必殺防禦",
    "防弓術": "防弓術", "防槍術": "防槍術", "風読み": "讀風",
}

EFFECT_ZH = {
    "戦闘後に技が2増える。累積上限は10で、マップ終了時に解除。": "戰鬥後技巧+2，累積上限10；地圖結束時解除。",
    "相手のHPが半分以下なら攻撃力が5、必殺が10増える。": "敵人HP低於一半時，攻擊力+5、必殺+10。",
    "必殺を重視した剣の戦技。": "重視必殺的劍戰技。", "命中を重視した剣の戦技。": "重視命中的劍戰技。",
    "剣装備時の命中が3増える。": "裝備劍時命中+3。", "相手が得る有利な地形の効果を無視する。": "無視敵人獲得的有利地形效果。",
    "攻撃時、技÷2%の確率で攻撃力が5増える。": "攻擊時，以技巧÷2%的機率使攻擊力+5。",
    "飛行に有効な剣の戦技。": "對飛行單位有效的劍戰技。", "重装に有効。": "對重裝單位有效。",
    "使用した戦闘で回避が10増える。": "使用該招的戰鬥中迴避+10。",
    "使用した戦闘で耐物が7増える。": "使用該招的戰鬥中物理耐性+7。", "使用した戦闘で防御力が3増える。": "使用該招的戰鬥中防禦力+3。",
    "命中を重視した槍の戦技。": "重視命中的槍戰技。", "槍装備時の命中が3増える。": "裝備槍時命中+3。",
    "槍を装備しているとき、命中が5増える。": "裝備槍時命中+5。", "必殺を重視した槍の戦技。": "重視必殺的槍戰技。",
    "威力を重視した槍の戦技。": "重視威力的槍戰技。", "敵撃破時に耐物が3増える。次の自分のフェイズまで有効。追撃はできない。": "擊破敵人時物理耐性+3，持續至下次己方行動階段；不能追擊。",
    "命中を重視した投擲。射程1〜2の槍が必要。": "重視命中的投擲技；需要射程1～2的槍。",
    "命中時、5%の確率で相手を混乱させる。追撃はできない。": "命中時有5%機率使敵人混亂；不能追擊。",
    "命中を重視した斧の戦技。": "重視命中的斧戰技。", "必殺を重視した斧の戦技。": "重視必殺的斧戰技。",
    "戦闘後に力が1増える。累積上限は5で、マップ終了時に解除。": "戰鬥後力量+1，累積上限5；地圖結束時解除。",
    "斧装備時の命中が3増える。": "裝備斧時命中+3。", "斧装備時の命中が5増える。": "裝備斧時命中+5。",
    "高い命中と引き換えにダメージが半分になる。": "提高命中，但造成的傷害減半。",
    "命中した敵の移動力を3下げる。次の自分のフェイズまで有効。": "命中後使敵人移動力-3，持續至下次己方行動階段。",
    "相手のHPが満タンなら、30%の確率で攻撃力が5増える。": "敵人滿HP時，有30%機率使攻擊力+5。",
    "弓装備時の命中が3増える。": "裝備弓時命中+3。", "弓を装備しているとき、命中が5増える。": "裝備弓時命中+5。",
    "必殺を重視した弓の戦技。": "重視必殺的弓戰技。", "命中を重視した弓の戦技。": "重視命中的弓戰技。",
    "戦闘後、1マスまで移動できる。": "戰鬥後可再移動最多1格。", "相手の攻撃より先に追撃する。": "在敵人攻擊前先發動追擊。",
    "戦闘後に相手の回避を20下げる。相手が1回戦闘すると解除。": "戰鬥後使敵人迴避-20；敵人進行一次戰鬥後解除。",
    "籠手装備時の命中が3増える。": "裝備拳套時命中+3。", "籠手を装備しているとき、命中が5増える。": "裝備拳套時命中+5。",
    "必殺を重視した格闘戦技。": "重視必殺的格鬥戰技。", "効果は未収録": "效果未收錄。", "命中を重視した格闘戦技。": "重視命中的格鬥戰技。",
    "風属性の初級攻撃魔法。飛行に有効。": "初級風屬性攻擊魔法；對飛行單位有效。", "雷属性の初級攻撃魔法。": "初級雷屬性攻擊魔法。",
    "疑似生命体による攻撃魔法。": "以擬似生命體攻擊的魔法。", "暗黒物質による攻撃魔法。": "以暗黑物質攻擊的魔法。",
    "炎属性の初級攻撃魔法。": "初級火屬性攻擊魔法。", "氷属性の初級攻撃魔法。": "初級冰屬性攻擊魔法。",
    "炎属性の上級攻撃魔法。": "高級火屬性攻擊魔法。", "黒魔法装備時の命中が3増える。": "裝備黑魔法時命中+3。",
    "味方の必避を30増やす。次の自分のフェイズまで有効。": "使友軍必殺迴避+30，持續至下次己方行動階段。",
    "冥魔に有効な神聖属性の攻撃魔法。": "對冥魔有效的神聖屬性攻擊魔法。", "味方のHPを回復する。": "恢復友軍HP。",
    "与ダメージの半分だけHPを回復する攻撃魔法。": "攻擊魔法，恢復相當於造成傷害一半的HP。", "味方の状態異常を解除する。": "解除友軍的異常狀態。",
    "白魔法装備時の命中が3増える。": "裝備白魔法時命中+3。", "歩兵時、隣接した味方と位置を交換する。大型ユニットには使用できない。": "步兵時與相鄰友軍交換位置；不能對大型單位使用。",
    "隣接した敵の必殺を5下げる。": "相鄰敵人的必殺-5。", "隣接した味方の攻撃力を1増やす。": "相鄰友軍的攻擊力+1。",
    "隣接した敵の回避を3下げる。": "相鄰敵人的迴避-3。", "歩兵で攻撃を受ける際、3%の確率で回避が100増える。": "步兵受到攻擊時，有3%機率使迴避+100。",
    "歩兵で弓または魔法を装備すると、命中が5増える。": "步兵裝備弓或魔法時命中+5。", "歩兵時、隣接する敵の移動力を1下げる。": "步兵時，使相鄰敵人的移動力-1。",
    "騎兵で先攻すると防御力が2増える。": "騎兵主動攻擊時防禦力+2。", "歩兵時、自分の守備が3増え、回避が10下がる。次の自分のフェイズまで有効。": "步兵時自身防禦+3、迴避-10，持續至下次己方行動階段。",
    "必殺を受ける際、30%の確率で被ダメージを半分にする。": "受到必殺時，有30%機率使傷害減半。", "重装時、弓の相手に対する防御力が5増える。": "重裝時，面對弓敵人的防禦力+5。",
    "重装時、槍を使う相手に対する防御力が5増える。": "重裝時，面對槍敵人的防禦力+5。", "弓の相手に対する回避が10増える。": "面對使用弓的敵人時迴避+10。",
}


def clean_name(text: str) -> str:
    return text.replace(" 育成目標にする", "").strip()


def main() -> None:
    characters = json.loads((ROOT / "redfreshet-characters.json").read_text(encoding="utf-8"))["characters"]
    owner_zh = {row["display_name_ja"]: row["display_name_zh"] for row in characters}
    rows: dict[tuple[str, str, str, str, str], dict] = {}

    for slug, proficiency in PROFICIENCIES.items():
        page_url = f"{BASE}/{slug}/"
        response = requests.get(page_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.select("table")[-1]
        for tr in table.select("tr")[1:]:
            cells = tr.select("th,td")
            if len(cells) < 6:
                continue
            name_ja, type_ja, owner_ja, _, condition_ja, effect_ja = [clean_name(cell.get_text(" ", strip=True)) for cell in cells[:6]]
            name = NAME_ZH[name_ja]
            effect = EFFECT_ZH[effect_ja]
            rank_match = re.search(r"(?:[A-Z]\+?)$", condition_ja)
            requirement = rank_match.group(0) if rank_match else "來源未列等級"
            item_link = cells[0].find("a", href=True)
            item_url = item_link["href"] if item_link else page_url
            if item_url.startswith("/"):
                item_url = "https://redfreshet.com" + item_url
            key = (proficiency, TYPE_ZH[type_ja], requirement, name, effect)
            row = rows.setdefault(key, {
                "proficiency": proficiency,
                "type": TYPE_ZH[type_ja],
                "level": requirement,
                "name": name,
                "effect": effect,
                "owners": [],
                "url": item_url,
                "source_url": page_url,
            })
            owner = owner_zh.get(owner_ja)
            if owner is None:
                raise KeyError(f"Missing Chinese owner name: {owner_ja}")
            if owner not in row["owners"]:
                row["owners"].append(owner)

    prof_order = list(PROFICIENCIES.values())
    type_order = {"技能": 0, "戰技": 1, "魔法": 2}
    rank_order = {"E": 0, "E+": 1, "D": 2, "D+": 3, "C": 4, "C+": 5, "B": 6, "B+": 7, "A": 8, "A+": 9, "S": 10, "來源未列等級": 99}
    output = sorted(rows.values(), key=lambda x: (prof_order.index(x["proficiency"]), rank_order.get(x["level"], 99), type_order[x["type"]], x["name"]))
    (ROOT / "redfreshet-proficiencies.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(output)} grouped proficiency learnables")


if __name__ == "__main__":
    main()
