# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlite3
import re

from .get_name import get_name, get_suri_hanja


def get_location(location_idx):
    locations = {
        1: '강원도', 2: '경기도', 3: '광주시', 4: '대구시', 5: '대전시',
        6: '부산시', 7: '서울시', 8: '세종시', 9: '울산시',
        10: '인천시', 11: '제주도', 12: '경상남도', 13: '경상북도',
        14: '전라남도', 15: '전라북도', 16: '충청남도', 17: '충청북도',
    }
    print(locations[location_idx])
    # TODO: 지역별 위도가 몇분 차이나므로 그 부분을 계산 할지 확인


def get_gender(gender_idx):
    gender = {
        1: '남자', 2: '여자'
    }
    print(gender[gender_idx])
    # TODO: 남녀 이름 구별


def get_birth_order(birth_order_idx):
    birth_order = {
        1: '첫째', 2: '둘째, 이후'
    }
    print(birth_order[birth_order_idx])
    # TODO: 불용한자 확인


def get_lastname(info):
    conn = sqlite3.connect('naming_korean.db')
    query = 'SELECT * FROM last_name where id=%d' % (info)
    c = conn.cursor()
    c.execute(query)
    row = c.fetchone()
    conn.close()
    return row[1]


def get_new_korean_name(gender, location, last_name, birth_datetime):
    # print('---------------------')
    # print(location)
    # print(gender)
    # print(birth_order)
    # print(birth_datetime)
    # print(last_name)
    # print('---------------------')
    # get_location(location)
    # get_gender(gender)
    # get_birth_order(birth_order)
    r = re.compile('[-: ]')
    birth = ''.join(r.split(birth_datetime))
    l = get_lastname(last_name)
    print(l)
    print(birth)
    result_name, flag = get_name(birth, l, gender)
    # print(result_name)
    # print('---------------------')
    return result_name, flag


def get_hanja_name(name):
    hanja1 = []
    hanja2 = []
    hanja3 = []
    conn = sqlite3.connect('naming_korean.db')
    c = conn.cursor()
    # query = 'select chinese_char from naming_baby where id=5624'

    query = '''
    SELECT naming_hanja.hanja, naming_hanja.pronunciations, naming_hanja.reading, last_name.hanja
    FROM naming_hanja
    INNER JOIN last_name ON naming_hanja.hanja = last_name.hanja
    WHERE naming_hanja.reading = "%s"
    ''' % name[0]
    for row in c.execute(query):
        hanja = row[0]
        pronounce = row[1]
        hanja = '%s %s' % (hanja.replace('\'', ''), pronounce.replace('\'', ''))
        hanja1.append(hanja)

    query = '''
    SELECT DISTINCT hanja,pronunciations
    FROM naming_hanja
    WHERE reading="%s" AND NOT pronunciations="|"
    ORDER BY pronunciations''' % name[1]
    for row in c.execute(query):
        hanja = row[0]
        pronounce = row[1]
        hanja = '%s %s' % (hanja.replace('\'', ''), pronounce.replace('\'', ''))
        hanja2.append(hanja)

    query = '''
    SELECT DISTINCT hanja,pronunciations
    FROM naming_hanja
    WHERE reading="%s" AND NOT pronunciations="|"
    ORDER BY pronunciations''' % name[2]
    for row in c.execute(query):
        hanja = row[0]
        pronounce = row[1]
        hanja = '%s %s' % (hanja.replace('\'', ''), pronounce.replace('\'', ''))
        hanja3.append(hanja)

    return hanja1, hanja2, hanja3


def get_your_luck(name, h1, h2, h3):
    conn = sqlite3.connect('naming_korean.db')
    hanja = '%s%s%s' % (h1, h2, h3)
    suri_hanja = get_suri_hanja(conn, hanja)

    your_luck = """
    <table class="table">
    <thead>
        <th class="col-xs-2"> 성명 </th>
        <th class="col-xs-10"> <strong style="font-size: 30px;">%s ( %s %s %s) </strong> </th>
    </thead>
    <tbody style='height:5px;'>
        <tr>
            <td> 획수음양 </td>
            <td> <mark>%s%s%s</mark> 음양이 고루섞여서 吉합니다.</td>
        </tr>
        <tr>
            <td> 수리사격 </td>
            <td> 元<small>(초년운), %s 획 <mark>%s</mark><br> - %s </small><br>
             亨<small>(중년운), %s 획 <mark>%s</mark><br> - %s </small><br>
             利<small>(장년운), %s 획 <mark>%s</mark><br> - %s </small><br>
             貞<small>(말년운), %s 획 <mark>%s</mark><br> - %s </small></td>
        </tr>
    </tbody>
</table>
</div>
""" % (name, h1, h2, h3,
       suri_hanja[0], suri_hanja[1], suri_hanja[2],
       suri_hanja[3], suri_hanja[4], suri_hanja[5],
       suri_hanja[6], suri_hanja[7], suri_hanja[8],
       suri_hanja[9], suri_hanja[10], suri_hanja[11],
       suri_hanja[12], suri_hanja[13], suri_hanja[14],
       )

    return your_luck
