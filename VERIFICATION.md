# 驗證紀錄 — 2026-09-18

- `python build.py` 成功：50 位不重複角色；四線可用數41／44／44／42；四線交集37。
- tier分布：Lord4、S2、A15、B21、C8。職業共32；25個有獨立頁面數值，7個部分資料待核實。
- 內嵌JavaScript通過 `node --check`；`git diff --check`通過。
- Codex瀏覽器實際檢查：四線切換顯示41／44／44／42；全部角色50；S級篩選顯示Esmeralda與Fianna；搜索Fianna後點Bishop連結只顯示Bishop；清除職業搜索後顯示32個職業。
- 響應式頁面寬度（viewport / document client / document scroll）：320／305／305、390／375／375、768／753／753、1440／1425／1425。差15px為瀏覽器捲軸，頁面沒有橫向溢出。
- 390px下表格局部client345／scroll540；招募原圖區域client313／scroll1776；展開原圖後頁面仍client375／scroll375。
- 內嵌PNG naturalWidth1776；瀏覽器無error console紀錄；已目視檢查390px畫面。
- 來源的留白、TBD、Buccar矛盾數值及編者推薦已明確標註。未做實機戰鬥、成長／技能疊加或挑戰模式驗證。
- 僅提交靜態檔案，沒有啟用GitHub Pages或其他部署。
