# 健康飲食系統
##### 組長：沈映廷
##### 組員：鄭淑娟、鄭婷勻、王紫璇、劉羿葳

本組設計了一個能幫助使用者檢視自己飲食狀況的系統，希望能透過此專案，讓民眾了解==健康飲食==的重要性，並改善外食族群==營養不均衡==的問題。

---

### 1.研究動機
- **外食成為主要飲食方式**
- **民眾對營養均衡的重視度不足**
- **均衡飲食對健康至關重要**
- **提升大眾對健康飲食的認知**
- **設計簡單飲食系統提供健康建議**

### 2.研究目的
本專案的目的在於設計出一個飲食評估系統，以幫助外食族群檢視自身的飲食狀況，提升大眾對健康飲食的認知。
 **系統將包含多方面的功能：**
#### LINE 官方帳號
- **圖文選單**
    - **前往官網** ：點選後可進入官網畫面查看更多內容。
    - **飲食小知識** ：使用者點擊後系統會提供建議，並提醒使用者需要注意的健康事項。
    - **意見回饋** ：收集使用者或客戶對產品、系統服務的評價和建議。
    - **計算健康** ：點選後可進入官網的計算健康頁面。
    - **文章** ：點選後可選擇查看增肌或減脂之文章，系統將提供相關內容。
    - **推薦好友** ：點選後可以與好友們分享本系統。
- **圖片辨識** ：使用者上傳圖片後，系統將辨識圖片中的食物，並提供該食物的名稱與卡路里資訊。
#### 官網畫面
- **推薦菜單** ：點進減脂和增肌頁面，即可查看相關菜色。
- **飲食小知識** ：顯示於減脂及增肌的頁面上方處，使用者點擊後會顯示需要注意的健康事項。
- **計算BMI、體脂率、基礎代謝率** ：使用者輸入基本資料身高體重後，即可了解相關指數的分析結果。
- **意見回饋** ：顯示於網頁最下方處，收集使用者或客戶對產品、系統服務的評價和建議。

### 3.未來可應用領域
- **個人健康管理** ：系統提供有關健康飲食、運動和生活方式的減脂與增肌小知識，幫助用戶制定合適的飲食計劃。
- **健身教練與營養師輔助工具** ：可為民眾提供健康指導，透過自動化計算功能，追蹤會員健康變化，提出專業的運動方式與飲食建議。
- **健康與營養教育** ：向學生或居民普及健康飲食與運動的知識。

### 4.系統開發工具
| **項目** | 內容 |
| --- | :--: |
| **開發工具與編程語言** | Python、HTML、JavaScript、CSS |
| **資料庫與雲端平台** | Firebase、Azure |
| **版本控制與協作平台** | GitHub |
| **硬體設備** | 筆記型電腦、手機 |

### 5.系統實作與展示
#### 官方帳號
加入後會出現以下訊息，並簡介系統的用途。
![官網](./website/圖片/官網.jpg)

#### 圖文選單
提供六項功能給使用者點選：
![圖文選單](website/圖片/圖文選單.png)

**(1) 前往官網**
[![主頁](website/圖片/主頁.jpg)](https://yingting-992.github.io/healthy/website/front_page/front_page.html)

**(2) 飲食小知識**
可選擇減脂或是增肌的小知識。
![小知識](website/圖片/小知識.jpg)

顯示後的圖文訊息可左滑查看更多。
![小知識](website/圖片/小知識2.jpg)

**(3) 意見回饋**
可選擇三種類型的回饋內容。
![意見回饋](website/圖片/意見回饋.jpg)

點選後即可輸入訊息並發送。
![意見回饋](website/圖片/意見回饋2.jpg)

**(4) 計算健康**
跳至網頁中的**計算健康**頁面，下方會做更詳細的介紹。

**(5) 文章**
可選擇要查詢增肌或是減脂的文章。
![文章](website/圖片/文章.jpg)

點選後會利用爬蟲的功能出現對應內容，最底下會附上連結，可查看完整文章。
![文章](website/圖片/文章2.jpg)

**(6) 推薦好友**
點選後可將官方帳號傳送給其他好友，讓更多人加入健康飲食的行列！
#### 圖片辨識
傳送水果圖片會回傳名稱及熱量資訊。
![圖片辨識](website/圖片/圖片辨識.jpg)

#### 官網頁面
減脂和增肌頁面上方提供飲食小知識區塊，點選後可查看詳細內容，中間的部分則是推薦菜單。
**(1) 減脂飲食**
![減脂](website/圖片/減脂.jpg)

**(2) 增肌飲食**
![增肌](website/圖片/增肌.jpg)

**(3) 計算健康**
- 輸入基本資料，系統會幫忙算出BMI、體脂率、BMR。
![計算健康](website/圖片/計算.png)

- 還可以選擇活動程度，進行熱量消耗計算。
![選擇活動](website/圖片/活動.png)

**(4) 頁尾**
![頁尾](website/圖片/頁尾.jpg)
- 頁尾左側提供掃碼功能，可加入LINE官方帳號。
- 中間部分提供回饋功能，使用者可隨時提出問題或使用感想。
- 右側的箭頭圖標能讓使用者隨時回到頁面最上方，方便瀏覽。

### 6.結論與未來展望
#### 結論
現代人的飲食習慣多半受限於繁忙的工作與生活節奏，外食成為普遍現象，然而，缺乏營養知識和飲食規劃常導致==健康問題==。因此，設計一個簡單易用、能提供營養建議的飲食系統對於改善外食族群的健康具有重大意義。透過這樣的系統，使用者可以在日常外食中輕鬆做出更健康的選擇，達成==營養均衡==的目標，==改善整體生活品質==。
#### 未來展望
- **智能化功能提升：** 對用戶的飲食模式進行更精確的分析。例如：根據用戶的飲食習慣、體型變化、運動量等數據，提供更適合的飲食計劃。
- **跨平台整合：** 除了LINE平台，未來系統可以擴展至其他主流平台，如Facebook、Instagram等社交媒體，提升其覆蓋面與可用性。
- **社群互動功能：** 讓使用者可以與家人、朋友、健身夥伴等分享飲食記錄、健身成果及健康知識，並在系統內部形成一個健康飲食的社群。
- **數據分析與報告功能：** 強化數據分析能力，並能提供詳細的健康報告，讓用戶能清楚了解自己的飲食與健康狀況。例如：長期追蹤結果、飲食偏好分析等等。

### 7.分工表
| **姓名** | **分工內容** |
| :--: | --- |
| **沈映廷** | 網頁設計、Azure自訂視覺(影響偵測)、firebase 後台連結 |
| **鄭淑娟** | 網頁設計、email回饋功能、爬文章&顯示、Azure Blob storage 圖片儲存 |
| **鄭婷勻** | 圖文選單設計、企畫書、網頁優化、文書總結專案、email 回饋功能 |
| **王紫璇** | 飲食小知識、推薦好友、操作介面整合及測試、email回饋功能 |
| **劉羿葳** | 爬蟲資料與蒐集、自訂視覺(製作及維護)