# NTUST CIT Master thesis

專案位置
https://github.com/cosmos23cg/MunsellColorReproduction

## 概述
此專案為碩士論文中所使用到的程式碼。以下為此篇論文基本資訊：
**學校**: 國立臺灣科技大學色彩與照明科技研究所
**碩論**: 以數位印刷技術複製曼賽爾色票之可行性研究
**研究生**: 蕭強
**指導教授**: 陳鴻興教授

## 如何使用
此專案用poetry進行套件管理，執行下方指令後，即可安裝相關套件。
> poetry install


## 專案內容
analysis.py: 分析munsell HVC個別的de2000, delta L*, C_ab, H_ab，並且找出幸賴區間、最大/小值，並輸出csv檔案
combine_hue.py：此腳本讀取每一個csv檔案後，依照Munsell HVC規則重新排列並輸出csv檔
deepblue_txt_fetch.py：抓取GMG軟體輸出的字串
parse_txt.py：抓取babel color輸出的munsell色票數據
plot_contour.py：畫等高線圖
plot_gamut.py：畫色域範圍
plot_histogram.py：畫色差值方圖
plot_munsell_page.py：畫色相頁
plot_scatter.py：畫HVC色分布與信賴區間範圍