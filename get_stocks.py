import baostock as bs
import pandas as pd
import datetime 
from chinese_calendar import is_workday
import numpy as np

# 机构重仓
Institutions150_0 = ['长电科技', '卫宁健康', '东山精密', '上海机场', '中炬高新', '沃森生物', '潍柴动力', '华测检测', '健帆生物', '中国建筑',
                   '汇川技术', '冀东水泥', '天坛生物', '康泰生物', '美年健康', '药明康德', '三七互娱', '智飞生物', '益丰药房', '歌尔股份',
                   '北方华创', '海螺水泥', '爱尔眼科', '华域汽车', '先导智能', '光环新网', '上汽集团', '南极电商', '华天科技', '深南电路',
                   '东方雨虹', '三安光电', '永辉超市', '太阳纸业', '生物股份', '圣邦股份', '中国中免', '泰格医药', '浪潮信息', '格力电器',
                   '宁德时代', '海大集团', '普洛药业', '中国中车', '中国铁建', '洋河股份', '中国神华', '用友网络', '兆易创新', '立讯精密',
                   '海康威视', '山西汾酒', '晨光文具', '海天味业', '顺网科技', '生益科技', '晶方科技', '东华软件', '海尔智家', '迈瑞医疗',
                   '科大讯飞', '山东药玻', '牧原股份', '洽洽食品', '通策医疗', '美亚柏科', '安井食品', '韦尔股份', '中航光电', '分众传媒',
                   '芒果超媒', '长春高新', '美的集团', '温氏股份', '中国石化', '复星医药', '绝味食品', '山东黄金', '三一重工', '闻泰科技',
                   '北新建材', '万华化学', '顺鑫农业', '华兰生物', '我武生物', '光威复材', '通威股份', '扬农化工', '华鲁恒升', '双汇发展',
                   '赣锋锂业', '中公教育', '国瓷材料', '烽火通信', '沪电股份', '中科曙光', '紫金矿业', '京沪高铁', '亿联网络', '中信特钢',
                   '宇通客车', '长江电力', '金风科技', '宋城演艺', '东方财富', '隆基股份', '乐普医疗', '古井贡酒', '安图生物', '壹网壹创',
                   '恒立液压', '伊利股份', '金山办公', '中环股份', '视源股份', '国电南瑞', '顺丰控股', '启明星辰', '金域医学', '完美世界',
                   '贵州茅台', '汇顶科技', '信维通信', '高德红外', '中国软件', '中顺洁柔', '亿纬锂能', '泸州老窖', '恒生电子', '康弘药业',
                   '比亚迪', '健友股份', '三花智控', '中兴通讯', '恒瑞医药', '深信服', '吉比特', '大参林', '新希望', '家家悦',
                   '凯莱英', '广联达', '五粮液', '欣旺达', '老百姓',   '苏泊尔', '京东方A', '卓胜微']

Institutions150_1 = ['贵州茅台', '立讯精密', '长春高新', '隆基股份', '恒瑞医药', '中国中免', '宁德时代', '迈瑞医疗', '美的集团', '泸州老窖',
                    '药明康德', '东方财富', '伊利股份', '恒生电子', '三一重工', '格力电器', '芒果超媒', '亿纬锂能', '顺丰控股', '爱尔眼科',
                    '万华化学', '海康威视', '康泰生物', '山西汾酒', '通威股份', '兆易创新', '海大集团', '三安光电', '三花智控', '三七互娱',
                    '歌尔股份', '东方雨虹', '通策医疗', '智飞生物', '中兴通讯', '汇川技术', '双汇发展', '紫金矿业', '海尔智家', '金山办公',
                    '古井贡酒', '分众传媒', '美年健康', '华鲁恒升', '用友网络', '南极电商', '泰格医药', '圣邦股份', '华兰生物', '华测检测',
                    '健帆生物', '蓝思科技', '华海药业', '绝味食品', '信维通信', '洋河股份', '顺鑫农业', '海天味业', '沃森生物', '赣锋锂业',
                    '牧原股份', '北方华创', '中炬高新', '长电科技', '上海机场', '海螺水泥', '闻泰科技', '山东药玻', '宋城演艺', '星宇股份',
                    '完美世界', '金域医学', '安井食品', '中科曙光', '永辉超市', '紫光国微', '国瓷材料', '华域汽车', '卫宁健康', '安琪酵母',
                    '紫光股份', '中科创达', '浪潮信息', '太阳纸业', '中国建筑', '韦尔股份', '我武生物', '中航光电', '乐普医疗', '晨光文具',
                    '宝信软件', '中公教育', '京沪高铁', '人福医药', '涪陵榨菜', '安图生物', '东山精密', '欧普康视', '北新建材', '亿联网络',
                    '光威复材', '康龙化成', '中国巨石', '先导智能', '普洛药业', '复星医药', '中航沈飞', '益丰药房', '中国软件', '视源股份',
                    '贝达药业', '浙江鼎力', '建设机械', '云南白药', '重庆啤酒', '宏发股份', '光线传媒', '洽洽食品', '青岛啤酒', '高德红外',
                    '捷佳伟创', '生益科技', '长江电力', '恩捷股份', '风华高科', '航发动力', '英科医疗', '天赐材料', '温氏股份', '中环股份', 
                    '潍柴动力', '京东方A', '吉比特', 'TCL科技', '深信服', '比亚迪', '片仔癀', '今世缘', '新宙邦', '卓胜微', 
                    '欣旺达', '五粮液', '广联达', '凯莱英', '璞泰来', '司太立', '同花顺', '中国神华', '福斯特', '掌趣科技']

# 北上资金前50
North50 = ['牧原股份', '顺丰控股', '韦尔股份', '潍柴动力', '三七互娱', '隆基股份', '宁德时代', '东方雨虹', '华兰生物', '国电南瑞',
           '药明康德', '生物股份', '三一重工', '迈瑞医疗', '立讯精密', '汇川技术', '保利地产', '泰格医药', '恒生电子', '中信证券',
           '恒立液压', '海天味业', '海康威视', '美的集团', '伊利股份', '贵州茅台', '长江电力', '招商银行', '华测检测', '万华化学',
           '工商银行', '分众传媒', '格力电器', '中国平安', '方正证券', '恒瑞医药', '云南白药', '上海机场', '海螺水泥', '上汽集团',
           '平安银行', '海尔智家', '洋河股份', '中国中免', '兴业银行', '爱尔眼科', '京东方A', '万科A', '五粮液', '广联达', ]

ZiXuan = ['美年健康', '美亚光电', '大华股份', '宝信软件', '中科创达', '福耀玻璃', '中信建投', '上海新阳', '苏州固锝', '老板电器',
          '上海贝岭', '伟明环保', '鹏鼎控股', '中国太保', '珠江啤酒', '上峰水泥', '宏发股份', '德赛西威', '涪陵榨菜', '光线传媒',
          '中航高科', '捷捷微电', '恩捷股份', '通富微电', '三只松鼠', '良品铺子', '中国长城', '南大光电', '得润电子', '安洁科技',
          '紫光国微', '联美控股', '重庆啤酒', '福成股份', '超图软件', 'TCL科技', '士兰微', '中科软', '新洋丰', '福莱特', '同花顺',
          '科沃斯', '白云山']

Champion = ['贝瑞基因', '迪安诊断', '阳光电源', '顺网科技', '密尔克卫', '富邦股份', '金城医药', '广州酒家', '博实股份', '巨星科技',
            '安车检测', '杭叉集团', '智莱科技', '杭锅股份', '雪榕生物', '华宏科技', '苏试试验', '飞荣达', '爱柯迪', '溢多利', '康力电梯',
            '宁波银行', '紫金矿业', '凯莱英']

# 北上前50 + 机构重仓集合
Ins148_North50 = list(set(Institutions150_0 + Institutions150_1 + North50 + Champion + ZiXuan)) # 158: Institutions148 + North50
# print(len(set(Ins148_North50))) # 247

def get_all_data():
    # 获取沪深300和中证500成分股
    rs_all = bs.query_all_stock(day="2020-06-30")
    print('query_all error_code:' + rs_all.error_code)
    print('query_all  error_msg:' + rs_all.error_msg)

    # 打印结果集
    all_stocks = []
    while (rs_all.error_code == '0') & rs_all.next():
        # 获取一条记录，将记录合并在一起
        all_stocks.append(rs_all.get_row_data())

    stocks_result = pd.DataFrame(all_stocks, columns=rs_all.fields)

    # stocks_result.to_csv("./stocks-pool/all_stocks.csv", encoding="gbk", index=False)
    return stocks_result

def get_ins148_north50_data():
    # 获取沪深300和中证500成分股
    rs_all = bs.query_all_stock("2020-06-30")
    print('query_all error_code:' + rs_all.error_code)
    print('query_all  error_msg:' + rs_all.error_msg)

    # 打印结果集
    all_stocks = []
    while (rs_all.error_code == '0') & rs_all.next():
        # 获取一条记录，将记录合并在一起
        code_info = rs_all.get_row_data()
        if code_info[2] in Ins148_North50:
            all_stocks.append(code_info)

    stocks_result = pd.DataFrame(all_stocks, columns=rs_all.fields)

    # stocks_result.to_csv("./stocks-pool/ins148_north50_stocks.csv", encoding="gbk", index=False)
    return stocks_result

# 沪深300 + 中证500
def get_hs300_zz500_data():
    # 获取沪深300和中证500成分股
    rs_hs300 = bs.query_hs300_stocks()
    rs_zz500 = bs.query_zz500_stocks()
    print('query_hs300 error_code:' + rs_hs300.error_code)
    print('query_hs300  error_msg:' + rs_hs300.error_msg)
    print('query_zz500 error_code:' + rs_zz500.error_code)
    print('query_zz500  error_msg:' + rs_zz500.error_msg)

    # 打印结果集
    hs300_stocks = []
    zz500_stocks = []
    while (rs_hs300.error_code == '0') & rs_hs300.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs_hs300.get_row_data())
    while (rs_zz500.error_code == '0') & rs_zz500.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs_zz500.get_row_data())

    stocks_result = pd.DataFrame(hs300_stocks+zz500_stocks, columns=rs_hs300.fields)

    # stocks_result.to_csv("./stocks-pool/hs300_zz500_stocks.csv", encoding="gbk", index=False)
    return stocks_result

if __name__ == '__main__':
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # data = get_ins148_north50_data()
    # print(data)
    data = pd.read_csv("./stocks-pool/all_stocks.csv", encoding='gbk')
    # print(data['code_name'].values.tolist())
    for i in Institutions150_1:
        if i not in data['code_name'].values.tolist():
            print(i)

    #### 登出系统 ####
    bs.logout()