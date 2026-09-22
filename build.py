import json, pathlib, base64, re
root=pathlib.Path(__file__).parent
# name | tier | strengths/proficiencies | limitation | advanced target | page id
raw='''Cai|Lord|劍、槍、白魔法；力量／技巧／速度均45%，個人技移動+1|來源未列弱點；騎術仍須另練|Bardinger|620167
Dietrich|Lord|劍、步兵；速度50%、技巧60%、幸運50%，先手必殺+5|來源未列弱點；迴避仍非必定免傷|Shido|620168
Theodora|Lord|槍、指揮；HP70%、防禦40%，30%機率減半傷害|減傷需機率觸發，不能作必定生存保證|Bardinger|620411
Leda|Lord|弓；速度65%，個人技可封鎖反擊|來源未列弱點；封反擊條件應以遊戲說明為準|Sniper|620437
Esmeralda|S|槍、斧、重甲；HP55%、防禦45%，減輕武器及配件重量|來源未列弱點；重甲路線需留意法術敵人（編者提醒）|Dreadnought|624005
Fianna|S|白／黑魔法；魔力55%、魔防45%，治療有機率不耗次數|節省次數屬機率效果，仍需管理法術資源|Bishop|623995
Bonaventure|A|黑魔法；魔力45%、技巧50%、速度40%，鄰接盟友技巧增益|來源未列專屬弱點；增益依賴站位|Ovate|623614
Peter|A|弓、步兵；技巧60%，弓戰技射程增益|射程優勢指弓戰技，勿當所有普通攻擊加射程|Sniper|624004
Lilian|A|弓、步兵；技巧55%，攻擊不能反擊的敵人時命中增益|個人技依賴敵人無法反擊|Sniper|624009
Mu|A|拳、劍、斧；個人技強化成長，多項物理能力均衡|來源未列弱點；需投入等級才能兌現成長優勢|Warrior|624010
Diego|A|劍；速度45%、技巧60%，可阻止鄰接盟友被追擊|保護效果依賴鄰接站位|Shido|624016
Dante|A|黑魔法；魔力45%、幸運45%，附近盟友迴避增益|支援效果依賴隊伍站位|Ovate|624018
Ninae|A|白魔法；魔防45%，對魔法敵人時命中及迴避增益|魔力35%；個人技限對魔法使用者|Bishop|623990
Nezha|A|劍、步兵；速度45%、技巧50%，先手攻擊+3|個人技加攻限先手|Shido|623977
Io|A|騎術、槍、斧；技巧45%，先手可提高防禦及迴避|速度35%；增益限先手|Bardinger|623980
Catania|A|劍；速度55%、技巧50%、幸運40%|個人技命中增益需要攻速比敵人高至少3|Shido|623981
Alexandra|A|劍；速度55%、技巧45%、幸運50%，鄰接盟友時命中／迴避增益|個人技依賴鄰接盟友|Shido|623983
Goliath|A|斧、重甲；HP55%、防禦50%，個人技提高體格|不可使用騎乘或飛行職業|Dreadnought|623976
Ludia|A|劍、步兵；速度55%、技巧45%，先手攻速+3|個人技攻速加成限先手|Shido|623992
Seteth|A|槍、斧、指揮；速度40%、技巧45%，敵方階段首次交戰可先攻|先攻效果不是整個敵方階段持續生效|Dragoon|623993
Halvin|A|弓、騎術；技巧60%、速度45%，交戰後命中可累積至地圖結束|命中增益需要先有交戰累積|Forest Knight|623997
Ursula|B|劍、弓；幸運40%、魅力45%，可對2格內盟友使用庫存道具|魔力35%，不擅白魔法；道具技不直接增傷／治療量|Sniper|624015
Peppe|B|弓、步兵；速度60%，敵方階段有機會先行|力量35%，追擊未必有足夠傷害；先行不穩定|Sniper|624000
Dadao|B|斧、重甲；HP50%、防禦45%，雙方均不能追擊時加攻|遇快速敵人時個人技失效；坦度成長不及頂級坦克|Dreadnought|623998
Loretta|B|劍；速度55%，HP高於一半時迴避增益|技巧40%、幸運30%；血量跌至一半以下失去增益|Shido|623996
Kiroc|B|弓；力量40%、技巧50%、速度55%，對異常狀態敵人增攻及命中|僅弓專長；依賴隊友施加異常狀態|Sniper|623994
Jester|B|弓、步兵；速度60%，使用Swap後防禦增加|力量35%；個人技不能補足輸出|Sniper|623991
Nuzzuo|B|弓；力量50%、技巧45%、速度55%，特效傷害時增攻|個人技只對能造成特效傷害的目標生效|Sniper|623987
Sofia|B|白魔法；魔力45%、魔防40%，個人技增加治療量|魔防／幸運遜於其他魔法坦克；技能不增傷或生存|Bishop|623986
Nydine|B|斧、騎術、飛行；力量40%、技巧40%、速度45%，騎乘可穿過敵方格|Game8推Bardinger但缺劍／槍專長；需要額外培養|Dragoon*|623979
Guzran|B|劍、拳、步兵；速度50%、技巧45%、幸運45%|個人技隨機選命中／迴避／必殺+10，不能依賴指定增益|Shido|623978
Simon|B|劍、斧、步兵；力量50%，可機率保留1HP免於致命傷|速度35%；保命依幸運觸發，不可靠|Warrior|624019
Sha Lan|B|槍、白魔法、指揮；魔力45%、魔防45%|需先使用Draw Back才能觸發個人技支援魔法效果|Bishop|624017
Tialla|B|黑／白魔法、指揮；魔力45%、幸運50%、魅力45%，對盟友戰技射程+1|射程效果非直接提高治療量，普通治療不等同盟友戰技|Bishop|623941
Gaitz|B|槍、斧、騎術；HP50%、防禦45%，鄰接盟友防禦+3|缺重甲專長；個人技不增加自身防禦|Bardinger*|624014
Lysander|B|槍、斧、騎術；速度50%，先手迴避+15|力量40%、技巧35%；個人技不補命中及火力|Bardinger|624002
Mikaela|B|斧、弓、步兵；力量45%，近接命中+10|技巧35%；遠距弓攻無法享受近接命中加成|Warrior|624008
Ultand|B|槍、白魔法；魔力40%、魔防45%，戰後為鄰接盟友少量回血|治療量較低，戰後回血範圍小且依賴站位|Bishop|624007
Sirocco|B|劍、黑／白魔法；魔力40%、技巧50%、速度45%，戰後回5HP|魔力較專門輸出法師低；回血不提高火力|Ovate|624006
Tobias|B|斧、騎術；力量60%，戰技攻擊+3|技巧30%、速度25%，命中及追擊差；普通攻擊不享戰技增攻|Warrior|623758
Buccar|B|槍、斧；HP50%、防禦45%，有受擊減傷個人技|重甲需補練；來源同段寫90%與10%減傷互相矛盾，幅度未核實|Dreadnought*|624003
Fabio|B|黑魔法、指揮；魔力50%，鄰接敵人迴避-5|技巧40%、速度35%；削迴避只限鄰接，不增加魔攻|Ovate*|623964
Olympia|C|斧、白魔法；魔力65%，持魔法時必殺增益|技巧35%、速度35%；缺黑魔法專長，魔力高不等於黑魔法成型快|Bishop*|624011
Benditz|C|弓、騎術；技巧50%，戰車職業個人技命中+20|力量35%、速度35%；轉Forest Knight後戰車個人技不再生效|Forest Knight|623982
Noctula|C|斧、拳；易培養物理戰士|力量45%、技巧40%、速度45%不突出；戰後迴避+3不增輸出|Warrior|623984
Yang Jie|C|斧、白魔法；可擔任治療|魔力／魔防／幸運均40%；擊殺後才觸發治療個人技，穩定性低|Bishop*|623985
Majide|C|力量50%，斧個人技力量+3|技巧30%、速度20%；加力量不能補命中及追擊缺陷|Warrior*|623988
Zarcone|C|斧；技巧60%，個人技命中+10，可疊Warrior斧命中+5|力量30%、速度35%、HP40%、防禦30%；易命中但輸出及坦度弱|Warrior|623989
Jasmine|C|槍、斧、重甲；反擊命中+20|力量40%、HP50%、防禦45%不突出；反擊命中不增傷及防禦|Dreadnought*|623999
Inyoni|C|斧、弓；力量50%，弓攻擊威力增益|技巧40%、速度35%；個人技不補命中及速度|Sniper|624001'''
routes=[
'''初始:Cai,Tialla,Peter;Ch6:Ultand;自動:Guzran;R3S2:Yang Jie;R4S1:Noctula;R5S3:Mikaela;R5S2:Majide;R6S3:Seteth,Ninae,Nezha;R6S1:Nydine;R6S2:Nuzzuo;R7S3:Goliath,Esmeralda,Loretta,Dadao;R7S2:Alexandra;R8S2:Lilian;R8S3:Lysander,Simon,Fianna,Olympia,Zarcone,Inyoni,Kiroc;R8S1:Jasmine;R9S3:Ludia,Sirocco,Mu,Halvin,Sofia,Benditz;R9S1:Peppe;R10S3:Jester,Dante,Diego,Ursula,Io,Catania''',
'''初始:Dietrich,Fabio,Esmeralda,Mikaela;自動:Yang Jie;R3S2:Io;R4S1:Kiroc;R5S3:Ultand;R5S2:Nydine;R6S3:Jester,Goliath,Lysander,Olympia;R6S1:Noctula;R7S3:Ursula,Simon,Fianna,Mu,Zarcone;R7S2:Benditz;R8S3:Peter,Ninae,Buccar,Guzran,Majide,Peppe,Inyoni,Alexandra;R8S2:Dante,Lilian;R8S1:Catania;R9S3:Tialla,Diego,Loretta,Ludia,Sirocco,Halvin,Sofia,Jasmine;R9S1:Nuzzuo;R10S3:Gaitz,Nezha,Sha Lan,Dadao''',
'''初始:Theodora,Bonaventure,Tobias,Lysander,Lilian;自動:Sofia;R3S1:Noctula;R4S1:Zarcone;R5S3:Loretta,Nydine;R5S1:Sirocco;R5S2:Dadao;R6S3:Ultand,Dante,Seteth,Ninae;R6S2:Nezha;R6S1:Nuzzuo,Alexandra;R7S3:Peter,Ludia,Simon,Halvin,Catania;R7S2:Peppe;R8S3:Mikaela,Buccar,Guzran,Majide,Jasmine;R8S2:Diego;R8S1:Benditz;R9S3:Jester,Goliath,Esmeralda,Ursula,Fianna,Olympia,Mu,Yang Jie;R9S1:Inyoni;R10S3:Tialla,Io,Kiroc''',
'''初始:Leda,Buccar,Sirocco,Mu,Olympia;自動:Catania;R3S1:Guzran;R4S2:Jasmine;R4S1:Kiroc;R5S3:Loretta,Fianna;R5S2:Dadao,Zarcone;R6S3:Esmeralda,Mikaela,Ninae,Simon;R6S1:Io;R7S2:Lilian;R7S3:Lysander,Ludia,Halvin,Sofia,Benditz;R7S1:Inyoni;R8S3:Tialla,Ultand,Diego,Sha Lan,Yang Jie,Noctula;R9S3:Fabio,Nezha,Nuzzuo,Majide;R10S3:Peter,Jester,Goliath,Dante,Seteth,Nydine,Alexandra''']
maps=[]
for route in routes:
    m={}
    for group in route.split(';'):
        req,names=group.split(':')
        for name in names.split(','): m[name]=req
    maps.append(m)
data=[]
for line in raw.splitlines():
    n,t,s,w,c,p=line.split('|'); data.append(dict(name=n,tier=t,strong=s,weak=w,target=c,routes=[m.get(n,'N/A') for m in maps],url='https://game8.co/games/Fire-Emblem-Fortunes-Weave/archives/'+p))
assert len(data)==50 and len(set(d['name'] for d in data))==50
assert [len(m) for m in maps]==[41,44,44,42]
avatars=json.loads((root/'avatar-positions.json').read_text(encoding='utf-8'))
assert set(avatars)=={u['name'] for u in data}
for unit in data:
    unit['avatar']=avatars[unit['name']]
personal=json.loads((root/'personal-skills.json').read_text(encoding='utf-8'))
assert set(personal)=={u['name'] for u in data}
for unit in data:
    unit['personalInfo']=personal[unit['name']]
# Align older tier-page summaries with the newly requested skill-effect source.
corrections={
    'Cai': ('strong','劍、槍、騎術、白魔法；力量／技巧／速度均45%，個人技移動+1'),
    'Leda': ('strong','弓；速度65%，主動交戰時5%機率封鎖反擊'),
    'Fabio': ('strong','黑魔法、指揮；魔力50%，鄰接敵人必殺迴避-5（非普通迴避）'),
    'Dante': ('strong','黑魔法；魔力45%、幸運45%，周圍2格盟友交戰時可機率提高必殺迴避'),
    'Nezha': ('strong','劍、步兵；速度45%、技巧50%，主動攻擊時50%機率攻擊力+3'),
    'Io': ('strong','騎術、槍、斧；技巧45%，騎兵主動交戰時防禦力+3、必殺迴避+30'),
    'Seteth': ('strong','槍、斧、指揮；速度40%、技巧45%，敌方階段首次交戰50%機率先攻'),
    'Buccar': ('strong','槍、斧；HP50%、防禦45%，受擊傷害降至90%（即減傷10%，依Entertainment14）'),
    'Kiroc': ('strong','弓；力量40%、技巧50%、速度55%，對異常狀態敵人攻擊力+3、必殺+10'),
    'Loretta': ('strong','劍；速度55%，HP不低於一半時迴避+10（含恰好一半）'),
    'Peppe': ('strong','弓、步兵；速度60%，敵方階段對已受傷敵人30%機率先攻'),
}
for unit in data:
    if unit['name'] in corrections:
        field,value=corrections[unit['name']]; unit[field]=value.replace('敌','敵')
    if unit['name']=='Cai': unit['weak']='來源未列弱點；騎術亦為新來源列出的專長，仍需升至考試門檻'
    if unit['name']=='Fabio': unit['weak']='技巧40%、速度35%；個人技只削鄰接敵人的必殺迴避，不直接補普通命中或魔攻'
    if unit['name']=='Dante': unit['weak']='個人技依賴2格範圍及盟友魅力÷2%的機率，增益為必殺迴避，並非普通迴避'
    if unit['name']=='Io': unit['weak']='速度35%；個人技限騎兵主動交戰，必殺迴避不同於普通迴避'
    if unit['name']=='Buccar': unit['weak']='Game8减傷敘述矛盾；本頁個人技能按新來源記為傷害×90%。重甲專長亦存在來源差異，考試前核對'.replace('减','減')
    if unit['name']=='Loretta': unit['weak']='技巧40%、幸運30%；HP低於一半才失去個人技增益'
    if unit['name']=='Kiroc': unit['weak']='僅弓專長；個人技依賴異常狀態，增益為必殺而非命中'
for unit in data:
    unit['combatNotes']=unit.pop('weak').replace('來源未列專屬弱點；','').replace('來源未列弱點；','')
    unit['proficiencies']=unit['personalInfo'].get('proficiencies')
    # The requested source lists strengths only. Missing strengths are not weaknesses.
    unit['weakSkills']=None
    unit['weakSkillsStatus']='not_provided'

def _records(payload, collection):
    """Accept a list, a wrapped collection, or an English-name keyed object."""
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    wrapped=payload.get(collection)
    if isinstance(wrapped, list):
        return wrapped
    if isinstance(wrapped, dict):
        return [dict(v, name=v.get('name') or k) for k,v in wrapped.items() if isinstance(v,dict)]
    metadata_keys={'metadata','field_guide','missing_report','source_index_url','retrieved_at','record_count','field_notes','missing_data_summary'}
    return [dict(v, name=v.get('name') or k) for k,v in payload.items() if k not in metadata_keys and isinstance(v,dict)]

def _key(value):
    return re.sub(r'[^a-z0-9]','',str(value or '').lower())

def _char_condition_zh(value):
    text=str(value or '')
    exact={
        '条件：第1部時タリムーン外伝完了，及，ストーリー時加入。':'條件：第1部完成塔利穆恩外傳，並於劇情中加入。',
        '条件：「セントリオンから的救援要請」完了，，帝都時本人於話，かけ。':'條件：完成「森特里昂的救援請求」後，在帝都與本人對話。',
        '条件：第1部時「亡き妹的装身具」完了，，第2部2章時キリーク倒す。':'條件：第1部完成「亡妹的飾品」，並在第2部第2章擊敗基里克。',
        '条件：増援的ネイサンキリーク時擊破。他的キャラ時倒す及加入，ない。':'條件：增援出現時由內森或基里克擊破；若由其他角色擊倒則不會加入。',
    }
    if text in exact: return exact[text]
    replacements={
        '条件：':'條件：','支拂う':'支付','支拂いあり':'需要支付','完了':'完成','交渉難易度':'交涉難度',
        '受注後':'接受委託後','入手':'取得','渡す':'交付','外伝':'外傳','ストーリー':'劇情',
        'クリア':'通關','スカウト':'招募','すべて':'全部','選ぶ':'選擇','賴み':'委託',
        'キャラ':'角色','話，かけ':'對話','倒す及加入，ない':'擊倒則不會加入','写，':'拓本',
    }
    for old,new in sorted(replacements.items(),key=lambda x:len(x[0]),reverse=True): text=text.replace(old,new)
    return text.replace('，，','，').replace('，。','。')

def _display_zh(value):
    """Clean machine-translated display text; raw Japanese remains in source fields only."""
    text=str(value or '')
    replacements={
        '鋭く小さな短劍':'鋒利小短劍','馬的お手入れ道具':'馬匹保養工具','儀礼用的鋭い槍':'儀式用鋒利長槍',
        '若い戈修':'年輕戈修','達古札ヒゲシバ':'達古札鬍鬚草','髭飾り':'鬍鬚飾品',
        '若い索修':'年輕索修','鋭い釣り針':'鋒利釣鉤',
        '白兵的間合い':'近戰距離掌控','泰夫入り焼き菓子':'泰夫夾心烤點心','少，甘い焼き菓子':'微甜烤點心',
        '素朴な焼き菓子':'樸素烤點心','香ば，い焼き菓子':'香酥烤點心','銀吉入り塞爾維':'銀吉風味塞爾維',
        '盾たち的肖像画':'眾盾衛的肖像畫','ユ・ファス的肖像':'柳華秀肖像','オーガス的泰夫':'奧加斯的泰夫',
        '派手すぎ腕輪':'華麗手鐲','闇討ち':'暗襲','槍投げ的達人':'投槍達人','，なやかな釣り竿':'柔韌釣竿',
        '魚的内臓的塩漬け':'鹽漬魚內臟','蜂蜜入り焼き菓子':'蜂蜜烤點心','ダンテ戯曲全集':'丹提戲曲全集',
        'フォドラ的紅茶':'芙朵拉紅茶','入れ知恵':'獻策','海的向こう的古書':'海外古書','狙い射ち':'精準射擊',
        '陣取り':'佔據陣地','薄い塞爾維':'清淡塞爾維','珍，い香辛料':'稀有香辛料','東方的耳飾り':'東方耳飾',
        'ジャーメル的乳':'賈梅爾乳','濃い塞爾維':'濃郁塞爾維','精霊的導き':'精靈引導','淡い色的画材':'淡色畫材',
        '村的素朴な料理集':'鄉村料理集','俺止まらねぇ':'勢不可擋','野菜的鉢植え':'蔬菜盆栽','風讀み':'讀風',
        'よく切れ彫刻刀':'鋒利雕刻刀','抑えつけ':'壓制','刺激的な戈修':'刺激風味戈修','素朴な戈修':'樸素戈修',
        '見切り':'看破','足止め':'阻滯','ニーザ産加爾姆':'尼薩產加爾姆','野菜的酢漬け':'醃漬蔬菜',
        '高級八卦占い道具':'高級八卦占卜工具','サラミス的菓子':'薩拉米斯點心','實用的な裁縫道具':'實用裁縫工具',
        '狩人的待ち伏せ':'獵人伏擊','ヤク的乳':'犛牛乳','蜂蜜入り的乳':'蜂蜜乳','風裂き的矢羽根':'裂風箭羽',
        '芳醇な索修':'芳醇索修','死於そびれ':'九死一生','致命避け':'致命迴避','引き留め役':'阻留者',
        '軽妙な索修':'輕快索修','無事的祈り':'平安祈禱','風任せ':'隨風','負けず嫌い':'不服輸',
        '情動的リザイア':'情動吸星術','リザイア':'吸星術','戰車乘り':'戰車騎手','暴れ斧':'狂斧',
        '恐れ知らず':'無所畏懼','強弓使い':'強弓手','美，い飾り矢':'美麗裝飾箭',
        '守護騎士的努め':'守護騎士的職責','弓姫':'弓姬','獣的衝動':'獸之衝動','歴戰的強者':'歷戰強者',
        '絶好調':'絕佳狀態','絶對防禦':'絕對防禦','闇的秘術':'暗之秘術','銀的精神':'白銀精神',
        '精霊的盤上遊戯':'精靈桌上遊戲','東方的盤上遊戯':'東方桌上遊戲','闘技場物語的写本':'鬥技場故事抄本',
        '軍略書的写本':'軍略書抄本','南方的薫泰夫':'南方芳香泰夫','南洋冒険奇譚':'南洋冒險奇譚',
        '子猫的置物':'小貓擺件','巨大魚的目玉':'巨魚眼珠','旅的老師的口伝録':'旅居老師口述錄',
        '東方恋愛見聞録':'東方戀愛見聞錄','莫爾菲斯歳時記':'莫爾菲斯歲時記','薬草料理大全':'藥草料理大全',
        '鍛錬用的装飾腕輪':'鍛鍊用裝飾手鐲','飛馬的風景画':'飛馬風景畫','熟成干，塞爾維':'熟成乾塞爾維',
        '秘伝的戈修':'秘傳戈修','世界的名詩集':'世界名詩集','火的山的戈修':'火山戈修',
        '大粒的泰夫':'大粒泰夫','小粒的泰夫':'小粒泰夫','東方的漆黑絹':'東方漆黑絹',
        '格闘術':'格鬥術','精霊':'精靈',
        '冒険王的英運':'冒險王的英運','冷静沈着':'冷靜沉著','先的先':'先發制人','後的先':'後發先至',
        '容赦無，':'毫不留情','怒涛':'怒濤','愛馬與連携':'愛馬協同','成長的兆，':'成長徵兆',
        '氣分上々':'興致高昂','氣分屋':'善變','疾駆':'疾馳','身躱，':'閃身','返礼':'回禮','風友軍於':'與風同行',
        '猪突猛進':'豬突猛進','白銀的乙女':'白銀少女','用心棒':'護衛','助太刀':'援護',
        '咄嗟的迴避':'應急迴避','補足説明':'補充說明','活發':'活潑','本氣的一發':'全力一擊',
        '好機':'良機','心的余裕':'從容心境','騎士的先陣':'騎士先鋒','騎士的感覺':'騎士直覺',
        'カイ篇':'凱伊篇','ディートリヒ篇':'迪托利希篇','セオドラ篇':'賽奧朵拉篇','レダ篇':'蕾達篇',
        'ディートリヒ':'迪托利希','レダ':'蕾達',
        'セントリオンから的救援要請':'森特里昂的救援請求','森特里昂から的救援要請':'森特里昂的救援請求',
        'エスメラルダ':'艾絲梅拉爾達','ダマセン':'達馬森','ピーテル':'彼得','アイギーナ':'艾吉娜',
        'グルマオサ':'古爾馬歐薩','オルヘル':'奧爾赫爾','カガヤキウオ':'輝光魚','ルルディヤー':'露露迪亞',
        'セテス':'塞特斯','デーツ':'椰棗','タリムーン':'塔利穆恩','ベルトラン':'貝特朗','コーシャルーガー':'科夏爾魯加',
        'ジェスター':'傑斯特','シロッコ':'西洛可','ウルタンド':'烏爾坦德','コロイオス':'科羅伊奧斯',
        'オリンピア':'奧林匹亞','コイントス':'擲硬幣','アナトリア':'安納托利亞','サラミス':'薩拉米斯',
        'ダ・ミナ':'達米娜','ネイサン':'內森','キリーク':'基里克','セントリオン':'森特里昂',
        '交渉的質問全部「い」':'交涉時所有問題皆選「是」','提示斷り':'提示全部拒絕',
        '全部的条件':'全部條件','条件':'條件','から出現':'起出現','満た，て':'符合後','交渉':'交涉',
        '贈り物':'禮物','増援':'增援','主人公':'主角','加入，ない':'不會加入','倒す':'擊敗',
        '亡き妹的装身具':'亡妹的飾品','わかった':'明白了','必要だ':'有必要','ど的選択肢時也よい':'任何選項皆可',
        '写，':'拓本','満月':'滿月','お手入れ':'保養','鋭い':'鋒利','素朴な':'樸素','刺激的な':'刺激風味',
        '速さ':'速度','守備':'防禦',
    }
    for old,new in sorted(replacements.items(),key=lambda x:len(x[0]),reverse=True): text=text.replace(old,new)
    text=text.replace('，，','，').replace('，。','。')
    return text.translate(str.maketrans('体気戦剣歩黒軽撃応発学変対辺処帰伝絶歴姫獣霊写薫険猫歳薬錬画恋闘装広図会国実済旧児号竜鉄専権将',
                                        '體氣戰劍步黑輕擊應發學變對邊處歸傳絕歷姬獸靈寫薰險貓歲藥鍊畫戀鬥裝廣圖會國實濟舊兒號龍鐵專權將'))

def _clean_display_tree(value):
    if isinstance(value,str): return _display_zh(value)
    if isinstance(value,list): return [_clean_display_tree(x) for x in value]
    if isinstance(value,dict): return {k:_clean_display_tree(v) for k,v in value.items()}
    return value

# Optional Redfreshet character details are merged without replacing route/tier/editorial data.
# Preferred schema is {"characters": [{"name": "Cai", ...}]}; an object keyed by
# English character name is also supported. `id`/slug is used when it is an English name.
character_source=root/'redfreshet-characters.json'
if character_source.exists():
    prof_zh={'剣術':'劍術','槍術':'槍術','斧術':'斧術','弓術':'弓術','格闘術':'格鬥術','白魔術':'白魔術','黒魔術':'黑魔術','指揮術':'指揮術','歩兵術':'步兵術','馬術':'馬術','重装術':'重裝術','飛行術':'飛行術'}
    red_payload=json.loads(character_source.read_text(encoding='utf-8'))
    red_records=_records(red_payload,'characters')
    for rec in red_records:
        if rec.get('quick_zh'): rec['quick_zh']=_clean_display_tree(rec['quick_zh'])
        quick=rec.get('quick_zh') or {}
        if quick.get('aptitude_tendency'):
            stat_map={'力':'力量','技':'技巧','魔防':'魔法防禦'}
            quick['aptitude_tendency']='・'.join(stat_map.get(x,x) for x in quick['aptitude_tendency'].split('・'))
        for row in rec.get('recruitment') or []:
            if row.get('route',{}).get('name_zh'): row['route']['name_zh']=_display_zh(row['route']['name_zh'])
            if row.get('join_type_zh'): row['join_type_zh']=_display_zh(row['join_type_zh'])
            if row.get('timing_zh'): row['timing_zh']=_display_zh(row['timing_zh'])
            if row.get('condition_zh'): row['condition_zh']=_display_zh(_char_condition_zh(row['condition_zh']))
            if row.get('condition_items_zh'):
                row['condition_items_zh']=[_display_zh(_char_condition_zh(x)) for x in row['condition_items_zh']]
    red_index={}
    for rec in red_records:
        for field in ('name','english_name','name_en','display_name_en','id','slug'):
            if rec.get(field): red_index.setdefault(_key(rec[field]),rec)
    for unit in data:
        match=red_index.get(_key(unit['name']))
        if match:
            unit['redfreshet']=match
            unit['recruitmentInfo']=match.get('recruitment')
            quick=match.get('quick_zh') or {}
            source_profs=match.get('skill_proficiencies') or []
            strengths=[prof_zh.get(p.get('name'),p.get('name')) for p in source_profs if isinstance(p,dict) and p.get('trait')=='得意']
            weaknesses=[prof_zh.get(p.get('name'),p.get('name')) for p in source_profs if isinstance(p,dict) and p.get('trait')=='苦手']
            if strengths: unit['proficiencies']='、'.join(strengths)
            if weaknesses:
                unit['weakSkills']='、'.join(weaknesses)
                unit['weakSkillsStatus']='documented'
            unit['aptitudeTendency']=quick.get('aptitude_tendency') or match.get('aptitude_tendency')
    matched_ids={id(u['redfreshet']) for u in data if 'redfreshet' in u}
    def _route_array(rec):
        routes=rec.get('routes') or rec.get('route_availability')
        def route_value(value):
            if isinstance(value,dict):
                value=value.get('condition_zh_tw') or value.get('condition') or value.get('requirement_zh_tw') or value.get('requirement') or ('可加入' if value.get('available') else None)
            return str(value or 'N/A')
        if isinstance(routes,list) and len(routes)==4: return [route_value(x) for x in routes]
        if isinstance(routes,dict):
            return [route_value(routes.get(k) or routes.get(k.lower())) for k in ('Cai','Dietrich','Theodora','Leda')]
        return ['N/A']*4
    for rec in red_records:
        if id(rec) in matched_ids: continue
        name=rec.get('name_en') or rec.get('english_name') or rec.get('display_name_en') or rec.get('name') or rec.get('display_name_ja') or rec.get('id') or '未命名角色'
        personal_skill=rec.get('personal_skill') or {}
        profs=rec.get('skill_proficiencies') or []
        recruitment=rec.get('recruitment') or rec.get('recruitment_conditions') or rec.get('route_and_recruitment') or rec.get('join_conditions')
        quick=rec.get('quick_zh') or {}
        personal_zh=quick.get('personal_skill') or {}
        prof_text='、'.join(str(prof_zh.get(p.get('name'),p.get('name')) if isinstance(p,dict) else p) for p in profs if p and (not isinstance(p,dict) or p.get('trait')=='得意'))
        data.append(dict(
            name=name, tier=rec.get('tier') or '追加', strong=quick.get('aptitude_tendency') or quick.get('summary') or rec.get('aptitude_tendency') or '來源未列能力傾向',
            target=rec.get('recommended_class') or rec.get('target_class') or '未整理', routes=_route_array(rec),
            url=rec.get('source_url') or 'https://redfreshet.com/game-tools/fe-banshisenko/characters/', avatar=None,
            personalInfo={'zh':rec.get('display_name_zh_tw') or rec.get('display_name_zh') or rec.get('display_name_ja') or '', 'personal':personal_zh.get('effect_zh') or personal_skill.get('effect_zh_tw') or personal_skill.get('effect'),
                'personalStatus':'documented' if (personal_zh.get('effect_zh') or personal_skill.get('effect')) else 'omitted','crests':[],'crestStatus':'not_listed',
                'proficiencies':prof_text or None,'source':rec.get('source_url') or character_source.name},
            combatNotes=quick.get('combat_notes') or rec.get('combat_notes') or '來源追加角色；戰鬥評價尚未整理', proficiencies=quick.get('proficiencies') or prof_text or None,
            weakSkills=None, weakSkillsStatus='not_provided', redfreshet=rec, sourceAdditional=True,
            recruitmentInfo=recruitment, playable=rec.get('playable'), rosterGroup=rec.get('roster_group'), aptitudeTendency=quick.get('aptitude_tendency') or rec.get('aptitude_tendency'),
        ))
    missing=[u['name'] for u in data if 'redfreshet' not in u and not u.get('sourceAdditional')]
    print(f'Redfreshet character merge: {50-len(missing)}/50 base matched; {len(data)-50} additional records'+(f'; base missing: {", ".join(missing)}' if missing else ''))

# Game8 calls these Preferred Skills and Non-Ideal Skills. Its tier-list
# explanation treats them as Class EXP learning affinities, so keep them
# separate from stat growths and general combat strengths/weaknesses.
game8_skill_source=root/'game8-skills.json'
if game8_skill_source.exists():
    game8_payload=json.loads(game8_skill_source.read_text(encoding='utf-8'))
    game8_index={_key(x.get('name')):x for x in game8_payload.get('characters',[]) if isinstance(x,dict)}
    game8_skill_zh={
        'Sword':'劍術','Spear':'槍術','Axe':'斧術','Bow':'弓術','Gauntlet':'格鬥術',
        'White Magic':'白魔術','Black Magic':'黑魔術','Authority':'指揮術',
        'Infantry':'步兵術','Riding':'馬術','Heavy Armor':'重裝術','Flying':'飛行術',
    }
    matched=0
    for unit in data:
        rec=game8_index.get(_key(unit['name']))
        if not rec:
            continue
        matched+=1
        unit['game8Boons']=[game8_skill_zh.get(x,x) for x in rec.get('boons',[])]
        unit['game8Banes']=[game8_skill_zh.get(x,x) for x in rec.get('banes',[])]
        unit['game8SkillSource']=rec.get('source_url') or unit.get('url')
    print(f'Game8 skill affinities: {matched}/{len(game8_index)} matched')
(root/'characters.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def _text_list(values):
    return '；'.join(str(v) for v in (values or []) if v not in (None,'')) or '來源未列出'

def _format_req_tree(node):
    if not isinstance(node,dict): return ''
    if node.get('type')=='requirement':
        text=node.get('text_zh_tw') or node.get('text_ja') or ''
        return '' if text.startswith(('條件：','条件：')) else text
    parts=[_format_req_tree(x) for x in node.get('items',[])]
    parts=[x for x in parts if x]
    if not parts: return ''
    if node.get('mode')=='any': return parts[0] if len(parts)==1 else '（'+' ／ '.join(parts)+'，任一）'
    return ' ＋ '.join(parts)

def _zh_text(value):
    text=str(value)
    replacements={
        'ディートリヒ篇で戰技強化を10回以上行い、スミルノス神殿の受付に話しかける。':'迪托利希篇中，強化戰技至少10次後，與斯米爾諾斯神殿櫃檯人員交談。',
        '救世篇 第2区分の残り1ターンで發生する':'救世篇第2區段剩餘1回合時發生的',
        'カイ篇・名聲Lv10で':'凱伊篇・名聲Lv10時，',
        'カイ篇':'凱伊篇','ディートリヒ篇':'迪托利希篇','セオドラ篇':'賽奧朵拉篇','レダ篇':'蕾達篇',
        '救世篇':'救世篇','カストールの稽古':'卡斯托爾的訓練','アウロラの稽古':'奧羅拉的訓練',
        '父からの秘密の委託':'父親的秘密委託','母からの特別な委託':'母親的特別委託',
        '挑戦者求む！':'徵求挑戰者！','挑戰者求む！':'徵求挑戰者！','新商品を作ってお披露目したい':'希望製作並展示新商品',
        '戰備增強をすべて達成':'完成全部戰備增強','試驗アイテムを入手':'取得考試道具',
        '神殿修復後の委託':'神殿修復後的委託','残り1ターンで發生する':'剩餘1回合時發生的',
        '戰技強化を10回以上行い、':'強化戰技至少10次後，','受付に話しかける':'與櫃檯人員交談',
        'を通關':'並通關','までの':'之前的','からの委託':'的委託','の間で':'之間並',
        'の受付':'的櫃檯','の挑戰状':'的挑戰書','第1区分':'第1區段','第2区分':'第2區段','第3区分':'第3區段',
        '天冠の神殿':'天冠神殿','アウロラの委託':'奧羅拉的委託','第2區段の':'第2區段的',
        '飛槍のイル・イラ':'飛槍・伊爾伊拉','必滅のオウコ':'必滅・歐科',
        'クレール神殿':'克萊爾神殿','マーズ神殿':'瑪爾斯神殿','スミルノス神殿':'斯米爾諾斯神殿',
        'カーラ神殿':'卡拉神殿','ジュラ神殿':'朱拉神殿',
        '凱伊篇・名聲Lv10で':'凱伊篇・名聲Lv10時，','迪托利希篇で':'迪托利希篇中，',
        'スミルノス神殿の與櫃檯人員交談':'斯米爾諾斯神殿與櫃檯人員交談',
        '試験手形':'考試證','下級':'初級','中級':'中級','上級':'上級','最高級':'最高級',
    }
    for old,new in sorted(replacements.items(),key=lambda x:len(x[0]),reverse=True): text=text.replace(old,new)
    return _display_zh(text)

def _skill_name_zh(value):
    text=str(value or '未命名技能')
    replacements={
        '白魔術の極限':'白魔術極限','黒魔術の探求':'黑魔術探求','鍵開け':'開鎖','黄金騎走':'黃金騎行',
        'なし':'無','不退構え':'不退架勢','引き締め':'振作','影晦まし':'隱匿身影','技冴え':'技巧精進',
        '特別な踊り':'特別舞蹈','立て直し':'重整態勢','籠城崩し':'破城','速さ呪縛':'速度咒縛','駆け抜け':'疾馳',
    }
    for old,new in replacements.items(): text=text.replace(old,new)
    text=text.replace('の','').replace('黒','黑').replace('剣','劍').replace('黄金','黃金')
    return _display_zh({'不退構え':'不退架勢','技冴え':'技巧精進','速さ呪縛':'速度咒縛'}.get(text,text))

def _class_from_red(c):
    q=c.get('qualification') or {}
    stats=c.get('stats') or {}
    skill_rows=c.get('class_skills_and_master_rewards') or c.get('skills') or []
    skills=[]
    for s in skill_rows:
        if not isinstance(s,dict):
            skills.append({'name':str(s),'type':'技能','requirement':'來源未列出','effect':'來源未列出'})
            continue
        skills.append({
            'name':_skill_name_zh(s.get('name_zh_tw') or s.get('name') or s.get('skill_name')),
            'type':_display_zh(s.get('type_zh_tw') or s.get('type') or s.get('kind') or '技能'),
            'requirement':_display_zh(s.get('level_requirement_zh_tw') or s.get('acquisition_requirement_zh_tw') or s.get('level_requirement') or s.get('requirement') or s.get('acquisition_requirement') or '來源未列等級'),
            'effect':_display_zh(s.get('effect_zh_tw') or s.get('description_zh_tw') or s.get('effect') or s.get('description') or '來源未列出'),
        })
    stat_names={'力':'力量','速さ':'速度','技':'技巧','守備':'防禦','魔防':'魔防','幸運':'幸運','魅力':'魅力','魔力':'魔力','HP':'HP'}
    fixed=[]; growth=[]
    for stat,values in stats.items():
        if not isinstance(values,dict): continue
        av=values.get('ability_modifier')
        gv=values.get('growth_modifier')
        label=stat_names.get(stat,stat)
        if av not in (None,0,'0'): fixed.append(f'{label}{int(av):+d}' if isinstance(av,(int,float)) else f'{label}{av}')
        if gv not in (None,0,'0'): growth.append(f'{label}{int(gv):+d}' if isinstance(gv,(int,float)) else f'{label}{gv}')
    unlock=[]
    if q.get('recommended_level') is not None: unlock.append(f"推薦 Lv.{q['recommended_level']}")
    if q.get('fame_level') is not None: unlock.append(f"名聲 Lv.{q['fame_level']}")
    if q.get('exam_ticket_zh_tw') or q.get('exam_ticket'): unlock.append(_zh_text(q.get('exam_ticket_zh_tw') or q.get('exam_ticket')))
    unlock.extend(_zh_text(x) for x in (q.get('unlock_conditions_zh_tw') or q.get('unlock_conditions') or []) if x)
    class_name=c.get('english_name') or c.get('name_en') or c.get('display_name_en') or c.get('name') or '未命名職業'
    display_name=_display_zh(c.get('name_zh_tw') or c.get('display_name_zh_tw') or c.get('display_name_zh') or c.get('name_zh') or '')
    aliases=[x for x in (c.get('name'),c.get('display_name_ja'),c.get('name_zh_tw'),c.get('display_name_zh_tw'),c.get('display_name_zh'),c.get('english_name'),c.get('name_en')) if x]
    class_en={'飛駝兵':'Ornius Rider','軽騎兵':'Light Cavalry','バーディンガー':'Bardinger','剣士':'Myrmidon','シドー':'Shido','スナイパー':'Sniper','ヘヴィアーマー':'Dreadnought','ビショップ':'Bishop','ウァテス':'Ovate','ウォーリアー':'Warrior','フォレストナイト':'Forest Knight','ブリガンド':'Brigand','ローグ':'Rogue','アーチャー':'Archer','重装歩兵':'Armored Knight','騎甲駝兵':'Armored Ornius Rider','シャーマン':'Shaman','プリースト':'Priest','セスタス':'Pugilist','闘士':'Gladiator','兵士':'Soldier','呪い師':'Diviner','猟兵':'Hunter','戦車兵':'Charioteer','天翼兵':'Wing Soldier','カラドリオス':'Caladrius','ドラグーン':'Dragoon','トルバドール':'Troubadour','カタフラクト':'Cataphract','戦象兵':'Elephant Rider','バトルモンク':'War Monk'}
    if c.get('name') in class_en: aliases.append(class_en[c['name']])
    class_prof_zh={'剣術':'劍術','槍術':'槍術','斧術':'斧術','弓術':'弓術','格闘術':'格鬥術','白魔術':'白魔術','黒魔術':'黑魔術','指揮術':'指揮術','歩兵術':'步兵術','馬術':'馬術','重装術':'重裝術','飛行術':'飛行術'}
    exp_bonuses=[]
    for bonus_row in c.get('skill_exp_bonuses') or []:
        if isinstance(bonus_row,dict):
            bonus_row=dict(bonus_row)
            for key in ('skill','name'):
                if bonus_row.get(key): bonus_row[key]=class_prof_zh.get(bonus_row[key],bonus_row[key])
        exp_bonuses.append(bonus_row)
    return dict(
        name=class_name, zh=display_name or '', tier=c.get('rank_zh_tw') or c.get('rank') or c.get('tier') or '未分類',
        req=_format_req_tree(q.get('requirements_tree_zh_tw') or q.get('requirements_tree')) or '無技能門檻（僅特殊解鎖）',
        unlock='；'.join(dict.fromkeys(unlock)) or '來源未列出',
        ability='；'.join(f"{s['name']}：{s['effect']}" for s in skills if '精通' not in str(s['type']) and 'マスター' not in str(s['type'])) or '來源未列出',
        master='；'.join(f"{s['name']}：{s['effect']}" for s in skills if '精通' in str(s['type']) or 'マスター' in str(s['type'])) or '來源未列出',
        skills=skills, move=c.get('movement') or '來源未列出',
        bonus='、'.join(fixed) or '來源未列出', growth='、'.join(growth) or '來源未列出',
        weapons=c.get('equippable_weapons_zh_tw') or c.get('equippable_weapons') or [], usableSkills=c.get('usable_skills_zh_tw') or c.get('usable_skills') or [],
        skillExpBonuses=exp_bonuses, aliases=aliases,
        url=c.get('source_url') or c.get('url') or 'https://redfreshet.com/game-tools/fe-banshisenko/classes/',
        source='Redfreshet', redfreshet=c,
    )

class_source=root/'redfreshet-classes.json'
if class_source.exists():
    class_payload=json.loads(class_source.read_text(encoding='utf-8'))
    jobs=[_class_from_red(c) for c in _records(class_payload,'classes')]
    if not jobs: raise ValueError('redfreshet-classes.json exists but contains no class records')
    print(f'Redfreshet classes: {len(jobs)} loaded')
else:
    jobs=[]
    for line in (root/'classes.txt').read_text(encoding='utf-8').splitlines():
        n,z,t,r,a,m,v,b,g,p=line.split('|')
        jobs.append(dict(name=n,zh=z,tier=t,req=r,unlock=('Lv.5／名聲1' if t=='初階' else 'Lv.20／名聲4' if t=='專門' else 'Lv.35／名聲8'),ability=a,master=m,skills=[],move=v,bonus=b,growth=g,url='https://game8.co/games/Fire-Emblem-Fortunes-Weave/archives/'+p,source='Game8'))
    assert len(jobs)==32
(root/'classes.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
template=(root/'template.html').read_text(encoding='utf-8')
template=template.replace('src="recruitment.png"','src="data:image/png;base64,'+base64.b64encode((root/'recruitment.png').read_bytes()).decode('ascii')+'"')
(root/'index.html').write_text(template.replace('/*DATA*/',json.dumps(data,ensure_ascii=False)).replace('/*CLASSES*/',json.dumps(jobs,ensure_ascii=False)),encoding='utf-8')
print(f'Built {len(data)} characters (50 route-chart + {len(data)-50} source additions); route counts 41 / 44 / 44 / 42')
