#-*- coding: utf-8 -*-
from __future__ import print_function
from GameBoard import *
import re

MAX_MELD_SEARCH_DEPTH = 2 # Setup maximum completed meld search depth.
addPtn = re.compile("add (.*)")
switchPtn = re.compile("switch (.*) to (.*)")
drpPtn = re.compile("drop (.*)")

def AllMeldComstCnt(tile, awang_list=[], atube_list=[], abamb_list=[], aword_list=[], awind_list=[], unique=False):
    """Look all possible meld composition
    This API will return all possible meld composition count including eye.
    * Argument 
      tile - Check tile
      awang_list - Available wang list
      atube_list - Available tube list
      abamb_list - Available bamb list
      aword_list - Available word list
      awind_list - Available wind list
      unique - True to unique the composition; False otherwise.
    * Return
      Count of all possible meld count.
    """
    ct = GameBoard.CardType(tile)
    if ct == 1:
        cnt = 0
        comstSet = set()
        if awang_list.count(tile) > 0:            
            comstSet.add("[{0},{0}]".format(tile))
            cnt+=1
            #print("\t[Test] Eye({0:s},{0:s})-{1}".format(tile, cnt)) 
        awang_list.sort()        
        for t1 in awang_list:
            cwang_list = awang_list[:]
            cwang_list.remove(t1)
            for t2 in cwang_list:
                clist = []
                clist.append(tile)
                clist.append(t1)
                clist.append(t2)
                if MeldDone(clist):
                    clist.sort()         
                    if not toCListStr(clist) in  comstSet:
                        if t1 == t2:
                            cnt+=1
                        else:
                            cnt+=min(awang_list.count(t1), awang_list.count(t2))                                            
                    comstSet.add(toCListStr(clist))                                        
                    #print("\t[Test] {0}-{1}".format(toCListStr(clist), cnt))
        return len(comstSet) if unique else cnt     
    elif ct == 2:
        cnt = 0
        comstSet = set()
        if atube_list.count(tile) > 0:
            comstSet.add("[{0},{0}]".format(tile)) 
            cnt+=1
        atube_list.sort()
        for t1 in atube_list:
            c_list = atube_list[:]
            c_list.remove(t1)
            for t2 in c_list:
                alist = []
                alist.append(tile)
                alist.append(t1)
                alist.append(t2)
                if MeldDone(alist):
                    alist.sort()         
                    if not toCListStr(alist) in  comstSet:
                        if t1 == t2:
                            cnt+=1
                        else:
                            cnt+=min(awang_list.count(t1), awang_list.count(t2))                                            
                    comstSet.add(toCListStr(alist))
        return len(comstSet) if unique else cnt    
    elif ct == 3:
        cnt = 0
        comstSet = set()
        if abamb_list.count(tile) > 0:
            comstSet.add("[{0},{0}]".format(tile))  
            cnt+=1
        abamb_list.sort()
        for t1 in abamb_list:
            c_list = abamb_list[:]
            c_list.remove(t1)
            for t2 in c_list:
                alist = []
                alist.append(tile)
                alist.append(t1)
                alist.append(t2)
                if MeldDone(alist):
                    alist.sort()         
                    if not toCListStr(alist) in  comstSet:
                        if t1 == t2:
                            cnt+=1
                        else:
                            cnt+=min(awang_list.count(t1), awang_list.count(t2))                                            
                    comstSet.add(toCListStr(alist))
        return len(comstSet) if unique else cnt    
    elif ct == 4:
        cnt=0
        if aword_list.count(tile) == 1: cnt+=1
        elif aword_list.count(tile) > 1: cnt+=2
        return cnt
    elif ct == 5:
        cnt=0
        if awind_list.count(tile) == 1: cnt+=1
        elif aword_list.count(tile) > 1: cnt+=2
        return cnt
    return 0

def _SearchTileCount(tile, wang_list, tube_list, bamb_list, word_list, wind_list):
    """ Search Tile Count. (找某張牌在手上牌組出現的次數)
    * Argument
      tile - Tile/Card to count.
      wang_list - Wang list to search.
      tube_list - Tube list to search.
      bamb_list - Bamb list to search.
      word_list - Word list to search.
      wind_list - Wind list to search.
    * Return
      Number of count."""
    ct = GameBoard.CardType(tile)
    if ct == 1:
        return wang_list.count(tile)
    elif ct == 2:
        return tube_list.count(tile)
    elif ct == 3:
        return bamb_list.count(tile)
    elif ct == 4:
        return word_list.count(tile)
    else:
        return wind_list.count(tile)


def calculatePWTileCnt(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp, actions):
    curPWTC = 0
    for act in actions:
        needTile = None
        mth = drpPtn.search(act)
        if mth: continue
        mth = addPtn.search(act)
        if mth:
            needTile = mth.group(1)
        else:
            mth = switchPtn.search(act)
            if mth:
                needTile = mth.group(2)
            else:
                continue
        #print("\t[Test] Need tile={0}...".format(needTile), end='')
        ct = GameBoard.CardType(needTile)
        if ct == 1:
            pwang_cp.remove(needTile)
            tcurPWTC = len(GameBoard.PreWinTiles2(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp))
            if tcurPWTC > curPWTC: curPWTC = tcurPWTC
            pwang_cp.append(needTile)
        elif ct == 2:
            ptube_cp.remove(needTile)
            tcurPWTC = len(GameBoard.PreWinTiles2(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp))
            if tcurPWTC > curPWTC: curPWTC = tcurPWTC
            ptube_cp.append(needTile)
        elif ct == 3:
            if not needTile in pbamb_cp:
                print("\t[Error] {0} not in {1}!".format(needTile, toCListStr(pbamb_cp)))
            pbamb_cp.remove(needTile)
            tcurPWTC = len(GameBoard.PreWinTiles2(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp))
            if tcurPWTC > curPWTC: curPWTC = tcurPWTC
            pbamb_cp.append(needTile)
        elif ct == 4:
            pword_cp.remove(needTile)
            tcurPWTC = len(GameBoard.PreWinTiles2(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp))
            if tcurPWTC > curPWTC: curPWTC = tcurPWTC
            pword_cp.append(needTile)
        elif ct == 5:
            pwind_cp.remove(needTile)
            tcurPWTC = len(GameBoard.PreWinTiles2(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp))
            if tcurPWTC > curPWTC: curPWTC = tcurPWTC
            pwind_cp.append(needTile)
        #print("{1} with PreWin Tile Count={0}...".format(pcardForm, curPWTC))
        return curPWTC

def SearchBestWinTileCompost(wang_list, awang_list,
                             tube_list, atube_list,
                             bamb_list, abamb_list,
                             word_list, aword_list,
                             wind_list, awind_list, debug=False):
    """ Search Best Win Tile Composition.
    This API will look for best win tile composition based on given card lists in hand.
    Below are the evaluation condition:
    1. Minimum actions taken to reach goal state.(Add/Drop/Switch cards)
    2. Maximum available cards to draw.
    
    * Argument:
      wang_list - Wang card list in hand
      awang_list - Available wang card list
      tube_list - Tube card list in hand
      atube_list - Available tube card list
      bamb_list - Bamb card list in hand
      abamb_list - Available bamb card list
      word_list - Word card list in hand
      aword_list - Available word card list
      wind_list - Wind card list in hand
      awind_list - Available wind card list
      debug - Debug flag. Trun to turn on debug message; False to turn off debug message.
    * Return:
      Tuple(Tile/Card Composition, Drop card suggestion list, Eat card suggestion list)"""
    origMeldCnt = (len(wang_list)+len(tube_list)+len(bamb_list)+len(word_list)+len(wind_list))/3
    if debug: print("\t[Test] Original Meld Count={0}...".format(origMeldCnt))
    if debug: print("\t[Test] Original Tiles:")
    if debug: print("\tWang={0}:{1}".format(toCListStr(wang_list), toCListStr(awang_list)))
    if debug: print("\tTube={0}:{1}".format(toCListStr(tube_list), toCListStr(atube_list)))
    if debug: print("\tBamb={0}:{1}".format(toCListStr(bamb_list), toCListStr(abamb_list)))
    if debug: print("\tWord={0}:{1}".format(toCListStr(word_list), toCListStr(aword_list)))
    if debug: print("\tWind={0}:{1}".format(toCListStr(wind_list), toCListStr(awind_list)))
    
    wang_solMap = SMeld1(wang_list, awang_list)
    if not wang_solMap:
        if debug: print("\t[Info] No suggest solution for wang list!")
        return
    tube_solMap = SMeld1(tube_list, atube_list)
    if not tube_solMap:
        if debug: print("\t[Info] No suggest solution for tube list!")
        return
    bamb_solMap = SMeld1(bamb_list, abamb_list)
    if not bamb_solMap:
        if debug: print("\t[Info] No suggest solution for bamboo list!")
        return
    word_solMap = SMeld2(word_list, aword_list)
    if not word_solMap:
        if debug: print("\t[Info] No suggest solution for word list!")
        return
    wind_solMap = SMeld2(wind_list, awind_list)
    if not wind_solMap:
        if debug: print("\t[Info] No suggest solution for wind list!")
        return

    soluMap = {}
    tmc = -1
    minCost = -1
    pcurWTC = -1
    pwang_cp = None
    ptube_cp = None
    pbamb_cp = None
    pword_cp = None
    pwind_cp = None
    pcardForm = None
    #addPtn = re.compile("add (.*)")
    #switchPtn = re.compile("switch (.*) to (.*)")
    #drpPtn = re.compile("drop (.*)")
    for wang_cp in wang_solMap.keys():  # wang loop
        hasEye = wang_solMap.get(wang_cp)[0][2]
        mc = len(wang_cp[1:len(wang_cp)-1].split(','))/3
        ac = len(wang_solMap.get(wang_cp)[0][1])
        #print('\t[Test] {0}/{1}/{2}...'.format(toCListStr(wang_solMap.get(wang_cp)[0][0]), mc, ac))
        for tube_cp in tube_solMap.keys(): # tube loop
            hasEye2 = tube_solMap.get(tube_cp)[0][2]
            if hasEye and hasEye2: continue
            tmc = len(tube_cp[1:len(tube_cp)-1].split(','))/3
            if (mc+tmc) > origMeldCnt: continue
            mc2 = mc + tmc
            ac2 = len(tube_solMap.get(tube_cp)[0][1])+ac
            hasEye2 = hasEye or hasEye2
            #print('\t[Test] {0}/{1}/{2}...'.format(toCListStr(tube_solMap.get(tube_cp)[0][0]), mc2, ac2))
            for bamb_cp in bamb_solMap.keys(): # bamb loop
                hasEye3 = bamb_solMap.get(bamb_cp)[0][2]
                if hasEye2 and hasEye3: continue
                tmc = len(bamb_cp[1:len(bamb_cp)-1].split(','))/3
                if (mc2+tmc) > origMeldCnt: continue
                mc3 = mc2+tmc
                ac3 = len(bamb_solMap.get(bamb_cp)[0][1])+ac2
                hasEye3 = hasEye2 or hasEye3
                #print("\t[Test] {0}/{1}/{2}...".format(toCListStr(bamb_solMap.get(bamb_cp)[0][0]), mc3, ac3))
                for word_cp in word_solMap.keys(): # word loop
                    hasEye4 = word_solMap.get(word_cp)[0][2]
                    if hasEye3 and hasEye4: continue                    
                    tmc = len(word_cp[1:len(word_cp)-1].split(','))/3
                    if (mc3+tmc) > origMeldCnt: continue                    
                    mc4 = mc3+tmc
                    ac4 = len(word_solMap.get(word_cp)[0][1])+ac3
                    hasEye4 = hasEye3 or hasEye4
                    for wind_cp in wind_solMap.keys(): # wind loop
                        if hasEye4 == wind_solMap.get(wind_cp)[0][2]: continue
                        tmc = len(wind_cp[1:len(wind_cp)-1].split(','))/3
                        if (mc4+tmc) != origMeldCnt: continue
                        cardForm = "{0}/{1}/{2}/{3}/{4}".format(toCListStr(wang_solMap.get(wang_cp)[0][0]),\
                                                                toCListStr(tube_solMap.get(tube_cp)[0][0]),\
                                                                toCListStr(bamb_solMap.get(bamb_cp)[0][0]),\
                                                                toCListStr(word_solMap.get(word_cp)[0][0]),\
                                                                toCListStr(wind_solMap.get(wind_cp)[0][0]))
                        ac5 = ac4 + len(wind_solMap.get(wind_cp)[0][1])
                        if ac5 == 0:
                            continue
                        # Keep shortest path target
                        if minCost == -1:
                            actions = []
                            actions.extend(wang_solMap.get(wang_cp)[0][1])
                            pwang_cp = wang_solMap.get(wang_cp)[0][0]
                            actions.extend(tube_solMap.get(tube_cp)[0][1])
                            ptube_cp = tube_solMap.get(tube_cp)[0][0]
                            actions.extend(bamb_solMap.get(bamb_cp)[0][1])
                            pbamb_cp = bamb_solMap.get(bamb_cp)[0][0]
                            actions.extend(word_solMap.get(word_cp)[0][1])
                            pword_cp = word_solMap.get(word_cp)[0][0]
                            actions.extend(wind_solMap.get(wind_cp)[0][1])
                            pwind_cp = wind_solMap.get(wind_cp)[0][0]
                            soluMap[cardForm] = actions
                            pcardForm = cardForm
                            minCost = ac5
                            pcurWTC = calculatePWTileCnt(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp, actions)
                        elif minCost > ac5:
                            actions = []
                            actions.extend(wang_solMap.get(wang_cp)[0][1])
                            pwang_cp = wang_solMap.get(wang_cp)[0][0]
                            actions.extend(tube_solMap.get(tube_cp)[0][1])
                            ptube_cp = tube_solMap.get(tube_cp)[0][0]
                            actions.extend(bamb_solMap.get(bamb_cp)[0][1])
                            pbamb_cp = bamb_solMap.get(bamb_cp)[0][0]
                            actions.extend(word_solMap.get(word_cp)[0][1])
                            pword_cp = word_solMap.get(word_cp)[0][0]
                            actions.extend(wind_solMap.get(wind_cp)[0][1])
                            pwind_cp = wind_solMap.get(wind_cp)[0][0]
                            soluMap.clear()
                            soluMap[cardForm] = actions
                            pcardForm = cardForm
                            minCost = ac5
                            pcurWTC = calculatePWTileCnt(pwang_cp, ptube_cp, pbamb_cp, pword_cp, pwind_cp, actions)
                        elif minCost == ac5:
                            nowWTC = 0
                            actions = []
                            actions.extend(wang_solMap.get(wang_cp)[0][1])
                            actions.extend(tube_solMap.get(tube_cp)[0][1])
                            actions.extend(bamb_solMap.get(bamb_cp)[0][1])
                            actions.extend(word_solMap.get(word_cp)[0][1])
                            actions.extend(wind_solMap.get(wind_cp)[0][1])
                            nowWTC = calculatePWTileCnt(wang_solMap.get(wang_cp)[0][0],
                                                        tube_solMap.get(tube_cp)[0][0],
                                                        bamb_solMap.get(bamb_cp)[0][0],
                                                        word_solMap.get(word_cp)[0][0],
                                                        wind_solMap.get(wind_cp)[0][0],
                                                        actions)
                            if nowWTC > pcurWTC:
                                #print("\t[Info] Change:")
                                #print("\t{0} to {1}".format(pcardForm, cardForm))
                                soluMap[cardForm] = actions
                                pcardForm = cardForm
                                pcurWTC = nowWTC
                            
    #2. Figure out the solution which has more possibility to get the required tiles
    if len(soluMap) == 0: return None
    #addPtn = re.compile("add (.*)")
    #switchPtn = re.compile("switch (.*) to (.*)")
    #drpPtn = re.compile("drop (.*)")
    tileAva = -1
    tileForm = ''
    eatList = []
    drpList = []
    teatList = []
    tdrpList = []
    # Keep target with most available tiles.
    for key in soluMap.keys():
        del teatList[:]
        del tdrpList[:]
        tc = 0
        #print("\t[Test] Calculate available tiles for {0}...".format(key), end='')
        actions = soluMap[key]    
        for act in actions:
            mth = addPtn.search(act)
            if mth:
                teatList.append(mth.group(1))
                tc += _SearchTileCount(mth.group(1), awang_list , atube_list, abamb_list, aword_list, awind_list)                
                continue
            mth = switchPtn.search(act)
            if mth:
                tdrpList.append(mth.group(1))
                teatList.append(mth.group(2))
                tc += _SearchTileCount(mth.group(2), awang_list , atube_list, abamb_list, aword_list, awind_list)                
                continue
            mth = drpPtn.search(act)
            if mth:
                tdrpList.append(mth.group(1))                
                continue
            
        if tc > tileAva:
            tileForm = key
            tileAva = tc
            del eatList[:]
            del drpList[:]
            eatList.extend(teatList)
            drpList.extend(tdrpList)
    return (tileForm, drpList, eatList)

# BD: Search Win Tile Composition
# Return: Map - Key as Card Composition ; Value as how may actions to reach target. 
def SearchWinTileCompost(wang_list, awang_list,
                         tube_list, atube_list,
                         bamb_list, abamb_list,
                         word_list, aword_list,
                         wind_list, awind_list):
    """ Search all possible win tile composition.
    This API will search all possible win tile composition with least actions to take.
    * Argument:
      wang_list - Wang card list in hand
      awang_list - Available wang card list
      tube_list - Tube card list in hand
      atube_list - Available tube card list
      bamb_list - Bamb card list in hand
      abamb_list - Available bamb card list
      word_list - Word card list in hand
      aword_list - Available word card list
      wind_list - Wind card list in hand
      awind_list - Available wind card list
    * Return:
      Map - Key as win tile composition; Value as action list to reach the goal win tile composition."""
    origMeldCnt = (len(wang_list)+len(tube_list)+len(bamb_list)+len(word_list)+len(wind_list))/3
    print("\t[Test] Original Meld Count={0}...".format(origMeldCnt))
    print("\t[Test] Original Tiles:")
    print("\tWang={0}:{1}".format(toCListStr(wang_list), toCListStr(awang_list)))
    print("\tTube={0}:{1}".format(toCListStr(tube_list), toCListStr(atube_list)))
    print("\tBamb={0}:{1}".format(toCListStr(bamb_list), toCListStr(abamb_list)))
    print("\tWord={0}:{1}".format(toCListStr(word_list), toCListStr(aword_list)))
    print("\tWind={0}:{1}".format(toCListStr(wind_list), toCListStr(awind_list)))
    
    wang_solMap = SMeld1(wang_list, awang_list)
    if not wang_solMap:
        print("\t[Info] No suggest solution for wang list!")
        return
    tube_solMap = SMeld1(tube_list, atube_list)
    if not tube_solMap:
        print("\t[Info] No suggest solution for tube list!")
        return
    bamb_solMap = SMeld1(bamb_list, abamb_list)
    if not bamb_solMap:
        print("\t[Info] No suggest solution for bamboo list!")
        return
    word_solMap = SMeld2(word_list, aword_list)
    if not word_solMap:
        print("\t[Info] No suggest solution for word list!")
        return
    wind_solMap = SMeld2(wind_list, awind_list)
    if not wind_solMap:
        print("\t[Info] No suggest solution for wind list!")
        return
    
    soluMap = {}
    tmc = -1
    for wang_cp in wang_solMap.keys():  # wang loop
        hasEye = wang_solMap.get(wang_cp)[0][2]
        mc = len(wang_cp[1:len(wang_cp)-1].split(','))/3
        ac = len(wang_solMap.get(wang_cp)[0][1])
        #print('\t[Test] {0}/{1}/{2}...'.format(toCListStr(wang_solMap.get(wang_cp)[0][0]), mc, ac))
        for tube_cp in tube_solMap.keys(): # tube loop
            hasEye2 = tube_solMap.get(tube_cp)[0][2]
            if hasEye and hasEye2: continue
            tmc = len(tube_cp[1:len(tube_cp)-1].split(','))/3
            if (mc+tmc) > origMeldCnt: continue
            mc2 = mc + tmc
            ac2 = len(tube_solMap.get(tube_cp)[0][1])+ac
            hasEye2 = hasEye or hasEye2
            #print('\t[Test] {0}/{1}/{2}...'.format(toCListStr(tube_solMap.get(tube_cp)[0][0]), mc2, ac2))
            for bamb_cp in bamb_solMap.keys(): # bamb loop
                hasEye3 = bamb_solMap.get(bamb_cp)[0][2]
                if hasEye2 and hasEye3: continue
                tmc = len(bamb_cp[1:len(bamb_cp)-1].split(','))/3
                if (mc2+tmc) > origMeldCnt: continue
                mc3 = mc2+tmc
                ac3 = len(bamb_solMap.get(bamb_cp)[0][1])+ac2
                hasEye3 = hasEye2 or hasEye3
                #print("\t[Test] {0}/{1}/{2}...".format(toCListStr(bamb_solMap.get(bamb_cp)[0][0]), mc3, ac3))
                for word_cp in word_solMap.keys(): # word loop
                    hasEye4 = word_solMap.get(word_cp)[0][2]
                    if hasEye4 and hasEye3: continue
                    tmc = len(word_cp[1:len(word_cp)-1].split(','))/3
                    if (mc3+tmc) > origMeldCnt: continue
                    mc4 = mc3+tmc
                    ac4 = len(word_solMap.get(word_cp)[0][1])+ac3
                    hasEye4 = hasEye3 or hasEye4
                    for wind_cp in wind_solMap.keys(): # wind loop
                        if hasEye4 == bamb_solMap.get(bamb_cp)[0][2]: continue
                        tmc = len(wind_cp[1:len(wind_cp)-1].split(','))/3
                        if (mc4+tmc) != origMeldCnt: continue
                        cardForm = "{0}/{1}/{2}/{3}/{4}".format(toCListStr(wang_solMap.get(wang_cp)[0][0]),\
                                                                toCListStr(tube_solMap.get(tube_cp)[0][0]),\
                                                                toCListStr(bamb_solMap.get(bamb_cp)[0][0]),\
                                                                toCListStr(word_solMap.get(word_cp)[0][0]),\
                                                                toCListStr(wind_solMap.get(wind_cp)[0][0]))
                        soluMap[cardForm] = ac4 + len(wind_solMap.get(wind_cp)[0][1])
                        print("\t[Test] {0} -> {1}".format(cardForm, soluMap[cardForm]))
    return soluMap

# BD: Check completed meld(s) with eye
# Return: True means card list satisfies completed meld(s) with eye.
#         False/None otherwise
def MeldDoneWithEye(clist):
    """ Check completed Meld with Eye for given card list.
    * Argument:
      clist - Card list
    * Return:
      True to satisfy requirement; False otherwise."""
    if len(clist) == 0: return False
    ct = GameBoard.CardType(clist[0])
    if ct < 4:
        return _MeldDoneWithEyeRec1(GameBoard.ToIntList(clist))
    else:
        return _MeldDoneWithEyeRec2(clist)

def _MeldDoneWithEyeRec1(clist):
    """ Check completed Meld with Eye for given card list. (Recursive implementation for 萬/筒/條)
    * Argument:
      clist - Card list
    * Return:
      True to satisfy requirement; False otherwise."""
    if len(clist) == 0: return False
    clist.sort()
    if len(clist) > 2:
        if clist[0] == clist[1] and clist[1] == clist[2]:
            return _MeldDoneWithEyeRec1(clist[3:]) or _MeldDoneRec1(clist[2:])
        elif clist[0] != clist[1]:
            val = clist[0]
            if (val+1) in clist and (val+2) in clist:
                clist.remove(val)
                clist.remove(val+1)
                clist.remove(val+2)
                return _MeldDoneWithEyeRec1(clist)
            return False
        else:
            val = clist[0]
            if clist.count(val+1) == 2 and clist.count(val+2) == 2:
                return _MeldDoneWithEyeRec1(clist[6:]) or _MeldDoneRec1(clist[2:])
            else:
                return _MeldDoneRec1(clist[2:])
    elif len(clist) == 2:
        return clist[0] == clist[1]
    return False

def _MeldDoneWithEyeRec2(clist):
    """ Check completed Meld with Eye for given card list. (Recursive implementation for 字/風)
    * Argument:
      clist - Card list
    * Return:
      True to satisfy requirement; False otherwise."""
    clist.sort()
    if len(clist) == 0:
        return False
    elif len(clist) > 2:
        if clist[0] == clist[1] and clist[1] == clist[2]:
            return _MeldDoneWithEyeRec2(clist[3:])
        elif clist[0] == clist[1]:
            return _MeldDoneRec2(clist[2:])
    elif len(clist) == 2:
        return clist[0] == clist[1]
    return False

# BD: Check completed meld(s).
# Return: True means card list satisfies completed meld(s).
#         False/None otherwise.
def MeldDone(clist):
    """ Check completed Meld without Eye for given card list.
    * Argument:
      clist - Card list
    * Return:
      True to satisfy requirement; False otherwise."""
    if len(clist) == 0: return True
    ct = GameBoard.CardType(clist[0])
    if ct < 4:
        return _MeldDoneRec1(GameBoard.ToIntList(clist))
    else:
        return _MeldDoneRec2(clist)

def _MeldDoneRec1(clist):
    """ Check completed Meld without Eye for given card list. (Recursive implementation for 萬/筒/條)
    * Argument:
      clist - Card list
    * Return:
      True to satisfy requirement; False otherwise."""
    clist.sort()
    if len(clist) == 0:
        return True
    elif len(clist) % 3 == 0:
        if clist[0] == clist[1] and clist[1] == clist[2]:
            return _MeldDoneRec1(clist[3:])
        elif clist[0] != clist[1]:
            val = clist[0]
            if (val+1) in clist and (val+2) in clist:
                clist.remove(val)
                clist.remove(val+1)
                clist.remove(val+2)
                return _MeldDoneRec1(clist)
            return False
        else:
            val = clist[0]
            if clist.count(val+1) == 2 and clist.count(val+2) == 2:
                return _MeldDoneRec1(clist[6:])
            return False

def _MeldDoneRec2(clist):
    """ Check completed Meld without Eye for given card list. (Recursive implementation for 風/字)
    * Argument:
      clist - Card list
    * Return:
      True to satisfy requirement; False otherwise."""
    clist.sort()
    if len(clist) == 0:
        return True
    elif len(clist) % 3 == 0:
        if clist[0] == clist[1] and clist[1] == clist[2]:
            return _MeldDoneRec2(clist[3:])
    return False

# BD: Translate tile string list into corresponding int list.
def ToIntList(clist):
    """ Translate tile string list into corresponding int list. (Only for 萬/筒/條)
    Example [1萬, 2萬, 3萬] -> [1, 2, 3]
    * Argument:
      clist - Card list.
    * Return:
      Translated result."""
    tlist = []
    for e in clist:
        tlist.append(int(e[0:1]))
    return tlist

# BD: Solution of Meld on Tile Type=萬/筒/條 牌.
# Argument:
#   - clist: Card/Tile list in hand
#   - availList: Available Card/Tile list.
# Return:
#   Map: key as solution card composition; value as tuple(Card Composition, Actions, HasEye Flag) 
def SMeld1(clist, availList):
    """ Solution to generate completed meld(s) from given card list (Only 萬/筒/條).
    For example, if you have card list [1萬, 3萬], 'add 2萬' will be one of the solution to generate a completed meld.
    * Argument:
      clist - Card list
      availList - Available card list corresponding to <clist>.
    * Return:
      Map - Key as solution card composition; Value as tuple(Card Composition, Actions, HasEye Flag)"""
    actions = []
    alist = _SMeld1(clist, availList, actions, 0)
    if alist:
        anwsMap = {}
        for aws in alist:
            key = aws[0].__str__()            
            if not key in anwsMap:
                al = []
                al.append(aws)
                anwsMap[key] = al
            else:
                al = anwsMap[key]
                if len(al[0][1]) > len(aws[1]):
                    del al[:]
                    al.append(aws)                
                elif len(al[0][1]) == len(aws[1]):
                    al.append(aws)
        return anwsMap

def SMeld2(clist, availList):
    """ Solution to generate completed meld(s) from given card list (Only 字/風).
    For example, if you have card list [東, 東], 'add 東', ''(Do nothing) will be two cases of the solution to generate a completed meld.
    * Argument:
      clist - Card list
      availList - Available card list corresponding to <clist>.
    * Return:
      Map - Key as solution card composition; Value as tuple(Card Composition, Actions, HasEye Flag)"""
    actions = []
    alist = _SMeld2(clist, availList, actions, 0)
    if alist:
        anwsMap = {}
        for aws in alist:
            key = aws[0].__str__()
            if not key in anwsMap:
                al = []
                al.append(aws)
                anwsMap[key] = al
            else:
                al = anwsMap[key]
                if len(al[0][1]) > len(aws[1]):
                    del al[:]
                    al.append(aws)
                elif len(al[0][1]) == len(aws[1]):
                    al.append(aws)
        return anwsMap

# BD: Recursive Search Completed Meld for Word/Wind card
def _SMeld2(clist, availList, actions, depth):
    if depth > MAX_MELD_SEARCH_DEPTH:
        return None
    clist.sort()
    if len(clist) == 0:
        wlist = []
        alist = actions[:]
        smeldaws = []
        smeldaws.append((wlist, alist, False))
        return smeldaws
##    elif len(clist) == 2 and clist[0] == clist[1]:
##        wlist = clist[:]
##        alist = actions[:]
##        hlist = availList[:]
##        smeldaws = []
##        smeldaws.append((wlist, alist, True))
##        if clist[0] in hlist:
##            wlist = clist[:]
##            alist = actions[:]
##            alist.append("add {0}".format(wlist[0]))
##            wlist.append(clist[0])
##            smeldaws.append((wlist, alist, False))
##        return smeldaws
    elif MeldDone(clist):
        wlist = clist[:]
        alist = actions[:]
        smeldaws = []
        smeldaws.append((wlist, alist, False))
        return smeldaws
    elif MeldDoneWithEye(clist):
        wlist = clist[:]
        alist = actions[:]
        smeldaws = []
        smeldaws.append((wlist, alist, True))
        return smeldaws
    else:
        wlist = clist[:]
        alist = actions[:]
        hlist = availList[:]
        smeldaws = []
        # Game search start!
        atileSet = set()
        for t in hlist: atileSet.add(t)
        
        # 1. Add tile
        for tile in atileSet:
            alist.append("add {0}".format(tile))
            wlist.append(tile)
            hlist.remove(tile)
            slist = _SMeld2(wlist, hlist, alist, depth+1)
            if slist: 
                smeldaws.extend(slist)
            wlist = clist[:]
            alist = actions[:]
            hlist = availList[:]
        # 2. Drop tile
        htileSet = set()
        for t in wlist: htileSet.add(t)
        for tile in htileSet:
            alist.append("drop {0}".format(tile))
            wlist.remove(tile)
            slist = _SMeld2(wlist, hlist, alist, depth+1)
            if slist: smeldaws.extend(slist)
            wlist = clist[:]
            alist = actions[:]
            hlist = availList[:]
        
        # 3. Switch tile
        for t in htileSet:
            for tile in atileSet:
                if t == tile: continue
                alist.append("switch {0} to {1}".format(t, tile))
                wlist.remove(t)
                wlist.append(tile)
                hlist.remove(tile)
                slist = _SMeld2(wlist, hlist, alist, depth+1)
                if slist: smeldaws.extend(slist)
                wlist = clist[:]
                alist = actions[:]
                hlist = availList[:]
        return smeldaws

# BD: Recursive Search Completed Meld for 萬筒條 card.
def _SMeld1(clist, availList, actions, depth):
    if depth > MAX_MELD_SEARCH_DEPTH:
        return None
    clist.sort()
    v1 = -1
    v2 = -1
    if len(clist) >= 2:
        v1 = int(clist[0][0:1])
        v2 = int(clist[1][0:1])
    
    if len(clist) == 0:
        wlist = clist[:]
        alist = actions[:]
        smeldaws = []
        smeldaws.append((wlist, alist, False))
        return smeldaws
##    elif len(clist) == 2 and (v2 == v1+1):
##        wlist = clist[:]
##        alist = actions[:]
##        hlist = availList[:]
##        smeldaws = []
##        tileType = clist[0][1:2]
##        tile = "{0}{1}".format(v2+1, tileType)
##        if tile in hlist:
##            alist.append("add {0}".format(tile))
##            wlist.append(tile)
##            wlist.sort()
##            smeldaws.append((wlist, alist, False))
##        if v1 > 1:
##            tile = "{0}{1}".format(v1-1, tileType)
##            if tile in hlist:
##                wlist = clist[:]
##                alist = actions[:]
##                alist.append("add {0}".format(tile))
##                wlist.append(tile)
##                wlist.sort()
##                smeldaws.append((wlist, alist, False))
##        return smeldaws
    elif MeldDone(clist):
        wlist = clist[:]
        alist = actions[:]
        smeldaws = []
        smeldaws.append((wlist, alist, False))
        return smeldaws
    elif MeldDoneWithEye(clist):
        wlist = clist[:]
        alist = actions[:]
        smeldaws = []
        smeldaws.append((wlist, alist, True))
        return smeldaws
    else:
        # Start game search
        clist.sort()
        wlist = clist[:]
        alist = actions[:]
        hlist = availList[:]
        if len(wlist) == 1:
            tile = wlist[0]
            alist.append("drop {0}".format(tile))
            del wlist[:]
            smeldaws = []
            smeldaws.append((wlist, alist, False))
            
            if tile in availList:
                wlist = clist[:]
                alist = actions[:]
                alist.append("add {0}".format(tile))
                wlist.append(tile)
                smeldaws.append((wlist, alist, True))
            return smeldaws
        else:
            smeldaws = []
            atileSet = set()
	    for t in hlist: atileSet.add(t)
	    # Add tile
	    #print('\t[Test] Check add tile...')
	    for tile in atileSet:
		    alist.append("add {0}".format(tile))
		    wlist.append(tile)
		    hlist.remove(tile)
		    aws_list = _SMeld1(wlist, hlist, alist, depth+1)
		    if aws_list:
			    smeldaws.extend(aws_list)
		    wlist = clist[:]
		    alist = actions[:]
		    hlist = availList[:]
	    # Drop tile
	    #print('\t[Test] Check drop tile...')
	    tileSet = set()
	    for t in wlist: tileSet.add(t)
	    for t in tileSet:
		    alist.append("drop {0}".format(t))
		    wlist.remove(t)
		    aws_list = _SMeld1(wlist, hlist, alist, depth+1)
		    if aws_list:
			    smeldaws.extend(aws_list)
		    wlist = clist[:]
		    alist = actions[:]
	    # Switch tile
	    #print('\t[Test] Check switch tile...')
	    for t in tileSet:
		    for tile in atileSet:
			    if tile == t: continue
			    alist.append("switch {0} to {1}".format(t, tile))
			    wlist.remove(t)
			    wlist.append(tile)
			    hlist.remove(tile)
			    aws_list = _SMeld1(wlist, hlist, alist, depth+1)
			    if aws_list:
				    smeldaws.extend(aws_list)
			    wlist = clist[:]
			    alist = actions[:]
			    hlist = availList[:]
	    return smeldaws
                    

def RemoveTriplet(clist):
    """ Remove all Triplet of given card list.
    * Argument:
      clist - card list."""
    clist.sort()
    rlist = []
    i = 0
    while i+2 < len(clist):
        if clist[i] == clist[i+1] and clist[i+1] == clist[i+2]:
            del clist[i:i+3]
            continue
        i+=1
