#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


def get_rsc_type(conn):

    fw = open('resource_type', 'w')
    for i in range(77, 91):
        url = 'http://sajuplus.tistory.com/%d' % i
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        r = urlopen(req)
        soup = BeautifulSoup(r, 'html.parser')
        temp = []
        for table in soup.findAll('table')[0].findAll('tr'):
            for idx, td in enumerate(table.find_all('td')):
                if idx % 8 == 2:
                    temp.append(td.text)
                    # print([idx], td.text)
                elif idx % 8 == 6:
                    temp.append(td.text)
                    # print([idx], td.text)
                    line = "'%s', '%s'\n" % (temp[0], temp[1])
                    fw.write(line)
                    del temp[:]
    fw.close()


def main():

    conn = sqlite3.connect('naming_korean.db')

    get_rsc_type(conn)

    conn.close()  # sqlite3 close


if __name__ == '__main__':
    main()
