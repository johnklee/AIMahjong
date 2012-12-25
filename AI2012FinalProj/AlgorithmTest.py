#!/usr/bin/python
#-*- coding: utf-8 -*-
from Algorithm import *
from GameBoard import *


testopt = input('Give test input: ')
print("Test input='{0}'...".format(testopt))

if int(testopt) == 4:
    print("\t[Test] Test API:SearchBestWinTileCompost...")
    awang_list = []
    awang_list.append('8萬')
    awang_list.append('8萬')
    awang_list.append('3萬')
    awang_list.append('3萬')
    awang_list.append('4萬')
    awang_list.append('4萬')
    awang_list.append('4萬')
    awang_list.append('5萬')
    awang_list.append('6萬')
    print("\t[Test] Available Wang List:{0}".format(toCListStr(awang_list)))
    print("\t[Test] Total {0} possible meld composition!".format(AllMeldComstCnt('4萬', awang_list, None, None, None, None)))
elif int(testopt) == 1:
    # [1萬 2萬 7萬 7萬 |4筒 5筒 6筒 |1條 3條 ||南 南 ]
    # [8萬 ||2條 3條 4條 5條 6條 7條 ||]
    # [4萬 |7筒 |4條 4條 3條||]
    print("\t[Test] Test API:SearchBestWinTileCompost...")
    wang_list = []
    wang_list.append('4萬')
    awang_list = []
    awang_list.append('8萬')
    awang_list.append('8萬')
    awang_list.append('3萬')
    awang_list.append('3萬')
    awang_list.append('4萬')
    awang_list.append('4萬')
    awang_list.append('4萬')
    awang_list.append('5萬')
    awang_list.append('5萬')
    print("\t[Test] Wang:{0}/{1}".format(toCListStr(wang_list), toCListStr(awang_list)))

    tube_list = []
    tube_list.append('7筒')
    #tube_list.append('5筒')
    #tube_list.append('6筒')
    atube_list = []
    atube_list.append('1筒')
    atube_list.append('1筒')
    atube_list.append('2筒')
    atube_list.append('2筒')
    atube_list.append('3筒')
    atube_list.append('4筒')
    atube_list.append('5筒')
    atube_list.append('6筒')
    atube_list.append('7筒')
    atube_list.append('8筒')
    atube_list.append('9筒')
    print("\t[Test] Tube:{0}/{1}".format(toCListStr(tube_list), toCListStr(atube_list)))

    bamb_list = []
    bamb_list.append('4條')
    bamb_list.append('4條')
    bamb_list.append('3條')
    abamb_list = []
    abamb_list.append('1條')
    abamb_list.append('2條')
    abamb_list.append('3條')
    abamb_list.append('4條')
    abamb_list.append('5條')
    abamb_list.append('6條')
    abamb_list.append('7條')
    print("\t[Test] Bamb:{0}/{1}".format(toCListStr(bamb_list), toCListStr(abamb_list)))

    word_list = []
    #word_list.append('中')
    #word_list.append('中')
    #word_list.append('發')
    aword_list = []
    aword_list.append('中')
    aword_list.append('發')
    aword_list.append('發')
    aword_list.append('白')
    aword_list.append('白')
    aword_list.append('白')
    aword_list.append('白')
    print("\t[Test] Word:{0}/{1}".format(toCListStr(word_list), toCListStr(aword_list)))

    wind_list = []
    #wind_list.append('南')
    #wind_list.append('南')
    awind_list = []
    awind_list.append('南')
    awind_list.append('北')
    awind_list.append('北')
    awind_list.append('北')
    awind_list.append('東')
    awind_list.append('東')
    awind_list.append('東')
    print("\t[Test] Wind:{0}/{1}".format(toCListStr(wind_list), toCListStr(awind_list)))


    solu = SearchBestWinTileCompost(wang_list, awang_list, tube_list, atube_list, bamb_list, abamb_list, word_list, aword_list, wind_list, awind_list)
    print("\t[Test] Best Solution={0}:".format(solu[0]))
    for dt in solu[1]:
        print("\tDrop {0}".format(dt))
    for et in solu[2]:
        print("\tEat {0}".format(et))

elif int(testopt) == 2:
    print("\t[Test] Test API:SearchWinTileCompost...")
    wang_list = []
    wang_list.append('1萬')
    wang_list.append('3萬')
    awang_list = []
    awang_list.append('2萬')
    awang_list.append('2萬')
    awang_list.append('3萬')
    awang_list.append('3萬')
    awang_list.append('4萬')
    awang_list.append('4萬')
    awang_list.append('4萬')
    awang_list.append('5萬')
    awang_list.append('5萬')

    tube_list = []
    tube_list.append('2筒')
    tube_list.append('2筒')
    tube_list.append('3筒')
    atube_list = []
    atube_list.append('1筒')
    atube_list.append('1筒')
    atube_list.append('2筒')
    atube_list.append('2筒')
    atube_list.append('3筒')
    atube_list.append('4筒')

    bamb_list = []
    abamb_list = []

    word_list = []
    word_list.append('中')
    word_list.append('中')
    word_list.append('發')
    aword_list = []
    aword_list.append('中')
    aword_list.append('發')
    aword_list.append('發')
    aword_list.append('白')
    aword_list.append('白')
    aword_list.append('白')
    aword_list.append('白')

    wind_list = []
    awind_list = []
    SearchWinTileCompost(wang_list, awang_list, tube_list, atube_list, bamb_list, abamb_list, word_list, aword_list, wind_list, awind_list)

elif testopt == '3':
    print("\t[Test] Test API:SMeld1/SMeld2...")
    clist = []
    clist.append('1萬')
    clist.append('3萬')

    avail_list = []
    avail_list.append('2萬')
    avail_list.append('2萬')
    avail_list.append('3萬')
    avail_list.append('4萬')
    avail_list.append('4萬')


    clist2 = []
    clist2.append('東風')
    clist2.append('東風')
    clist2.append('西風')
    clist2.append('西風')

    avail_list2 = []
    avail_list2.append('東風')
    avail_list2.append('東風')
    avail_list2.append('西風')
    avail_list2.append('南風')

    amap = SMeld1(clist, avail_list)
    amap2 = SMeld2(clist2, avail_list2)

    print('Solution for {0}: Avail={1}'.format(toCListStr(clist), toCListStr(avail_list)))
    for vals in amap.values():
        for sol in vals:
            print("\t{0} -> {1}".format(toCListStr(sol[0]), toCListStr(sol[1])))

    print('===========================================')
    print('Solution for {0}: Avail={1}'.format(toCListStr(clist2), toCListStr(avail_list2)))
    for vals in amap2.values():
        for sol in vals:
            print("\t{0} -> {1}".format(toCListStr(sol[0]), toCListStr(sol[1])))
