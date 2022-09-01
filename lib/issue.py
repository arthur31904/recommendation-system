"""
內容	解釋	格式
server_time	            伺服器響應時間	        utc timestamp
server_time_consumed	伺服器運行花費時間	    uyc timestamp
message	                伺服器訊息	        string
code	                訊息代碼	            int
status	                狀態，success、fail	string
response	            回應資料	            json

常見錯誤代碼	代碼
系統錯誤	601
連線異常	602
資料庫錯誤	603
權限異常	604
創建異常	xxx1
資料重複	xxx2
更新異常	xxx3
讀取異常	xxx4


"""
issue = {
    # 系統
    "601": {"code": 601, "message": u"System Error.", "zh_tw": u"系統錯誤"},
    "602": {"code": 602, "message": u"Connect Error.", "zh_tw": u"連線異常"},
    "603": {"code": 603, "message": u"DataBase Error.", "zh_tw": u"資料庫錯誤"},
    "604": {"code": 604, "message": u"Permission Error.", "zh_tw": u"權限異常"},
    "901": {"code": 901, "message": u"Data Type Error: {}", "zh_tw": u"參數傳輸格式錯誤"},
    "902": {"code": 902, "message": u"Email Send Error: {}", "zh_tw": u"信件寄送失敗"},
    "903": {"code": 903, "message": u"Recaptcha Verification Error: {}", "zh_tw": u"Google驗證失敗"},

    # 網站設定(Optimization)
    "951": {"code": 951, "message": u"Optimization Create Data Error: {}", "zh_tw": u"網站設定創建異常"},
    "952": {"code": 952, "message": u"Optimization already exist.", "zh_tw": u"網站設定已存在"},
    "953": {"code": 953, "message": u"Optimization Update Data Error: {}", "zh_tw": u"網站設定更新異常"},
    "954": {"code": 954, "message": u"Optimization Read Data Error: {}", "zh_tw": u"網站設定讀取異常"},
    "955": {"code": 955, "message": u"Optimization is not exist.", "zh_tw": u"網站設定不存在"},
    "956": {"code": 956, "message": u"Optimization Delete Data Error: {}", "zh_tw": u"網站設定刪除異常"},
    "956": {"code": 956, "message": u"Optimization Delete Data Error: {}", "zh_tw": u"網站設定刪除異常"},

    # 帳號(account)
    "1001": {"code": 1001, "message": u"Account Create Data Error: {}", "zh_tw": u"帳號資料創建異常"},
    "1002": {"code": 1002, "message": u"帳號已存在", "zh_tw": u"帳號已存在"},
    "1003": {"code": 1003, "message": u"Account Update Data Error: {}", "zh_tw": u"帳號資料更新異常"},
    "1004": {"code": 1004, "message": u"Account Read Data Error: {}", "zh_tw": u"帳號資料讀取異常"},
    "1005": {"code": 1005, "message": u"帳號不存在", "zh_tw": u"帳號不存在"},
    "1006": {"code": 1006, "message": u"Password Error.", "zh_tw": u"密碼錯誤"},
    "1007": {"code": 1007, "message": u"此帳號已凍結,請洽管理員.", "zh_tw": u"此帳號已凍結,請洽管理員"},
    "1008": {"code": 1008, "message": u"Send Email Error.", "zh_tw": u"寄信錯誤"},
    "1009": {"code": 1009, "message": u"Email Token is invalid", "zh_tw": u"驗證碼失效"},
    "1010": {"code": 1010, "message": u"Google Email Auth Error", "zh_tw": u"Google Email 驗證失敗"},
    "1011": {"code": 1011, "message": u"Facebook Email Auth Error", "zh_tw": u"Facebook Email 驗證失敗"},
    "1012": {"code": 1012, "message": u"登入帳號密碼錯誤", "zh_tw": u"登入帳號密碼錯誤"},

    # 文章(article)
    "1401": {"code": 1401, "message": u"Article Create Data Error: {}", "zh_tw": u"文章資料創建異常"},
    "1402": {"code": 1402, "message": u"文章已存在", "zh_tw": u"文章已存在"},
    "1403": {"code": 1403, "message": u"Article Update Data Error: {}", "zh_tw": u"文章資料更新異常"},
    "1404": {"code": 1404, "message": u"Article Read Data Error: {}", "zh_tw": u"文章資料讀取異常"},
    "1405": {"code": 1405, "message": u"Article is not exist.", "zh_tw": u"文章不存在"},


    # 會員(Member)
    "2001": {"code": 2001, "message": u"會員資料創建異常", "zh_tw": u"會員資料創建異常"},
    "2002": {"code": 2002, "message": u"會員已存在", "zh_tw": u"會員已存在"},
    "2003": {"code": 2003, "message": u"會員資料更新異常", "zh_tw": u"會員資料更新異常"},
    "2004": {"code": 2004, "message": u"會員資料讀取異常", "zh_tw": u"會員資料讀取異常"},
    "2005": {"code": 2005, "message": u"會員不存在", "zh_tw": u"會員不存在"},
    "2006": {"code": 2006, "message": u"此Email已使用", "zh_tw": u"此Email已使用"},
    "2007": {"code": 2007, "message": u"此電話已使用", "zh_tw": u"此電話已使用"},
    "2008": {"code": 2008, "message": u"驗證碼錯誤", "zh_tw": u"驗證碼錯誤"},
    "2009": {"code": 2009, "message": u"此帳號已凍結,請洽管理員", "zh_tw": u"此帳號已凍結,請洽管理員"},
    "2010": {"code": 2010, "message": u"此身分證字號/護照號碼已使用", "zh_tw": u"此身分證字號/護照號碼已使用"},
    "2011": {"code": 2011, "message": u"無此Email對應的帳號存在", "zh_tw": u"無此Email對應的帳號存在"},
    "2012": {"code": 2012, "message": u"無此手機對應的帳號存在", "zh_tw": u"無此手機對應的帳號存在"},
    "2013": {"code": 2013, "message": u"請填妥會員資料", "zh_tw": u"驗證碼錯誤"},
    "2014": {"code": 2014, "message": u"會員未開通", "zh_tw": u"會員未開通"},
    "2015": {"code": 2015, "message": u"請先取得驗證碼", "zh_tw": u"請先取得驗證碼"},

    # Image
    "2401": {"code": 2401, "message": u"Image is not exist.", "zh_tw": u"圖片不存在"},
    "2402": {"code": 2402, "message": u"Image Permission Error.", "zh_tw": u"圖片權限錯誤"},
    "2403": {"code": 2403, "message": u"Image Params Error.", "zh_tw": u"圖片參數錯誤"},
    "2404": {"code": 2404, "message": u"Image Format Error.", "zh_tw": u"圖片檢查格式錯誤"},
    "2405": {"code": 2405, "message": u"Image Upload File Error: {}", "zh_tw": u"圖片上傳當案錯誤"},
    "2406": {"code": 2406, "message": u"Image Upload Base64 Error.", "zh_tw": u"圖片上傳Base64錯誤"},
    "2407": {"code": 2407, "message": u"Image Upload link Error.", "zh_tw": u"圖片上傳連結錯誤"},
    "2408": {"code": 2408, "message": u"Image Upload Other File Error.", "zh_tw": u"圖片上傳其他錯誤"},
    "2409": {"code": 2409, "message": u"Image API Get Error.", "zh_tw": u"圖片API Get錯誤"},
    "2411": {"code": 2411, "message": u"Image Create Data Error: {}", "zh_tw": u"圖片資料創建異常"},
    "2412": {"code": 2412, "message": u"Image Read Data Error: {}", "zh_tw": u"圖片資料讀取異常"},
    "2413": {"code": 2413, "message": u"Image Update Data Error: {}", "zh_tw": u"圖片資料更新異常"},
    "2414": {"code": 2414, "message": u"Image Delete Data Error: {}", "zh_tw": u"圖片資料刪除異常"},

    # News
    "3001": {"code": 3001, "message": u"News Create Data Error: {}", "zh_tw": u"News創建資料異常"},
    "3002": {"code": 3002, "message": u"News Edit Data Error: {}", "zh_tw": u"News編輯資料異常"},
    "3003": {"code": 3003, "message": u"News Get List Data Error: {}", "zh_tw": u"News搜尋列表資料異常"},
    "3004": {"code": 3004, "message": u"News Get Data Error: {}", "zh_tw": u"News搜尋取得資料異常"},
    "3005": {"code": 3005, "message": u"News is not exist.", "zh_tw": u"News不存在"},
    "3006": {"code": 3006, "message": u"News Delete Error: {}.", "zh_tw": u"News不存在"},

    # 分類相關
    "6001": {"code": 6001, "message": u"Category Create Data Error: {}", "zh_tw": u"Category創建資料異常"},
    "6002": {"code": 6002, "message": u"Category Edit Data Error: {}", "zh_tw": u"Category編輯資料異常"},
    "6003": {"code": 6003, "message": u"Category Get List Data Error: {}", "zh_tw": u"Category搜尋列表資料異常"},
    "6004": {"code": 6004, "message": u"Category Get Data Error: {}", "zh_tw": u"Category搜尋取得資料異常"},
    "6005": {"code": 6005, "message": u"Category is not exist.", "zh_tw": u"Category不存在"},
    "6006": {"code": 6006, "message": u"Category Delete Error: {}.", "zh_tw": u"Category不存在"},

    # 標籤(Tag)
    "7001": {"code": 7001, "message": u"Tag Create Data Error: {}", "zh_tw": u"標籤創建異常"},
    "7002": {"code": 7002, "message": u"Tag already exist.", "zh_tw": u"標籤已存在"},
    "7003": {"code": 7003, "message": u"Tag Update Data Error: {}", "zh_tw": u"標籤更新異常"},
    "7004": {"code": 7004, "message": u"Tag Read Data Error: {}", "zh_tw": u"標籤讀取異常"},
    "7005": {"code": 7005, "message": u"Tag is not exist.", "zh_tw": u"標籤不存在"},
    "7006": {"code": 7006, "message": u"Tag Delete Data Error: {}", "zh_tw": u"標籤刪除異常"},

    # 影片(Video)
    "7101": {"code": 7101, "message": u"Video Create Data Error: {}", "zh_tw": u"影片創建異常"},
    "7102": {"code": 7102, "message": u"Video already exist.", "zh_tw": u"影片已存在"},
    "7103": {"code": 7103, "message": u"Video Update Data Error: {}", "zh_tw": u"影片更新異常"},
    "7104": {"code": 7104, "message": u"Video Read Data Error: {}", "zh_tw": u"影片讀取異常"},
    "7105": {"code": 7105, "message": u"Video is not exist.", "zh_tw": u"影片不存在"},
    "7106": {"code": 7106, "message": u"Video Delete Data Error: {}", "zh_tw": u"影片刪除異常"},

    # 供應商(Vendor)
    "7201": {"code": 7201, "message": u"Vendor Create Data Error: {}", "zh_tw": u"供應商創建異常"},
    "7202": {"code": 7202, "message": u"Vendor already exist.", "zh_tw": u"供應商已存在"},
    "7203": {"code": 7203, "message": u"Vendor Update Data Error: {}", "zh_tw": u"供應商更新異常"},
    "7204": {"code": 7204, "message": u"Vendor Read Data Error: {}", "zh_tw": u"供應商讀取異常"},
    "7205": {"code": 7205, "message": u"Vendor is not exist.", "zh_tw": u"供應商不存在"},
    "7206": {"code": 7206, "message": u"Vendor Delete Data Error: {}", "zh_tw": u"供應商刪除異常"},


    # 工業事蹟
    "8001": {"code": 8001, "message": u"Work Create Data Error: {}", "zh_tw": u"工業事蹟創建異常"},
    "8002": {"code": 8002, "message": u"Work already exist.", "zh_tw": u"工業事蹟已存在"},
    "8003": {"code": 8003, "message": u"Work Update Data Error: {}", "zh_tw": u"工業事蹟更新異常"},
    "8004": {"code": 8004, "message": u"Work Read Data Error: {}", "zh_tw": u"工業事蹟讀取異常"},
    "8005": {"code": 8005, "message": u"Work is not exist.", "zh_tw": u"工業事蹟不存在"},
    "8006": {"code": 8006, "message": u"Work Delete Data Error: {}", "zh_tw": u"工業事蹟刪除異常"},

    "8101": {"code": 8101, "message": u"Work Image Create Data Error: {}", "zh_tw": u"工業事蹟圖片創建異常"},
    "8102": {"code": 8102, "message": u"Work Image already exist.", "zh_tw": u"工業事蹟圖片已存在"},
    "8103": {"code": 8103, "message": u"Work Image Update Data Error: {}", "zh_tw": u"工業事蹟圖片更新異常"},
    "8104": {"code": 8104, "message": u"Work Image Read Data Error: {}", "zh_tw": u"工業事蹟圖片讀取異常"},
    "8105": {"code": 8105, "message": u"Work Image is not exist.", "zh_tw": u"工業事蹟圖片不存在"},
    "8106": {"code": 8106, "message": u"Work Image Delete Data Error: {}", "zh_tw": u"工業事蹟圖片刪除異常"},

    # 產品
    "8201": {"code": 8201, "message": u"Porduct Create Data Error: {}", "zh_tw": u"產品創建異常"},
    "8202": {"code": 8202, "message": u"Porduct already exist.", "zh_tw": u"產品已存在"},
    "8203": {"code": 8203, "message": u"Porduct Update Data Error: {}", "zh_tw": u"產品更新異常"},
    "8204": {"code": 8204, "message": u"Porduct Read Data Error: {}", "zh_tw": u"產品讀取異常"},
    "8205": {"code": 8205, "message": u"Porduct is not exist.", "zh_tw": u"產品不存在"},
    "8206": {"code": 8206, "message": u"Porduct Delete Data Error: {}", "zh_tw": u"產品刪除異常"},

    "8301": {"code": 8301, "message": u"Porduct Image Create Data Error: {}", "zh_tw": u"產品圖片創建異常"},
    "8302": {"code": 8302, "message": u"Porduct Image already exist.", "zh_tw": u"產品圖片已存在"},
    "8303": {"code": 8303, "message": u"Porduct Image Update Data Error: {}", "zh_tw": u"產品圖片更新異常"},
    "8304": {"code": 8304, "message": u"Porduct Image Read Data Error: {}", "zh_tw": u"產品圖片讀取異常"},
    "8305": {"code": 8305, "message": u"Porduct Image is not exist.", "zh_tw": u"產品圖片不存在"},
    "8306": {"code": 8306, "message": u"Porduct Image Delete Data Error: {}", "zh_tw": u"產品圖片刪除異常"},


    # banner
    "9001": {"code": 9001, "message": u"Banner Create Data Error: {}", "zh_tw": u"Banner創建資料異常"},
    "9002": {"code": 9002, "message": u"Banner Edit Data Error: {}", "zh_tw": u"Banner編輯資料異常"},
    "9003": {"code": 9003, "message": u"Banner Get List Data Error: {}", "zh_tw": u"Banner搜尋列表資料異常"},
    "9004": {"code": 9004, "message": u"Banner Get Data Error: {}", "zh_tw": u"Banner取得資料異常"},
    "9005": {"code": 9005, "message": u"Banner api get Data Error: {}", "zh_tw": u"Banner api取得資料異常"},
    "9006": {"code": 9006, "message": u"Banner api delete Data Error: {}", "zh_tw": u"Banner api刪除資料異常"},
    "9007": {"code": 9007, "message": u"Banner api create from Data Error: {}", "zh_tw": u"Banner api新增from檢查資料異常"},
    "9008": {"code": 9008, "message": u"Banner api create api Data Error: {}", "zh_tw": u"Banner api新增資料異常"},
    "9009": {"code": 9009, "message": u"Banner api edit from Data Error: {}", "zh_tw": u"Banner api編輯from檢查資料異常"},
    "9010": {"code": 9010, "message": u"Banner api edit api Data Error: {}", "zh_tw": u"Banner api編輯資料異常"},

    # 課程(class)
    "9101": {"code": 9101, "message": u"Class Create Data Error: {}", "zh_tw": u"課程資料創建異常"},
    "9102": {"code": 9102, "message": u"Class already exist.", "zh_tw": u"課程已存在"},
    "9103": {"code": 9103, "message": u"Class Update Data Error: {}", "zh_tw": u"課程資料更新異常"},
    "9104": {"code": 9104, "message": u"Class Read Data Error: {}", "zh_tw": u"課程資料讀取異常"},
    "9105": {"code": 9105, "message": u"Class is not exist.", "zh_tw": u"課程不存在"},

    # 教練(coach)
    "9401": {"code": 9401, "message": u"Coach Create Data Error: {}", "zh_tw": u"教練資料創建異常"},
    "9402": {"code": 9402, "message": u"帳號已存在", "zh_tw": u"帳號已存在"},
    "9403": {"code": 9403, "message": u"Coach Update Data Error: {}", "zh_tw": u"教練資料更新異常"},
    "9404": {"code": 9404, "message": u"Coach Read Data Error: {}", "zh_tw": u"教練資料讀取異常"},
    "9405": {"code": 9405, "message": u"Coach is not exist.", "zh_tw": u"教練不存在"},
    "9406": {"code": 9406, "message": u"課程已結束", "zh_tw": u"課程已結束"},

    "9500": {"code": 9500, "message": u"項目使用中，不可刪除", "zh_tw": u"項目使用中，不可刪除"},

    "9702": {"code": 9702, "message": u"醫生已存在", "zh_tw": u"醫生已存在"},
    # send us message
    "961": {"code": 961, "message": u"Support Email Error.", "zh_tw": u"support email 設定錯誤"},

}
