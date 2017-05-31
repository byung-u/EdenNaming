#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import sqlite3

# /usr/local/lib/python3.6/site-packages/hangul_utils
from hangul_utils import hangul_len, split_syllable_char
from block_list import BLOCK_LIST


def get_last_name_info(conn, hanja):
    s = conn.cursor()
    query = 'SELECT hanja,reading,strokes,add_strokes,five_type FROM naming_hanja where hanja="%s"' % hanja
    s.execute(query)
    row = s.fetchone()
    return list(row)


# 목 -> 화 -> 토 -> 금 -> 수 -> 목 (생)
# 토 -> 목 -> 금 -> 화 -> 수 -> 토 (흉)
def check_five_type(name_type):
    # http://sajuplus.tistory.com/235
    if name_type == '木木水':  # 木
        return True
    elif name_type == '木木火':
        return True
    elif name_type == '木水木':
        return True
    elif name_type == '木水水':
        return True
    elif name_type == '木火木':
        return True
    elif name_type == '木火火':
        return True
    elif name_type == '木火土':
        return True
    elif name_type == '木水金':
        return True
    elif name_type == '木土火':
        return True
    elif name_type == '木火水':
        return True
    elif name_type == '木水火':
        return True
    elif name_type == '木木水':
        return True
    elif name_type == '火木木':  # 火
        return True
    elif name_type == '火木水':
        return True
    elif name_type == '火木火':
        return True
    elif name_type == '火火木':
        return True
    elif name_type == '火火土':
        return True
    elif name_type == '火土金':
        return True
    elif name_type == '火土火':
        return True
    elif name_type == '火土土':
        return True
    elif name_type == '火金土':
        return True
    elif name_type == '火土金':
        return True
    elif name_type == '火水木':
        return True
    elif name_type == '火木土':
        return True
    elif name_type == '土金金':  # 土
        return True
    elif name_type == '土金土':
        return True
    elif name_type == '土金水':
        return True
    elif name_type == '土火木':
        return True
    elif name_type == '土火火':
        return True
    elif name_type == '土火土':
        return True
    elif name_type == '土土金':
        return True
    elif name_type == '土土火':
        return True
    elif name_type == '土水金':
        return True
    elif name_type == '土金火':
        return True
    elif name_type == '土木火':
        return True
    elif name_type == '土火金':
        return True
    elif name_type == '土土土':
        return True
    elif name_type == '金金水':  # 金
        return True
    elif name_type == '金金土':
        return True
    elif name_type == '金水金':
        return True
    elif name_type == '金水木':
        return True
    elif name_type == '金水水':
        return True
    elif name_type == '金土金':
        return True
    elif name_type == '金土火':
        return True
    elif name_type == '金土土':
        return True
    elif name_type == '金木水':
        return True
    elif name_type == '金水土':
        return True
    elif name_type == '金火土':
        return True
    elif name_type == '金土水':
        return True
    elif name_type == '水金金':  # 水
        return True
    elif name_type == '水金水':
        return True
    elif name_type == '水金土':
        return True
    elif name_type == '水木木':
        return True
    elif name_type == '水木水':
        return True
    elif name_type == '水木火':
        return True
    elif name_type == '水水金':
        return True
    elif name_type == '水水木':
        return True
    elif name_type == '水火木':
        return True
    elif name_type == '水木金':
        return True
    elif name_type == '水土金':
        return True
    elif name_type == '水金木':
        return True
    elif name_type == '水水水':
        return True
    else:  # not in  水火土金木 rule
        return False


def check_81_suri(conn, total_strokes):
    s = conn.cursor()
    query = 'SELECT luck_type FROM naming_81 WHERE strokes=%s' % total_strokes
    for row in s.execute(query):
        if row[0].endswith('吉') is False:  # not 吉
            return False
    return True


def get_siju(iljin, hour):
    siju = [
        ["甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥"],
        ["丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥"],
        ["戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥"],
        ["庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥"],
        ["壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"],
    ]

    if iljin == '甲' or iljin == '己':
        x = 0
    elif iljin == '乙' or iljin == '庚':
        x = 1
    elif iljin == '丙' or iljin == '辛':
        x = 2
    elif iljin == '丁' or iljin == '壬':
        x = 3
    elif iljin == '戊' or iljin == '癸':
        x = 4
    else:
        print('[ERR] invalid iljin: ', iljin)
        return None

    if 23 <= hour or hour < 1:
        y = 0
    elif 1 <= hour < 3:
        y = 1
    elif 3 <= hour < 5:
        y = 2
    elif 5 <= hour < 7:
        y = 3
    elif 7 <= hour < 9:
        y = 4
    elif 9 <= hour < 11:
        y = 5
    elif 11 <= hour < 13:
        y = 6
    elif 13 <= hour < 15:
        y = 7
    elif 15 <= hour < 17:
        y = 8
    elif 17 <= hour < 19:
        y = 9
    elif 19 <= hour < 21:
        y = 10
    elif 21 <= hour < 23:
        y = 11
    else:
        print('[ERR] invalid hour: ', hour)
        return None
    return (siju[x][y])


def get_secha_wolgeon_iljin(conn, year, month, day):
    s = conn.cursor()
    query = '''
    SELECT lun_secha, lun_wolgeon, lun_iljin
    FROM gregorian_calendar
    WHERE sol_year=%s and sol_month=%s and sol_day=%s
    ''' % (year, month, day)
    s.execute(query)
    row = s.fetchone()
    return row[0], row[1], row[2]


def get_h10gan_5types(h10gan):
    if h10gan == '甲' or h10gan == '乙':
        return '木'
    elif h10gan == '丙' or h10gan == '丁':
        return '火'
    elif h10gan == '戊' or h10gan == '己':
        return '土'
    elif h10gan == '庚' or h10gan == '辛':
        return '金'
    elif h10gan == '壬' or h10gan == '癸':
        return '水'
    else:
        return None


def get_h12ji_5types(h12ji):
    if h12ji == '子' or h12ji == '亥':
        print('h12ji: ', h12ji,  '水')
        return '水'
    elif h12ji == '寅' or h12ji == '卯':
        return '木'
    elif h12ji == '巳' or h12ji == '午':
        return '火'
    elif h12ji == '辰' or h12ji == '戌' or h12ji == '丑' or h12ji == '未':
        return '土'
    elif h12ji == '申' or h12ji == '酉':
        return '金'
    else:
        return None


def get_5types(h10gan, h12ji):
    res_h10gan = get_h10gan_5types(h10gan)
    if res_h10gan is None:
        return None
    res_h12ji = get_h12ji_5types(h12ji)
    if res_h12ji is None:
        return None

    return '%s%s' % (res_h10gan, res_h12ji)


def get_energy_saju(siju_type, iljin_type, wolgeon_type, secha_type):
    energy = {
            '木': 0,
            '火': 0,
            '土': 0,
            '金': 0,
            '水': 0,
    }
    energy[siju_type[0]] += 1
    energy[siju_type[1]] += 1
    energy[iljin_type[0]] += 1
    energy[iljin_type[1]] += 1
    energy[wolgeon_type[0]] += 1
    energy[wolgeon_type[1]] += 1
    energy[secha_type[0]] += 1
    energy[secha_type[1]] += 1
    return min(energy, key=energy.get), max(energy, key=energy.get)


def get_saju(conn, birth):
    year = birth[0:4]
    month = birth[4:6]
    day = birth[6:8]
    hour = birth[8:10]
    secha, wolgeon, iljin = get_secha_wolgeon_iljin(conn, year, month, day)
    siju = get_siju(iljin[0], int(hour))  # siju : hour

    siju_type = get_5types(siju[0], siju[1])
    if siju_type is None:
        return None
    iljin_type = get_5types(iljin[0], iljin[1])
    if iljin_type is None:
        return None
    wolgeon_type = get_5types(wolgeon[0], wolgeon[1])
    if wolgeon_type is None:
        return None
    secha_type = get_5types(secha[0], secha[1])
    if secha_type is None:
        return None
    # print('[DBG1]', year, month, day, hour)
    # print('[DBG2] hour, day, month, year')
    # print('[DBG2]', siju[0], iljin[0], wolgeon[0], secha[0])
    # print('[DBG3]', siju[1], iljin[1], wolgeon[1], secha[1])
    # print('[DBG4]', siju_type[0], iljin_type[0], wolgeon_type[0], secha_type[0])
    # print('[DBG4]', siju_type[1], iljin_type[1], wolgeon_type[1], secha_type[1])

    weak, strong = get_energy_saju(siju_type, iljin_type, wolgeon_type, secha_type)
    saju = {
            'year': year, 'month': month, 'weak': weak, 'strong': strong,
            'siju': siju, 'siju_type': siju_type,
            'iljin': iljin, 'iljin_type': iljin_type,
            'wolgeon': wolgeon, 'wolgeon_type': wolgeon_type,
            'secha': secha, 'secha_type': secha_type,
    }
    return saju


def check_total_stroke(conn, last_name, m1, m2):
    t1 = get_total_strokes(last_name, m2, None)
    if check_81_suri(conn, t1) is False:  # (홍+길) 동
        return False

    t2 = get_total_strokes(m1, m2, None)
    if check_81_suri(conn, t2) is False:  # 홍 (길+동)
        return False

    t3 = get_total_strokes(last_name, m1, m2)
    if check_81_suri(conn, t3) is False:  # (홍+길+동)
        return False

    return True


def get_hangul_len(s):
    hlen = 0
    for i in range(len(s)):
        print(s[i])
        hlen += hangul_len(s[i])
    return hlen


def check_plus_minus_hangul(conn, last_name, m1, m2):
    # 홍길동 -> ㅎㄱㄷ (한글 획수 홀/짝 확인)
    s1 = hangul_len(last_name[1])
    s2 = hangul_len(m1[1])
    s3 = hangul_len(m2[1])
    if s1 % 2 == 0 and s2 % 2 == 0 and s3 % 2 == 0:
        return False
    if s1 % 2 == 1 and s2 % 2 == 1 and s3 % 2 == 1:
        return False
    return True


def check_plus_minus_hanja(conn, n1, n2, n3):
    if n1[3] is None:
        n1_strk = int(n1[2])
    else:
        n1_strk = int(n1[2]) + int(n1[3])

    if n2[3] is None:
        n2_strk = int(n2[2])
    else:
        n2_strk = int(n2[2]) + int(n2[3])

    if n3[3] is None:
        n3_strk = int(n3[2])
    else:
        n3_strk = int(n3[2]) + int(n3[3])

    if n1_strk % 2 == 0 and n2_strk % 2 == 0 and n3_strk % 2 == 0:
        return False
    if n1_strk % 2 == 1 and n2_strk % 2 == 1 and n3_strk % 2 == 1:
        return False
    return True


def check_hangul_hard_pronounce(last_name, m1, m2):
    s1 = split_syllable_char(last_name[1])
    s2 = split_syllable_char(m1[1])
    s3 = split_syllable_char(m2[1])

    if (s1[0] == s2[0] == s3[0]):  # 김구관
        return False
    elif s2[0] == s3[0]:  # 신류려
            return False

    if (s2[1] == 'ㅐ'):  # 김해선 -> 김혜선
        return False
    elif (s3[1] == 'ㅔ'):  # 김지에 -> 김지애
        return False

    if (s2[0] == s3[0]):  # 이름의 자음이 같은 경우에 모음 확인
        if (s2[1] == 'ㅜ' and s3[1] == 'ㅜ'):  # 최준주
            return False
        elif (s2[1] == 'ㅜ' and s3[1] == 'ㅠ'):  # 김주쥬
            return False
        elif (s2[1] == 'ㅗ' and s3[1] == 'ㅗ'):  # 박곤고
            return False
        elif (s2[1] == 'ㅗ' and s3[1] == 'ㅛ'):  # 박포표
            return False

    if (s2[1] == 'ㅖ' and s3[1] == 'ㅖ'):  # 이계혜
            return False
    elif (s2[1] == 'ㅖ' and s3[1] == 'ㅐ'):  # 이혜애
            return False
    elif (s2[1] == 'ㅖ' and s3[1] == 'ㅔ'):  # 이혜에
            return False

    if len(s2) == 3 and len(s3) > 1:
        if s2[2] == s3[0]:  # 김열루
            return False

    if len(s2) == 3 and len(s3) == 3:
        if (s2[1] == 'ㅕ' and s2[2] == 'ㄴ' and s3[1] == 'ㅕ' and s3[2] == 'ㄴ'):  # 최현련
            return False
        elif (s2[1] == 'ㅕ' and s2[2] == 'ㅁ' and s3[1] == 'ㅕ' and s3[2] == 'ㅇ'):  # 최겸경
            return False
        elif (s2[1] == 'ㅕ' and s2[2] == 'ㅇ' and s3[1] == 'ㅕ' and s3[2] == 'ㅇ'):  # 최영경
            return False
        elif (s2[1] == 'ㅑ' and s2[2] == 'ㅇ' and s3[1] == 'ㅕ' and s3[2] == 'ㅁ'):  # 최양념
            return False
        elif (s2[2] == 'ㄱ' and s3[2] == 'ㄱ'):  # 이혁탁
            return False
        elif (s2[2] == 'ㄴ' and s3[2] == 'ㄴ'):  # 이완린
            return False

    return True


def get_name_list(conn, last_name, m1):
    name_list = []
    s = conn.cursor()
    query = """
    SELECT hanja,reading,strokes,add_strokes,five_type
    FROM naming_hanja
    WHERE is_naming_hanja=1 AND reading
    NOT IN ('만', '병', '백', '장', '춘', '최', '충', '창', '치', '참', '천', '택', '탁', '태', '외', '사', '매', '읍', '소')
    """
    for m2 in s.execute(query):  # ('架', 9, None, '木')
        if m1[0] == m2[0]:
            continue

        name2 = '%s%s' % (m1[1], m2[1])
        try:
            if BLOCK_LIST[name2] == 1:
                continue
        except:
            pass

        name_type = '%s%s%s' % (last_name[4], m1[4], m2[4])
        # STEP 4: 오행의 배치 관계
        if check_five_type(name_type) is False:
            continue

        # STEP 2: 수리영동 조직관계
        # STEP 7: 수리 역상의 관계
        if check_total_stroke(conn, last_name, m1, m2) is False:
            continue

        # STEP 3: 음양 배열 관계
        if check_plus_minus_hangul(conn, last_name, m1, m2) is False:
            continue

        if check_plus_minus_hanja(conn, last_name, m1, m2) is False:
            continue

        # STEP 6: 음령 오행의 역상 관계
        if check_hangul_hard_pronounce(last_name, m1, m2) is False:
            continue

        temp_name = '%s%s%s' % (last_name[1], m1[1], m2[1])
        name_list.append(temp_name)

    if len(name_list) == 0:
        return None

    return name_list


def get_total_strokes(n1, n2, n3=None):
    if n1[3] is None:
        n1_strk = int(n1[2])
    else:
        n1_strk = int(n1[2]) + int(n1[3])

    if n2[3] is None:
        n2_strk = int(n2[2])
    else:
        n2_strk = int(n2[2]) + int(n2[3])

    if n3 is None:
        total_strokes = n1_strk + n2_strk
        # print(n1[2], n1[3], n2[2], n2[3], '---> ', total_strokes)
    else:
        if n3[3] is None:
            n3_strk = int(n3[2])
        else:
            n3_strk = int(n3[2]) + int(n3[3])
        total_strokes = n1_strk + n2_strk + n3_strk
        # print(n1[2], n1[3], n2[2], n2[3], n3[2], n3[3], '-> ', total_strokes)
    return total_strokes


"""
▣ 사주에 ‘木’이 3개이상 있을때는 ‘火’ 또는 ‘金’에 해당하는 글자로 작명합니다.
▣ 사주에 ‘土’가 3개이상 있을때는 ‘金’ 또는 ‘木’에 해당하는 글자로 작명합니다.
▣ 사주에 ‘火’가 3개이상 있을때는 ‘土’ 또는 ‘水’에 해당하는 글자로 작명합니다.
▣ 사주에 ‘金’이 3개이상 있을때는 ‘水’ 또는 ‘火’에 해당하는 글자로 작명합니다.
▣ 사주에 ‘水’가 3개이상 있을때는 ‘木’ 또는 ‘土’에 해당하는 글자로 작명합니다.
   if strong == '木' and row[4] == '火':
       return True
   elif strong == '木' and row[4] == '金':
       return True
   elif strong == '土' and row[4] == '金':
       return True
   elif strong == '土' and row[4] == '木':
       return True
   elif strong == '火' and row[4] == '土':
       return True
   elif strong == '火' and row[4] == '水':
       return True
   elif strong == '金' and row[4] == '水':
       return True
   elif strong == '金' and row[4] == '火':
       return True
   elif strong == '水' and row[4] == '木':
       return True
   elif strong == '水' and row[4] == '土':
       return True
   else:
       return False
"""


def type_check_with_month(saju, row):
    strong = saju['strong']
    month = saju['month']
    # 木火土金水
    if month == '01' or month == '02' or month == '03':
        if strong == '木' and row[4] == '木':
            return False
        elif strong == '木' and row[4] == '水':
            return False
        elif strong == '火' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '火':
            return False
        elif strong == '土' and row[4] == '水':
            return False
        elif strong == '土' and row[4] == '木':
            return False
        elif strong == '金' and row[4] == '木':
            return False
        elif strong == '金' and row[4] == '水':
            return False
        elif strong == '水' and row[4] == '水':
            return False
        elif strong == '水' and row[4] == '金':
            return False
    elif month == '04' or month == '05' or month == '06':
        if strong == '木' and row[4] == '火':
            return False
        elif strong == '木' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '土':
            return False
        elif strong == '火' and row[4] == '木':
            return False
        elif strong == '土' and row[4] == '火':
            return False
        elif strong == '土' and row[4] == '土':
            return False
        elif strong == '金' and row[4] == '火':
            return False
        elif strong == '金' and row[4] == '木':
            return False
        elif strong == '水' and row[4] == '火':
            return False
        elif strong == '水' and row[4] == '木':
            return False
    elif month == '07' or month == '08' or month == '09':
        if strong == '木' and row[4] == '金':
            return False
        elif strong == '木' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '金':
            return False
        elif strong == '火' and row[4] == '土':
            return False
        elif strong == '土' and row[4] == '金':
            return False
        elif strong == '土' and row[4] == '水':
            return False
        elif strong == '金' and row[4] == '金':
            return False
        elif strong == '金' and row[4] == '土':
            return False
        elif strong == '水' and row[4] == '水':
            return False
        elif strong == '水' and row[4] == '金':
            return False
    elif month == '10' or month == '11' or month == '12':
        if strong == '木' and row[4] == '水':
            return False
        elif strong == '木' and row[4] == '木':
            return False
        elif strong == '火' and row[4] == '水':
            return False
        elif strong == '火' and row[4] == '金':
            return False
        elif strong == '土' and row[4] == '水':
            return False
        elif strong == '土' and row[4] == '金':
            return False
        elif strong == '金' and row[4] == '水':
            return False
        elif strong == '金' and row[4] == '木':
            return False
        elif strong == '水' and row[4] == '金':
            return False
        elif strong == '水' and row[4] == '水':
            return False

    return True


def main():
    start_time = time.time()  # START
    conn = sqlite3.connect('naming_korean.db')

    # TEST data
    birth = '200203010501'  # '200203011201'
    hanja = "金"  # 菊 李

    # 성씨 정보
    last_name = get_last_name_info(conn, hanja)
    if last_name[1] == '리':
        last_name[1] = '이'
    elif last_name[1] == '로':
        last_name[1] = '노'
    elif last_name[1] == '금':
        last_name[1] = '김'
    elif last_name[1] == '림':
        last_name[1] = '임'

    # STEP 1: 선천명과의 합국 조화 관계
    saju = get_saju(conn, birth)
    if saju is None:
        print('get saju failed')
        return

    s = conn.cursor()
    # query = 'SELECT hanja,reading,strokes,add_strokes,five_type FROM naming_hanja;'
    # STEP 8: 어휘 어감의 조정 관계
    query = """
    SELECT hanja,reading,strokes,add_strokes,five_type
    FROM naming_hanja
    WHERE is_naming_hanja=1
    AND reading
    NOT IN ('각', '과', '국', '니', '렴', '렬', '린', '랑', '려', '령', '락',
    '량', '련', '목', '복', '애', '엄', '열', '오', '요', '왕', '욱', '읍',
    '빈', '표', '필', '탁', '회', '후', '흠')
    """
    total_list = 0
    for row in s.execute(query):  # ('架', 9, None, '木')
        name1 = '%s%s' % (last_name[1], row[1])
        try:
            if BLOCK_LIST[name1] == 1:
                continue
        except:
            pass
        name_list = get_name_list(conn, last_name, row)
        if name_list is None:
            continue
        print(name_list)
        total_list += len(name_list)

    print("--- %s seconds ---" % (time.time() - start_time))  # END
    print('Total: ', total_list)
    conn.close()  # db close
    return


"""
[o] 1: 선천명과의 합국 조화 관계
[o] 2: 수리영동 조직관계
[o] 7: 수리 역상의 관계
[o] 3: 음양 배열 관계
[o] 4: 오행의 배치 관계
[o] 8: 어휘 어감의 조정 관계
[o] 6: 음령 오행의 역상 관계

[o] 5: 자의 정신 관계
"""


if __name__ == '__main__':
    main()
