# 共通
segments = (
    "無線",
    "エネルギー",
    "ソフトウェア",
    "その他"
)

tax_rates = (
    0.0,
    0.08,
    0.10,
)

# marketing
lead_entities = (
    "法人",
    "個人",
)

lead_trade_status = (
    "新規",
    "リピート",
    "中止",
    "削除",
)

lead_ranks = (
    "A:お取引中",
    "B:見積り提示",
    "C:商談中",
    "D:コンタクト",
    "E:To Do",
)

lead_contacted_media = (
    "Pending",
    "Web Form",
    "Mail",
    "Tel",
    "Door to Door",
)

quotation_captions = (
    '資材費',
    '労務費',
    '測定器使用料',
    'システム使用料',
    'その他'
)

expiries_of_quotation = (
    "本書発行後、1ヶ月",
)

payment_conditions = (
    "現金一括、検収後1ヶ月以内",
    "現金一括、入金確認次第に手配",
    "現金50%入金確認次第手配、検収後残り現金50%"
)

quatation_conditions = (
    "出張費については実費を別途精算",
    "官公庁への代行手続きは含んでおりません",
)

project_status = (
    "計画中",
    "契約中",
    "完了",
)

# accounting
cost_types = (
    "消耗工具器具備品費",
    "修繕費",
    "事務用消耗品費",
    "旅費交通費",
    "通信費",
    "水道光熱費",
    "広告宣伝費",
    "見本費",
    "保管費",
    "法定福利費",
    "福利厚生費",
    "外注費",
    "会費",
    "交際費",
    "租税公課",
    "図書費",
    "保険料",
    "賃借料",
    "販売手数料",
    "支払手数料",
    "荷造費",
    "運搬費",
    "その他",
)

# emission
emission_sources = (
    "燃料（都市ガスを除く。）の使用",
    "都市ガスの使用",
    "他人から供給された電気の使用",
    "他人から供給された熱の使用",
    "特定事業所排出者によるもの",
    "路線便の使用(特定輸送排出者)",
    "路線便の使用(特定輸送排出者以外)",
    "チャーター便の使用(特定輸送排出者)",
    "チャーター便の使用(特定輸送排出者以外)",
    "自家用車",
    "航空機での移動",
    "バスでの移動",
    "フェリーでの移動",
    "フェリーでの輸送",
    "電車での移動",
    "電車での輸送",
    "廃棄物の焼却(廃プラ)",
    "廃棄物の焼却(紙くず)",
    "廃棄物の焼却(産廃)",
)

# https://www.env.go.jp/earth/ondanka/supply_chain/gvc/estimate.html
scope_categories = (
    'Scope1 直接排出',
    'Scope2 間接排出',
    'Scope3-1 購入した製品・サービス',
    'Scope3-2 資本財',
    'Scope3-3 Scope1, 2に含まれない燃料及びエネルギー活動',
    'Scope3-4 輸送、配送(上流)',
    'Scope3-5 事業から出る廃棄物',
    'Scope3-6 出張',
    'Scope3-7 雇用者の通勤',
    'Scope3-8 リース資産(上流)',
    'Scope3-9 輸送、配送(下流)',
    'Scope3-10 販売した製品の加工',
    'Scope3-11 販売した製品の使用',
    'Scope3-12 販売した製品の廃棄',
    'Scope3-13 リース資産(下流)',
    'Scope3-14 フランチャイズ',
    'Scope3-15 投資',
)