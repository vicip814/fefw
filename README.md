# 萬縷千絲｜四線角色與職業速查

繁體中文、深色、手機友善的靜態攻略。直接打開 `index.html` 即可使用；資料內嵌，不需 API、npm 或外部字型。

- 50 位第一部角色；四線可用數為 41 / 44 / 44 / 42，交集37人。
- 搜尋、路線、tier、可招募與排序篩選；每人武器專長、弱點、高階目標及建議培養鏈。
- 50位角色卡均有44px小頭像，以原招募圖的CSS局部顯示製作；頭像來源內嵌，可離線使用。`avatar-positions.json`維護每人的圖中位置。
- 個人技能與血印效果依指定Entertainment14角色資料文章：44人的個人技能有明確效果，10人有共12项血印；其餘缺欄／調查中／角色未列均明確標示，血印未列不推斷為無。6人的個人技缺口保留既有Game8摘要作另標來源的補充參考。
- 個人技能及血印內容、來源中文名可搜尋；已校正Fabio／Dante／Io的必殺迴避、Kiroc必殺增益、Loretta半血條件及Buccar傷害×90%語義。
- 32個職業：技能與精通效果、熟練門檻、移動、25個獨立攻略頁的固定屬性及職業成長修正；來源留白保留待核實。
- 主角Lord獨立分類，不將其當作S級以上；招募依使用者附圖，tier及角色／職業解釋依Game8 2026-09-18快照。
- 編者推論、來源矛盾與TBD均在頁面標明。沒有實機測試，未宣稱挑戰模式最優解。

## 更新

修改 `build.py` 的角色／路線資料、`classes.txt` 的職業資料或 `template.html`，執行：

```sh
python build.py
```

會產生 `characters.json`、`classes.json` 與完整 `index.html`。`recruitment.png` 是使用者提供的招募原圖，build時內嵌到HTML，頁內可展開對照。HTML單檔離線可用，JSON僅供資料維護。所有來源連結在頁內。

`personal-skills.json`維護個人技／血印及缺資料狀態。可用選用匯入工具 `python import-personal-source.py source-entertainment14.html` 從指定文章HTML快照擷取欄位（需beautifulsoup4）；完整來源網頁不提交。血印名稱未在文章提供，本站呈現其觸發與效果。

發布到GitHub僅代表程式碼已推送，未自動開啟GitHub Pages。
