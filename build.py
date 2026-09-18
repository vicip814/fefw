import json, pathlib, base64
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
(root/'characters.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
jobs=[]
for line in (root/'classes.txt').read_text(encoding='utf-8').splitlines():
    n,z,t,r,a,m,v,b,g,p=line.split('|')
    jobs.append(dict(name=n,zh=z,tier=t,req=r,ability=a,master=m,move=v,bonus=b,growth=g,url='https://game8.co/games/Fire-Emblem-Fortunes-Weave/archives/'+p))
assert len(jobs)==32
(root/'classes.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
template=(root/'template.html').read_text(encoding='utf-8')
template=template.replace('src="recruitment.png"','src="data:image/png;base64,'+base64.b64encode((root/'recruitment.png').read_bytes()).decode('ascii')+'"')
(root/'index.html').write_text(template.replace('/*DATA*/',json.dumps(data,ensure_ascii=False)).replace('/*CLASSES*/',json.dumps(jobs,ensure_ascii=False)),encoding='utf-8')
print('Built 50 characters; route counts 41 / 44 / 44 / 42')
