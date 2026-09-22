# 萬縷千絲｜四線角色與職業速查

繁體中文、深色、手機友善的靜態攻略。直接打開 `index.html` 即可使用；資料內嵌，不需 API、npm 或外部字型。

- 63 位角色：原招募圖50人保留第一部四線門檻、tier及培養建議，另加入Redfreshet收錄的13名追加／隱藏角色。第一部四線可用數仍為41 / 44 / 44 / 42，交集37人。
- 搜尋、路線、tier、可招募與排序篩選；每人擅長提升的武器／技能、學習弱項、高階目標及建議培養鏈。學習弱項未有來源資料時標「未提供」，不以未列專長推斷；戰鬥短板／運用條件另列。
- 原50位角色卡均有44px小頭像，以招募圖的CSS局部顯示製作；新增13人使用文字頭像，避免冒用錯誤肖像。`avatar-positions.json`維護原50人的圖中位置。
- Redfreshet逐頁資料含63人的能力成長傾向、擅長／不擅長技能、初始技能級別、287筆習得技能、245筆禮物反應與各線加入方法；追加角色清楚標為「追加／未整理」，不擅自評tier或推薦最終職業。
- 個人技能與血印效果依指定Entertainment14角色資料文章：44人的個人技能有明確效果，10人有共12项血印；其餘缺欄／調查中／角色未列均明確標示，血印未列不推斷為無。6人的個人技缺口保留既有Game8摘要作另標來源的補充參考。
- 個人技能及血印內容、來源中文名可搜尋；已校正Fabio／Dante／Io的必殺迴避、Kiroc必殺增益、Loretta半血條件及Buccar傷害×90%語義。
- 60個職業：轉職所需武器技能、推薦等級、名聲、考試證與特殊解鎖條件，並列固定能力、成長修正、可用武器、職業技能及精通獎勵。
- 主角Lord獨立分類，不將其當作S級以上；招募依使用者附圖，tier及角色／職業解釋依Game8 2026-09-18快照。
- 編者推論、來源矛盾與TBD均在頁面標明。沒有實機測試，未宣稱挑戰模式最優解。

## 更新

修改 `build.py`、`redfreshet-characters.json`、`redfreshet-classes.json` 或 `template.html`，執行：

```sh
python build.py
```

會產生 `characters.json`、`classes.json` 與完整 `index.html`。`recruitment.png` 是使用者提供的招募原圖，build時內嵌到HTML，頁內可展開對照。HTML單檔離線可用，JSON僅供資料維護。所有來源連結在頁內。

`personal-skills.json`維護個人技／血印及缺資料狀態。可用選用匯入工具 `python import-personal-source.py source-entertainment14.html` 從指定文章HTML快照擷取欄位（需beautifulsoup4）；完整來源網頁不提交。血印名稱未在文章提供，本站呈現其觸發與效果。Redfreshet兩份JSON保留逐頁資料及來源網址，方便追溯。

發布到GitHub僅代表程式碼已推送，未自動開啟GitHub Pages。
