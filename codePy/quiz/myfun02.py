def extract_cond(cond):
    if 'boy' in cond:
        cond.remove('boy')
        sex = 1
        sex_text = '限男生'
    elif 'girl' in cond:
        cond.remove('girl')
        sex = 2
        sex_text = '限女生'
    elif 'all_sex' in cond:
        cond.remove('all_sex')
        sex = 3
        sex_text = '男女皆可(不限)'
    else:
        sex = 3
        sex_text = '男女皆可(不限)'
    result = {'cond':cond, 'sex':sex, 'sex_text':sex_text}
    return result



# --------------------------------------------------
# create meta_location
def extract_location(req_raw):
    result01 = {x:req_raw[x] for x in req_raw.keys() & {'regionid', 'region_name'}}
    result02 = {x:req_raw[x] for x in req_raw.keys() & {'streetid', 'street_name','regionid', 'region_name'}}
    result03 = {x:req_raw[x] for x in req_raw.keys() & {'sectionid', 'section_name','regionid', 'region_name'}}
    result = {'region':result01, 'street':result02, 'section':result03}
    return result


# --------------------------------------------------
# clean data for cathay_search
def extarct_sex(condition):
    if 'boy' in condition:
        result = 1,
    elif 'girl' in condition:
        result = 2
    else:
        result = 3
    return result



def raw_cathay(raw):
    renter = raw['nick_name'].split(' ')
    cond = raw['condition'].split(',')
    
    # remove element
    raw.pop('nick_name')
    raw.pop('condition')
    
    # 出租者身分, 出租者(姓氏, 稱謂)
    raw['renter'] = {
        'renter_role': renter[0],
        'renter_fname': renter[1][0:1],
        'renter_title': renter[1][1:],
    }
    raw['sex'] = extarct_sex(cond)
    return raw


# --------------------------------------------------
# clean data for my_search
def raw_my(raw):
    renter = raw['nick_name'].split(' ')
    cond = extract_cond(raw['condition'].split(','))
    
    # 出租者身分, 出租者(姓氏, 稱謂)
    raw['renter'] = {
        'renter_role': renter[0],
        'renter_fname': renter[1][0:1],
        'renter_title': renter[1][1:],
    }
    raw['price'] = int(raw['price'].replace(',', ''))
    raw['living'] = raw['living'].split(',')
    raw['condition'] = cond['cond']
    raw['sex'] = cond['sex']
    
    # remove element
    raw.pop('nick_name')
    return raw



# global variable
global meta_kind, meta_shape, meta_condition, meta_living

meta_kind = {
    "0": "不限",
    "1": "整層住家",
    "2": "獨立套房",
    "3": "分租套房",
    "4": "雅房",
}

meta_shape = {
    "1": "公寓",
    "2": "電梯大樓",
    "3": "透天厝",
    "4": "別墅",
}

meta_condition = {
    'cook': '可開火',
    'cartplace': '有車位',
    'balcony_0': '沒有陽台',
    'pet': '可養寵物',
    'trabus': '有公車',
    'lease': '可短期租賃',
    'balcony_1': '有陽台',
    'lift': '有電梯',
    'tv': '電視',
    'cold': '冷氣',
    'icebox': '冰箱',
    'hotwater': '熱水器',
    'naturalgas': '天然瓦斯',
    'four': '第四台',
    'broadband': '網路',
    'washer': '洗衣機',
    'bed': '床',
    'wardrobe': '衣櫃',
    'sofa': '沙發',
    'bookTable': '桌子',
    'chair': '椅子',
}

meta_living = {
    'depart': '百貨公司',
    'advstore': '進便利商店',
    'market': '傳統市場',
    'night': '夜市',
    'park': '公園綠地',
    'school': '學校',
    'hospital': '醫療機構',
}


def trans_kind(x):
    try:
        result = meta_kind[str(x)]
    except:
        result = str(x)
    return result


def trans_shape(x):
    try:
        result = meta_shape[str(x)]
    except:
        result = str(x)
    return result


def trans_condition(x):
    try:
        result = meta_condition[str(x)]
    except:
        result = str(x)
    return result


def trans_living(x):
    try:
        result = meta_living[str(x)]
    except:
        result = str(x)
    return result


from datetime import datetime
import re
def raw_meta(raw):
    renter = raw['nick_name'].split(' ')
    cond = extract_cond(raw['condition'].split(','))
    
    # 出租者身分, 出租者(姓氏, 稱謂)
    raw['renter'] = {
        'renter_role': renter[0],
        'renter_fname': renter[1][0:1],
        'renter_title': renter[1][1:],
    }
    raw['updatetime'] = str(datetime.fromtimestamp(raw['updatetime']))
    raw['refreshtime'] = str(datetime.fromtimestamp(raw['refreshtime']))
    raw['cover'] = re.sub('[0-9]{3}x[0-9]{3}.crop', '800x600.water3', raw['cover'])
    raw['price'] = str(raw['price']).replace(',', '') + ' ' + raw['unit']
    raw['kind'] = trans_kind(raw['kind'])
    raw['shape'] = trans_shape(raw['shape'])
    raw['living'] = [trans_living(x) for x in raw['living'].split(',')]
    raw['condition'] = [trans_condition(x) for x in cond['cond']]
    raw['sex'] = cond['sex_text']
    
    # remove element
    raw.pop('nick_name')
    raw.pop('unit')
    
    return raw

