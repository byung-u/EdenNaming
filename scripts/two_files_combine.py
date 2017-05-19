#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    file1 = 'dump'   # <option value="145">
    file2 = 'dump2'  # 昌
    # combine with zip:  <option value="145">昌
    with open(file1) as f1, open(file2) as f2, open("combined_data", "w") as fout:
        for t in zip(f1, f2):
            fout.write(''.join(x.strip() for x in t)+'\n')


if __name__ == '__main__':
    main()
