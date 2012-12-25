#-*- coding: utf-8 -*-
import os.path
import subprocess
import random

# 0) Global function
def searchWithEye(clist):
    """Search Completed Meld With Eye
    * Argument:
        clist - Card list
    * Return:
        True if the card list satisfied completed meld with eye; False/None otherwise.
    """
    if len(clist)==0:
        return False
    elif len(clist)>2:
        if clist[0]==clist[1]==clist[2]:
            # 刻 (Triplet)
            return searchWithEye(clist[3:]) or searchNoEye(clist[2:])
        elif clist[0]!=clist[1]:
            val = clist[0]
            if (val+1 in clist) and (val+2 in clist):
                clist.remove(val)
                clist.remove(val+1)
                clist.remove(val+2)
                clist.sort()
                return searchWithEye(clist)
            else:
                return False
        else:
            val = clist[0]
            if clist.count(val+1)==2 and clist.count(val+2)==2:
                # 順 (Sequence)
                return searchWithEye(clist[6:]) or searchNoEye(clist[2:])
            else:    
                return searchNoEye(clist[2:])
    elif len(clist)==2:
        return clist[0] == clist[1]
    else:
        return False
    
def searchNoEye(clist):
    """Search Completed Meld Without Eye
    * Argument:
        clist - Card list
    * Return:
        True if the card list satisfied completed meld; False/None otherwise.
    """
    if len(clist)==0:
        return True
    elif len(clist)>2:
        if clist[0]==clist[1]==clist[2]:
            # 刻 (Triplet)
            del clist[0:3]
            return searchNoEye(clist)
        elif clist[0]!=clist[1]:
            # 順 (Sequence)
            val = clist[0]
            if (val+1 in clist) and (val+2 in clist):
                clist.remove(val)
                clist.remove(val+1)
                clist.remove(val+2)
                clist.sort()
                return searchNoEye(clist)
            else:
                return False
        else:
            val = clist[0]
            if clist.count(val+1)==2 and clist.count(val+2)==2:
                del clist[0:6]
                clist.sort()
                return searchNoEye(clist)
            else:    
                return False
    else:
        return False

def toCListStr(clist):
    """ Translate Give Card List Into String
    * Argument:
      clist - Card list
    * Return:
      String representation of card list.
    """
    cstr = '['
    if len(clist) > 0:
        cstr+="{0:s}".format(clist[0])
        for i in range(1, len(clist)):
            cstr+=" {0:s}".format(clist[i])
    cstr+=']'
    return cstr

# 1) Class definition
class GameBoard:
    """ Game Board as frameword to simulate Mahjong Gameing.
    * Information
      - Mahjoing rule: http://ezmjtw.tripod.com/mahjong16-big5.htm
      - 麻將基本術語中英文對照表: http://www.xqbase.com/other/mahjongg_english.htm
                               http://liangliangliang.pixnet.net/blog/post/15530445-%E2%99%A5%E9%BA%BB%E5%B0%87%E8%8B%B1%E6%96%87mahjong-%E5%9F%BA%E6%9C%AC%E5%96%AE%E5%AD%97%E7%AF%87%E2%99%A5
      - 麻將胡牌技巧: http://ezmjtw.tripod.com/mahjongskill-big5.htm
    """
    def __init__(self):
        self.bamb_list = [] # 條子
        self.wang_list = [] # 萬字
        self.tube_list = [] # 筒子
        self.flow_list = [] # 花牌
        self.word_list = [] # 字牌 (中發白)
        self.wind_list = [] # 風牌
        self.aget_list = [] # 玩家
        self.drop_list = [] # 海底
        self.fwind_list = []
        self.fword_list = []
        self.fwang_list = []
        self.ftube_list = []
        self.fbamb_list = []
        self.play_turn = 0  # 摸牌玩家
        self.fwind_list.append('東')
        self.fwind_list.append('西')
        self.fwind_list.append('南')
        self.fwind_list.append('北')
        self.fword_list.append('中')
        self.fword_list.append('發')
        self.fword_list.append('白')
        self.win_round = {}
        self.pwin_round = {}
        for i in range(1,10):
            self.fwang_list.append('{0}萬'.format(i))        
            self.ftube_list.append('{0}筒'.format(i))
            self.fbamb_list.append('{0}條'.format(i))
       
        self.debug = False
        self.win_agent = None
        self.drop_record = {}
        self.wrong_count = 0
        self.play_count = 0
        self.card_count = 0
        #self.shuffle()        

    def show_tube_list(self):
        """ Show tube(筒) card list in hand."""
        print("{0}".format(toCListStr(self.tube_list)))

    def show_wang_list(self):
        """ Show wang(萬) card list in hand."""
        print("{0}".format(toCListStr(self.wang_list)))

    def show_bamb_list(self):
        """ Show bamboo(條) card list in hand."""
        print("{0}".format(toCListStr(self.bamb_list)))

    def show_wind_list(self):
        """ Show wind(風) card list in hand."""
        print("{0}".format(toCListStr(self.wind_list)))

    def show_word_list(self):
        """ Show word(中發白) card list in hand."""
        print("{0}".format(toCListStr(self.word_list)))

    def awang_list(self, agent=None):
        """ Return available wang card list except those exist in sea bed, eat meld, pong/gong meld.
        * Argument:
          agent - Self Agent used to get rid of the available count. 
        * Return:
          List of wang card possible to obtain.
        * Note
          Some cards may be in other agents' hands will be obtained in the return list."""
        awang_list = []
        for wc in self.fwang_list:
            cnt = 4 - self.drop_list.count(wc)
            for agt in self.aget_list:
                cnt -= agt.pong_list.count(wc)
            if agent:
                cnt -= agent.wang_list.count(wc)            
            awang_list.extend([wc]*cnt)
        return awang_list

    def atube_list(self, agent=None):
        """ Return available wang card list except those exist in sea bed, eat meld, pong/gong meld.
        * Argument:
          agent - Self Agent used to get rid of the available count.
        * Return:
          List of tube card possible to obtain.
        * Note
          Some cards may be in other agents' hands will be obtained in the return list."""
        alist = []
        for t in self.ftube_list:
            cnt = 4 - self.drop_list.count(t)
            for agt in self.aget_list:
                cnt -= agt.pong_list.count(t)
            if agent:
                cnt -= agent.tube_list.count(t)
            alist.extend([t]*cnt)
        return alist

    def abamb_list(self, agent=None):
        """ Return available bamboo card list except those exist in sea bed, eat meld, pong/gong meld.
        * Argument:
          agent - Self Agent used to get rid of the available count.
        * Return:
          List of bamboo card possible to obtain.
        * Note
          Some cards may be in other agents' hands will be obtained in the return list."""
        alist = []
        for t in self.fbamb_list:
            cnt = 4 - self.drop_list.count(t)
            for agt in self.aget_list:
                cnt -= agt.pong_list.count(t)
            if agent:
                cnt -= agent.bamb_list.count(t)
            alist.extend([t]*cnt)            
        return alist

    def aword_list(self, agent=None):
        """ Return available word card list except those exist in sea bed, eat meld, pong/gong meld.
        * Argument:
          agent - Self Agent used to get rid of the available count.
        * Return:
          List of word(中發白) card possible to obtain.
        * Note
          Some cards may be in other agents' hands will be obtained in the return list."""
        alist = []
        for t in self.fword_list:
            cnt = 4 - self.drop_list.count(t)
            for agt in self.aget_list:
                cnt -= agt.pong_list.count(t)
            if agent:
                cnt -= agent.word_list.count(t)
            alist.extend([t]*cnt) 
        return alist

    def awind_list(self, agent=None):
        """ Return available wind card list except those exist in sea bed, eat meld, pong/gong meld.
        * Argument:
          agent - Self Agent used to get rid of the available count.
        * Return:
          List of wind(風牌) card possible to obtain.
        * Note
          Some cards may be in other agents' hands will be obtained in the return list."""
        alist = []
        for t in self.fwind_list:
            cnt = 4 - self.drop_list.count(t)
            for agt in self.aget_list:
                cnt -= agt.pong_list.count(t)
            if agent:
                cnt -= agent.wind_list.count(t)
            alist.extend([t]*cnt) 
        return alist

    def rightOpponent(self, agent):
        """ Obtain the right opponent agent (下家).
        * Argument:
          agent - Self Agent.
        * Return:
          Right hand side agent object.
        """
        if agent in self.aget_list and len(self.aget_list) > 1:
            curpos = self.aget_list.index(agent)
            return self.aget_list[(curpos+1) % len(self.aget_list)]

    def leftOpponent(self, agent):
        """ Obtain the left opponent agent (上家).
        * Argument:
          agent - Self Agent.
        * Return:
          Left hand side agent object.
        """
        if agent in self.aget_list and len(self.aget_list) > 1:
            curpos = self.aget_list.index(agent)
            return self.aget_list[(curpos-1) % len(self.aget_list)]
            #else:
            #    return self.aget_list[len(self.aget_list) - 1]

    def appendAgent(self, agent):
        """ Join gameboard with given agent.
        * Argument:
          agent - Agent object to join gameboard.
        """
        self.aget_list.append(agent)

    def appearCardCount(self, card):
        """ Count shown card 
        * Argument:
          card - Card to count.
        * Return:
          How many of given card shown on table(In sea bed, eat meld, pong/kong meld). 
        """
        cnt = 0
        for agent in self.aget_list:
            cnt += agent.pong_list.count(card)
        cnt += self.drop_list.count(card)
        return cnt 

    @staticmethod
    def ToIntList(clist):
        """ Translate Card List(萬/筒/條) into corresponding Int List.
        * Argument:
          clist - Card list
        * Return:
          Translated list. Ex. [1萬, 2萬, 3萬] -> [1, 2, 3]
        """
        tlist = []
        for e in clist:
            tlist.append(int(e[0:1]))
        return tlist

    # 確認 clist 是否有雀眼. clist 必須是完整的 meld+雀眼.
    @staticmethod
    def HasEye(ctype, clist):
        """ Check if the given card List has Eye.
        * Argument:
          ctype - Card type(1=萬;2=筒;3=條;4=字;5=風)
          clist - Card list
        * Return:
          True to have eye; False otherwise."""
        list_len = len(clist)
        if list_len > 1:
            if ctype <=3:
                for e in set(clist):
                    if clist.count(e) == 2:                        
                        if searchWithEye(GameBoard.ToIntList(clist)):
                            return e
            else:
                GameBoard.RemoveTriplet(clist[:])
                if len(clist)==2 and (clist[0]==clist[1]):
                    return clist[0]

    @staticmethod
    def RemoveTriplet(clist):
        """ Remove all Triple from given card list.
        * Argument:
          clist - Card list
        """
        clist.sort()
        p=0
        while p+2<len(clist):
            if clist[p]==clist[p+1] and clist[p+1]==clist[p+2]:
                del clist[p:p+3]
            else:
                p+=1            

    # 從 check_tuple = (card_type, card_list) 中找出可以胡牌的 Tile
    # Input: check_tuple = (card_type, card_list)
    # Output: win tile list
    @staticmethod
    def searchWTiles(chek_tuple, hasEye=True):
        """ Search card(s) leading to win. (找 萬/筒/條/風/字 牌形成 Completed meld 所缺的牌)
        * Argument:
          chek_tuple - Tuple(card type, card list)
          hasEye - True to consider the Eye; False otherwise.
        * Return:
          A list contains card list lead to win.
        """
        tiles=[]
        if chek_tuple[0]==1:
            for i in range(1,10):                    
                c_list = []
                for e in chek_tuple[1]:
                    c_list.append(int(e[0:1]))
                c_list.append(i)
                c_list.sort()
                if hasEye and searchWithEye(c_list):
                    tiles.append('{0}萬'.format(i))
                elif not hasEye and searchNoEye(c_list):
                    tiles.append('{0}萬'.format(i))
        elif chek_tuple[0]==2:
            for i in range(1,10):                    
                c_list = []
                for e in chek_tuple[1]:
                    c_list.append(int(e[0:1]))
                c_list.append(i)
                c_list.sort()
                if hasEye and searchWithEye(c_list):
                    tiles.append('{0}筒'.format(i))
                elif not hasEye and searchNoEye(c_list):
                    tiles.append('{0}筒'.format(i))
        elif chek_tuple[0]==3:
            for i in range(1,10):                    
                c_list = []
                for e in chek_tuple[1]:
                    c_list.append(int(e[0:1]))
                c_list.append(i)
                c_list.sort()
                if hasEye and searchWithEye(c_list):
                    tiles.append('{0}條'.format(i))
                elif not hasEye and searchNoEye(c_list):
                    tiles.append('{0}條'.format(i))
        elif chek_tuple[0]==4: # 中發白
            GameBoard.RemoveTriplet(chek_tuple[1])
            if hasEye and (len(chek_tuple[1])==1):
                tiles.append(chek_tuple[1][0])
            elif not hasEye and (len(chek_tuple[1])==2):
                if chek_tuple[0] == chek_tuple[1]:
                    return chek_tuple[0]
        elif chek_tuple[0]==5: # 風牌
            GameBoard.RemoveTriplet(chek_tuple[1])
            if(len(chek_tuple[1])==1):
                tiles.append(chek_tuple[1][0])
            elif not hasEye and (len(chek_tuple[1])==2):
                if chek_tuple[0] == chek_tuple[1]:
                    return chek_tuple[0]
        return tiles
    @staticmethod
    def PreWinTiles2(wang_list, tube_list, bamb_list, word_list, wind_list):
        """ Confirm the tile lead to goal state according to given card lists."""
        meld_list = []
        chek_list = []
        if len(wang_list) > 0:
            if len(wang_list)%3==0:
                meld_list.append(wang_list[:])
            else:
                chek_list.append((1, wang_list[:]))
            
        if len(tube_list) > 0:
            if len(tube_list)%3==0:
                meld_list.append(tube_list[:])
            else:
                chek_list.append((2, tube_list[:]))

        if len(bamb_list) > 0:
            if len(bamb_list)%3==0:
                meld_list.append(bamb_list[:])
            else:
                chek_list.append((3, bamb_list[:]))

        if len(word_list) > 0:
            if len(word_list)%3==0:
                meld_list.append(word_list[:])
            else:
                chek_list.append((4, word_list[:]))

        if len(wind_list) > 0:
            if len(wind_list)%3==0:
                meld_list.append(wind_list[:])
            else:
                chek_list.append((5, wind_list[:]))

        # 1) Check impossible composition
        if len(chek_list) > 2:
            return []

        for clist in meld_list:
            ctype = GameBoard.CardType(clist[0])
            if ctype<4:                
                if not searchNoEye(GameBoard.ToIntList(clist)):
                    return []
            else:
                GameBoard.RemoveTriplet(clist)
                if(len(clist)!=0):
                    return []

        # 2) Start to look for possible tiles to win
        if len(chek_list)==2: 
            eye_1 = GameBoard.HasEye(chek_list[0][0], chek_list[0][1])
            eye_2 = GameBoard.HasEye(chek_list[1][0], chek_list[1][1])
            if eye_1 and eye_2:
                #print('eye_1={0}; eye_2={1}'.format(eye_1, eye_2))
                #print('check {0}'.format(eye_1))
                tiles = []
                chek_tuple = chek_list[0]
                chek_tuple[1].append(eye_1)
                chek_tuple[1].sort()
                if chek_tuple[0]<=3:
                    if searchNoEye(GameBoard.ToIntList(chek_tuple[1])):
                        tiles.append(eye_1)
                    else:
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) == 0:
                        tiles.append(eye_1)
                    else:
                        return []                
                chek_tuple = chek_list[1]
                chek_tuple[1].append(eye_2)
                chek_tuple[1].sort()
                #print('check {0}->{1}'.format(eye_2, chek_tuple[1]))
                if chek_tuple[0]<=3:
                    if searchNoEye(GameBoard.ToIntList(chek_tuple[1])):
                        tiles.append(eye_2)
                    else:
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) == 0:
                        tiles.append(eye_2)
                    else:
                        return []
                return tiles
            elif eye_1:                
                chek_tuple = chek_list[0]
                #print('Check eye_1={0}={1}!'.format(eye_1, chek_tuple[1]))
                if chek_tuple[0]<=3:
                    if not searchWithEye(GameBoard.ToIntList(chek_tuple[1])):
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) != 0:
                        return []
                #print('Pass check. Search tile...{0}'.format(chek_list[1]))
                return GameBoard.searchWTiles(chek_list[1], hasEye=False)
            elif eye_2:
                #print('Check eye_2={0}={1}!'.format(eye_2, chek_tuple[1]))
                chek_tuple = chek_list[1]
                if chek_tuple[0]<=3:
                    if not searchWithEye(GameBoard.ToIntList(chek_tuple[1])):
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) != 0:
                        return []
                #print('Pass check. Search tile {0}...'.format(chek_list[0]))
                return GameBoard.searchWTiles(chek_list[0], hasEye=False)
            else:
                return []
        else:
            if len(chek_list) > 0:
                chek_tuple = chek_list[0]
                return GameBoard.searchWTiles(chek_tuple)
        return []

    @staticmethod
    def PreWinTiles(agent):
        """ Confirm the tile lead to win according to card list in hand.
        Example: Input Agent=[1萬 2萬 3萬 4萬 4萬 1筒 3筒 3筒 3筒 3筒 ] / [] / []
                 Output=['2筒']
        * Argument:
          agent - Agent object.
        * Return:
          Card list leading to win(agent 正在聽的牌)."""
        #tiles = []
        meld_list = []
        chek_list = []
        if len(agent.wang_list) > 0:
            if len(agent.wang_list)%3==0:
                meld_list.append(agent.wang_list[:])
            else:
                chek_list.append((1, agent.wang_list[:]))
            
        if len(agent.tube_list) > 0:
            if len(agent.tube_list)%3==0:
                meld_list.append(agent.tube_list[:])
            else:
                chek_list.append((2, agent.tube_list[:]))

        if len(agent.bamb_list) > 0:
            if len(agent.bamb_list)%3==0:
                meld_list.append(agent.bamb_list[:])
            else:
                chek_list.append((3, agent.bamb_list[:]))

        if len(agent.word_list) > 0:
            if len(agent.word_list)%3==0:
                meld_list.append(agent.word_list[:])
            else:
                chek_list.append((4, agent.word_list[:]))

        if len(agent.wind_list) > 0:
            if len(agent.wind_list)%3==0:
                meld_list.append(agent.wind_list[:])
            else:
                chek_list.append((5, agent.wind_list[:]))

        # 1) Check impossible composition
        if len(chek_list) > 2:
            return []

        for clist in meld_list:
            ctype = GameBoard.CardType(clist[0])
            if ctype<4:                
                if not searchNoEye(GameBoard.ToIntList(clist)):
                    return []
            else:
                GameBoard.RemoveTriplet(clist)
                if(len(clist)!=0):
                    return []

        # 2) Start to look for possible tiles to win
        if len(chek_list)==2: 
            eye_1 = GameBoard.HasEye(chek_list[0][0], chek_list[0][1])
            eye_2 = GameBoard.HasEye(chek_list[1][0], chek_list[1][1])
            if eye_1 and eye_2:
                #print('eye_1={0}; eye_2={1}'.format(eye_1, eye_2))
                #print('check {0}'.format(eye_1))
                tiles = []
                chek_tuple = chek_list[0]
                chek_tuple[1].append(eye_1)
                chek_tuple[1].sort()
                if chek_tuple[0]<=3:
                    if searchNoEye(GameBoard.ToIntList(chek_tuple[1])):
                        tiles.append(eye_1)
                    else:
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) == 0:
                        tiles.append(eye_1)
                    else:
                        return []                
                chek_tuple = chek_list[1]
                chek_tuple[1].append(eye_2)
                chek_tuple[1].sort()
                #print('check {0}->{1}'.format(eye_2, chek_tuple[1]))
                if chek_tuple[0]<=3:
                    if searchNoEye(GameBoard.ToIntList(chek_tuple[1])):
                        tiles.append(eye_2)
                    else:
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) == 0:
                        tiles.append(eye_2)
                    else:
                        return []
                return tiles
            elif eye_1:                
                chek_tuple = chek_list[0]
                #print('Check eye_1={0}={1}!'.format(eye_1, chek_tuple[1]))
                if chek_tuple[0]<=3:
                    if not searchWithEye(GameBoard.ToIntList(chek_tuple[1])):
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) != 0:
                        return []
                #print('Pass check. Search tile...{0}'.format(chek_list[1]))
                return GameBoard.searchWTiles(chek_list[1], hasEye=False)
            elif eye_2:
                #print('Check eye_2={0}={1}!'.format(eye_2, chek_tuple[1]))
                chek_tuple = chek_list[1]
                if chek_tuple[0]<=3:
                    if not searchWithEye(GameBoard.ToIntList(chek_tuple[1])):
                        return []
                else:
                    GameBoard.RemoveTriplet(chek_tuple[1])
                    if len(chek_tuple[1]) != 0:
                        return []
                #print('Pass check. Search tile {0}...'.format(chek_list[0]))
                return GameBoard.searchWTiles(chek_list[0], hasEye=False)
            else:
                return []
        else:
            if len(chek_list) > 0:
                chek_tuple = chek_list[0]
                return GameBoard.searchWTiles(chek_tuple)
        return []
        
    @staticmethod
    def NextCard(card):
        """ Retrieve next Wang/Tube/Bamb card in number order. (筒萬條的下張轉換函數)
        Input: 筒萬條. Ex. '1萬' ,'2筒' ,'3條'.
        Output: 筒萬條的下一張. 但如果是 9筒/萬/條 或不是筒萬條, 則返回 None.
        Example: Input='1萬' ; Output='2萬'
        * Argument:
          card - wang/tube/bamb card.
        * Return:
          Previous card in order or None."""
        ctype = GameBoard.CardType(card)
        number = int(card[:1])        
        if ctype==1:
            if number<9:
                return "{0}{1}".format(number+1, '萬')
        elif ctype==2:
            if number<9:
                return "{0}{1}".format(number+1, '筒')
        elif ctype==3:
            if number<9:
                return "{0}{1}".format(number+1, '條')

    @staticmethod
    def PrevCard(card):
        """ Retrieve previous Wang/Tube/Bamb card in number order. (筒萬條的上張轉換函數)
        Input: 筒萬條. Ex. '1萬' ,'2筒' ,'3條'.
        Output: 筒萬條的下一張. 但如果是 9筒/萬/條 或不是筒萬條, 則返回 None.
        Example: Input='2筒' ; Output='1筒'
        * Argument:
          card - wang/tube/bamb card.
        * Return:
          Prefious card in number order or None."""
        ctype = GameBoard.CardType(card)
        number = int(card[:1])        
        if ctype==1:
            if number>1:
                return "{0}{1}".format(number-1, '萬')
        elif ctype==2:
            if number>1:
                return "{0}{1}".format(number-1, '筒')
        elif ctype==3:
            if number>1:
                return "{0}{1}".format(number-1, '條')
            
    # 胡牌判斷
    @staticmethod
    def GoalState(agent, card):
        """ Goal State Check. (胡牌判斷)
        * Argument:
          agent - Agent object
          card - Card to join card list in hand.
        * Return:
          True to win; False otherwise."""
        # http://www.programmer-club.com/showSameTitleN/gameprogram/3310.html
        tbamb_list = [] # 條子
        for e in agent.bamb_list:
            tbamb_list.append(int(e[0:1]))
        twang_list = [] # 萬字
        for e in agent.wang_list:
            twang_list.append(int(e[0:1]))    
        ttube_list = [] # 筒子
        for e in agent.tube_list:
            ttube_list.append(int(e[0:1]))    
        tword_list = agent.word_list[:] # 字牌 (中發白)
        twind_list = agent.wind_list[:] # 風牌
        ctype = GameBoard.CardType(card)
        if ctype==1:
            twang_list.append(int(card[0:1]))
            twang_list.sort()
        elif ctype==2:
            ttube_list.append(int(card[0:1]))
            ttube_list.sort()
        elif ctype==3:
            tbamb_list.append(int(card[0:1]))
            tbamb_list.sort()
        elif ctype==4:
            tword_list.append(card)
            tword_list.sort()
        elif ctype==5:
            twind_list.append(card)
            twind_list.sort()

        #print("\t[Test] Wang: {0}".format(toCListStr()))
        # Filter impossible composition
        bamb_len = len(tbamb_list)
        wang_len = len(twang_list)
        tube_len = len(ttube_list)
        word_len = len(tword_list)
        dirt_len = len(twind_list)
        if (bamb_len%3+wang_len%3+tube_len%3+word_len%3+dirt_len%3)!=2 or \
           bamb_len==1 or wang_len==1 or tube_len==1 or word_len==1 or dirt_len==1:
            #print("\t[Test] Return false-1")
            return False
        
        # 確認 風牌    
        if dirt_len>0:
            GameBoard.RemoveTriplet(twind_list)
            dirt_len = len(twind_list)
            if dirt_len==2: # 雀眼
                if twind_list[0]!=twind_list[1]:
                    #print("\t[Test] Return false-2")
                    return False
                else:
                    del twind_list[:]
            elif dirt_len!=0:
                #print("\t[Test] Return false-3")
                return False
            
        # 確認 字牌
        if word_len>0:
            GameBoard.RemoveTriplet(tword_list)
            word_len = len(tword_list)
            if word_len==2: # 雀眼
                if tword_list[0]!=tword_list[1]:
                    #print("\t[Test] Return false-4")
                    return False
                else:
                    del tword_list[:]
            elif word_len!=0:
                #print("\t[Test] {0}".format(toCListStr(tword_list)))
                #print("\t[Test] Return false-5")
                return False            

        # 確認 條子
        if bamb_len>0:
            if bamb_len%3 == 0: # 刻/順
                if not searchNoEye(tbamb_list):
                    #print("\t[Test] Return false-6")
                    return False
            else: # 含雀眼
                if not searchWithEye(tbamb_list):
                    #print("\t[Test] Return false-7")
                    return False

        # 確認 萬子
        if wang_len>0:
            if wang_len%3 == 0: # 刻/順
                if not searchNoEye(twang_list):
                    #print("\t[Test] Return false-8")
                    return False
            else: # 含雀眼
                if not searchWithEye(twang_list):
                    return False

        # 確認 筒子
        if tube_len>0:
            if tube_len%3 == 0: # 刻/順
                if not searchNoEye(ttube_list):
                    #print("\t[Test] Return false-9")
                    return False
            else: # 含雀眼
                if not searchWithEye(ttube_list):
                    #print("\t[Test] Return false-10")
                    return False        
        return True

    @staticmethod
    def CardType(card):
        """ Card Type (萬/筒/條/字/風 的判斷函式)
        * Argument:
          card - Card to evaluate.
        * Return:
          Integer (1=萬; 2=筒; 3=條; 4=字; 5=風; 6=花)"""
        if card.endswith('萬'): return 1
        elif card.endswith('筒'): return 2
        elif card.endswith('條'): return 3
        elif card in ['中', '發', '白']: return 4
        elif card in ['東', '南', '西', '北']: return 5
        else: return 6 # 花牌

    # 開始遊戲    
    def play(self):
        """ Start to simulate Mahjong game until draw or win."""
        self.play_count+=1
        self.shuffle()
        # Draw cards for each agent
        for agent in self.aget_list:
            agent.assignCard();
            #print(agent)
        
            
        # Start game by assign card to each agent until one of them reach goal state
        i = 0
        while self.card_count>10 and not self.win_agent:
            agent = self.aget_list[int(self.play_turn)]
            self.play_turn = (self.play_turn+1)%len(self.aget_list)
            dcard = None
            if hasattr(agent, 'idraw'):
                dcard = agent.idraw()
            else:
                dcard = agent.draw()
            if hasattr(agent, 'wrong') and agent.wrong:
                self.dprint("[Debug] {0}->{1}".format(agent, agent.card_count))
                agent.wrong=False
                #subprocess.call('sleep 5s', shell=True) 
                self.wrong_count+=1
                break

            if dcard: self.disCard(agent, dcard)
            i+=1
            pwin_ac = 0
            for agent in self.aget_list:
                self.dprint("[Turn{0}] {1}".format(i, agent))
                if hasattr(agent, 'pwin_flag') and agent.pwin_flag:
                    pwin_ac+=1
            
            # Calculate prewin agent distribution
            if i in self.pwin_round:
                pwin_map = self.pwin_round[i]
                if pwin_ac in pwin_map:
                    pwin_map[pwin_ac]+=1
                else:
                    pwin_map[pwin_ac]=1
            else:
                pwin_map = {}
                pwin_map[pwin_ac] = 1
                self.pwin_round[i] = pwin_map

        if self.win_agent:
            self.dprint("\t[Test] Agent({0}) win the game!".format(self.win_agent.name))
            if i in self.win_round:
                self.win_round[i]+=1
            else:
                self.win_round[i]=1
        else:
            self.dprint("\t[Test] 流局...")

    def dprint(self, msg_str):
        """ Debug print function.
        If self.debug=true, print the message. Otherwise ignore the message.
        * Argument:
          msg_str - Debug message to print."""
        if self.debug:
            print(msg_str)

    def testplay(self):
        orig_debug = self.debug
        self.debug = False
        self.play_count+=1
        self.card_count = len(self.wang_list) + len(self.bamb_list) + len(self.tube_list) + \
                          len(self.flow_list) + len(self.word_list) + len(self.wind_list)
        # Draw cards for each agent
        #for agent in self.aget_list:
            #print(agent)
        
            
        # Start game by assign card to each agent until one of them reach goal state
        i = 0
        #print "card count: ",self.card_count
        while self.card_count>10 and not self.win_agent:
            agent = self.aget_list[int(self.play_turn)]
            self.play_turn = (self.play_turn+1)%len(self.aget_list)
            dcard = None
            if hasattr(agent, 'idraw'):
                dcard = agent.idraw()
            else:
                dcard = agent.draw()
            if hasattr(agent, 'wrong') and agent.wrong:
                self.dprint("[Debug] {0}->{1}".format(agent, agent.card_count))
                agent.wrong=False
                #subprocess.call('sleep 5s', shell=True) 
                self.wrong_count+=1
                break
            if dcard: self.disCard(agent, dcard)
            i+=1
        self.debug = orig_debug

    def _recordDrop(self, agent, card):
        if agent.name in self.drop_record:
            drop_list = self.drop_record[agent.name]
            drop_list.append(card)
            drop_list.sort()
        else:
            drop_list = []
            drop_list.append(card)
            self.drop_record[agent.name] = drop_list

    # 丟牌到海底, callback by agent.
    def disCard(self, agent, card):
        self._recordDrop(agent, card)
        # 任一家可以按照順序決定要不要碰牌

        # 確認有沒有人已經胡
        next_pos = self.aget_list.index(agent)+1
        for sft in range(len(self.aget_list)-1):
            other_agent = self.aget_list[(next_pos+sft)%len(self.aget_list)]
            if GameBoard.GoalState(other_agent, card):
                self.win_agent = other_agent
                other_agent.win_card = card
                other_agent.win+=1
                agent.lose+=1
                self.dprint("\t[Test] Agent({0}) 胡牌 {1}!!!".format(other_agent.name, card))
                if hasattr(other_agent, 'hu'):
                    other_agent.hu(card)
                return
                

        # 任一家可以按照順序決定要不要碰牌
        rtv = None
        next_pos = self.aget_list.index(agent)+1
        for sft in range(len(self.aget_list)-1):
            other_agent = self.aget_list[(next_pos+sft)%len(self.aget_list)]
            ctype = GameBoard.CardType(card)
            if ctype==1:
                count = other_agent.wang_list.count(card)
                if count>1:
                    rtv = other_agent.pong(agent, ctype, count, card)
            elif ctype==2:
                count = other_agent.tube_list.count(card)
                if count>1:
                    rtv = other_agent.pong(agent, ctype, count, card)
            elif ctype==3:
                count = other_agent.bamb_list.count(card)
                if count>1:
                    rtv = other_agent.pong(agent, ctype, count, card)
            elif ctype==4:
                count = other_agent.word_list.count(card)
                if count>1:
                    rtv = other_agent.pong(agent, ctype, count, card)
            elif ctype==5:
                count = other_agent.wind_list.count(card)
                if count>1:
                    rtv = other_agent.pong(agent, ctype, count, card)
                
            if rtv: # 有人碰
                self.play_turn = (self.aget_list.index(other_agent)+1) % len(self.aget_list)
                self.disCard(other_agent, rtv)                    
                return
                        

        # 下家可以決定要不要吃牌
        next_agent = self.aget_list[(self.aget_list.index(agent)+1) % len(self.aget_list)]
        #print("\t[Test] next agent={0}...".format(next_agent.name))
        ctype = GameBoard.CardType(card)
        eat_list = []
        rtv = None # 吃牌後放棄的牌
        if ctype==1:
            if card == '1萬' and \
               ('2萬' in next_agent.wang_list) and \
               ('3萬' in next_agent.wang_list):
                eat_list.append((['2萬', '3萬'], ['1萬', '2萬', '3萬']))
            elif card == '9萬' and \
               ('7萬' in next_agent.wang_list) and \
               ('8萬' in next_agent.wang_list):
                eat_list.append((['7萬', '8萬'], ['7萬', '8萬', '9萬']))                
            elif card == '2萬':
                if {'1萬', '3萬'} < set(next_agent.wang_list):
                    eat_list.append((['1萬', '3萬'], ['1萬', '2萬', '3萬']))
                if {'3萬', '4萬'} < set(next_agent.wang_list):         
                    eat_list.append((['3萬', '4萬'], ['2萬', '3萬', '4萬']))
            elif card == '8萬':
                if {'7萬', '9萬'} < set(next_agent.wang_list):
                    eat_list.append((['7萬', '9萬'], ['7萬', '8萬', '9萬']))                    
                if {'6萬', '7萬'} < set(next_agent.wang_list):
                    eat_list.append((['6萬', '7萬'], ['6萬', '7萬', '8萬']))                     
            elif card == '3萬':
                if {'1萬', '2萬'} < set(next_agent.wang_list):
                    eat_list.append((['1萬', '2萬'], ['1萬', '2萬', '3萬']))                     
                if {'2萬', '4萬'} < set(next_agent.wang_list):
                    eat_list.append((['2萬', '4萬'], ['2萬', '3萬', '4萬'])) 
                if {'4萬', '5萬'} < set(next_agent.wang_list):
                    eat_list.append((['4萬', '5萬'], ['3萬', '4萬', '5萬']))          
            elif card == '4萬':
                if {'2萬', '3萬'} < set(next_agent.wang_list):
                    eat_list.append((['2萬', '3萬'], ['2萬', '3萬', '4萬']))                     
                if {'3萬', '5萬'} < set(next_agent.wang_list):
                    eat_list.append((['3萬', '5萬'], ['3萬', '4萬', '5萬']))                       
                if {'5萬', '6萬'} < set(next_agent.wang_list):
                    eat_list.append((['5萬', '6萬'], ['4萬', '5萬', '6萬']))                     
            elif card == '5萬':
                if {'3萬', '4萬'} < set(next_agent.wang_list):
                    eat_list.append((['3萬', '4萬'], ['3萬', '4萬', '5萬']))                       
                if {'4萬', '6萬'} < set(next_agent.wang_list):
                    eat_list.append((['4萬', '6萬'], ['4萬', '5萬', '6萬']))                       
                if {'6萬', '7萬'} < set(next_agent.wang_list):
                    eat_list.append((['6萬', '7萬'], ['5萬', '6萬', '7萬']))                    
            elif card == '6萬':
                if {'4萬', '5萬'} < set(next_agent.wang_list):
                    eat_list.append((['4萬', '5萬'], ['4萬', '5萬', '6萬']))                     
                if {'5萬', '7萬'} < set(next_agent.wang_list):
                    eat_list.append((['5萬', '7萬'], ['5萬', '6萬', '7萬']))                    
                if {'7萬', '8萬'} < set(next_agent.wang_list):
                    eat_list.append((['7萬', '8萬'], ['6萬', '7萬', '8萬']))                       
            elif card == '7萬':
                if {'5萬', '6萬'} < set(next_agent.wang_list):
                    eat_list.append((['5萬', '6萬'], ['5萬', '6萬', '7萬']))                      
                if {'6萬', '8萬'} < set(next_agent.wang_list):
                    eat_list.append((['6萬', '8萬'], ['6萬', '7萬', '8萬']))                     
                if {'8萬', '9萬'} < set(next_agent.wang_list):
                    eat_list.append((['8萬', '9萬'], ['7萬', '8萬', '9萬']))
            if len(eat_list) > 0:
                rtv = next_agent.eat(agent, card, ctype, eat_list)
                
        elif ctype==2:
            if card == '1筒' and \
               ('2筒' in next_agent.tube_list) and \
               ('3筒' in next_agent.tube_list):
                eat_list.append((['2筒', '3筒'], ['1筒', '2筒', '3筒']))
            elif card == '9筒' and \
               ('7筒' in next_agent.tube_list) and \
               ('8筒' in next_agent.tube_list):
                eat_list.append((['7筒', '8筒'], ['7筒', '8筒', '9筒']))                
            elif card == '2筒':
                if {'1筒', '3筒'} < set(next_agent.tube_list):
                    eat_list.append((['1筒', '3筒'], ['1筒', '2筒', '3筒']))
                if {'3筒', '4筒'} < set(next_agent.tube_list):         
                    eat_list.append((['3筒', '4筒'], ['2筒', '3筒', '4筒']))
            elif card == '8筒':
                if {'7筒', '9筒'} < set(next_agent.tube_list):
                    eat_list.append((['7筒', '9筒'], ['7筒', '8筒', '9筒']))                    
                if {'6筒', '7筒'} < set(next_agent.tube_list):
                    eat_list.append((['6筒', '7筒'], ['6筒', '7筒', '8筒']))                     
            elif card == '3筒':
                if {'1筒', '2筒'} < set(next_agent.tube_list):
                    eat_list.append((['1筒', '2筒'], ['1筒', '2筒', '3筒']))                     
                if {'2筒', '4筒'} < set(next_agent.tube_list):
                    eat_list.append((['2筒', '4筒'], ['2筒', '3筒', '4筒'])) 
                if {'4筒', '5筒'} < set(next_agent.tube_list):
                    eat_list.append((['4筒', '5筒'], ['3筒', '4筒', '5筒']))          
            elif card == '4筒':
                if {'2筒', '3筒'} < set(next_agent.tube_list):
                    eat_list.append((['2筒', '3筒'], ['2筒', '3筒', '4筒']))                     
                if {'3筒', '5筒'} < set(next_agent.tube_list):
                    eat_list.append((['3筒', '5筒'], ['3筒', '4筒', '5筒']))                       
                if {'5筒', '6筒'} < set(next_agent.tube_list):
                    eat_list.append((['5筒', '6筒'], ['4筒', '5筒', '6筒']))                     
            elif card == '5筒':
                if {'3筒', '4筒'} < set(next_agent.tube_list):
                    eat_list.append((['3筒', '4筒'], ['3筒', '4筒', '5筒']))                       
                if {'4筒', '6筒'} < set(next_agent.tube_list):
                    eat_list.append((['4筒', '6筒'], ['4筒', '5筒', '6筒']))                       
                if {'6筒', '7筒'} < set(next_agent.tube_list):
                    eat_list.append((['6筒', '7筒'], ['5筒', '6筒', '7筒']))                    
            elif card == '6筒':
                if {'4筒', '5筒'} < set(next_agent.tube_list):
                    eat_list.append((['4筒', '5筒'], ['4筒', '5筒', '6筒']))                     
                if {'5筒', '7筒'} < set(next_agent.tube_list):
                    eat_list.append((['5筒', '7筒'], ['5筒', '6筒', '7筒']))                    
                if {'7筒', '8筒'} < set(next_agent.tube_list):
                    eat_list.append((['7筒', '8筒'], ['6筒', '7筒', '8筒']))                       
            elif card == '7筒':
                if {'5筒', '6筒'} < set(next_agent.tube_list):
                    eat_list.append((['5筒', '6筒'], ['5筒', '6筒', '7筒']))                      
                if {'6筒', '8筒'} < set(next_agent.tube_list):
                    eat_list.append((['6筒', '8筒'], ['6筒', '7筒', '8筒']))                     
                if {'8筒', '9筒'} < set(next_agent.tube_list):
                    eat_list.append((['8筒', '9筒'], ['7筒', '8筒', '9筒']))
            if len(eat_list) > 0:
                rtv = next_agent.eat(agent, card, ctype, eat_list)
            
        elif ctype==3:
            if card == '1條' and \
               ('2條' in next_agent.bamb_list) and \
               ('3條' in next_agent.bamb_list):
                eat_list.append((['2條', '3條'], ['1條', '2條', '3條']))
            elif card == '9條' and \
               ('7條' in next_agent.bamb_list) and \
               ('8條' in next_agent.bamb_list):
                eat_list.append((['7條', '8條'], ['7條', '8條', '9條']))                
            elif card == '2條':
                if {'1條', '3條'} < set(next_agent.bamb_list):
                    eat_list.append((['1條', '3條'], ['1條', '2條', '3條']))
                if {'3條', '4條'} < set(next_agent.bamb_list):         
                    eat_list.append((['3條', '4條'], ['2條', '3條', '4條']))
            elif card == '8條':
                if {'7條', '9條'} < set(next_agent.bamb_list):
                    eat_list.append((['7條', '9條'], ['7條', '8條', '9條']))                    
                if {'6條', '7條'} < set(next_agent.bamb_list):
                    eat_list.append((['6條', '7條'], ['6條', '7條', '8條']))                     
            elif card == '3條':
                if {'1條', '2條'} < set(next_agent.bamb_list):
                    eat_list.append((['1條', '2條'], ['1條', '2條', '3條']))                     
                if {'2條', '4條'} < set(next_agent.bamb_list):
                    eat_list.append((['2條', '4條'], ['2條', '3條', '4條'])) 
                if {'4條', '5條'} < set(next_agent.bamb_list):
                    eat_list.append((['4條', '5條'], ['3條', '4條', '5條']))          
            elif card == '4條':
                if {'2條', '3條'} < set(next_agent.bamb_list):
                    eat_list.append((['2條', '3條'], ['2條', '3條', '4條']))                     
                if {'3條', '5條'} < set(next_agent.bamb_list):
                    eat_list.append((['3條', '5條'], ['3條', '4條', '5條']))                       
                if {'5條', '6條'} < set(next_agent.bamb_list):
                    eat_list.append((['5條', '6條'], ['4條', '5條', '6條']))                     
            elif card == '5條':
                if {'3條', '4條'} < set(next_agent.bamb_list):
                    eat_list.append((['3條', '4條'], ['3條', '4條', '5條']))                       
                if {'4條', '6條'} < set(next_agent.bamb_list):
                    eat_list.append((['4條', '6條'], ['4條', '5條', '6條']))                       
                if {'6條', '7條'} < set(next_agent.bamb_list):
                    eat_list.append((['6條', '7條'], ['5條', '6條', '7條']))                    
            elif card == '6條':
                if {'4條', '5條'} < set(next_agent.bamb_list):
                    eat_list.append((['4條', '5條'], ['4條', '5條', '6條']))                     
                if {'5條', '7條'} < set(next_agent.bamb_list):
                    eat_list.append((['5條', '7條'], ['5條', '6條', '7條']))                    
                if {'7條', '8條'} < set(next_agent.bamb_list):
                    eat_list.append((['7條', '8條'], ['6條', '7條', '8條']))                       
            elif card == '7條':
                if {'5條', '6條'} < set(next_agent.bamb_list):
                    eat_list.append((['5條', '6條'], ['5條', '6條', '7條']))                      
                if {'6條', '8條'} < set(next_agent.bamb_list):
                    eat_list.append((['6條', '8條'], ['6條', '7條', '8條']))                     
                if {'8條', '9條'} < set(next_agent.bamb_list):
                    eat_list.append((['8條', '9條'], ['7條', '8條', '9條']))
            if len(eat_list) > 0:
                rtv = next_agent.eat(agent, card, ctype, eat_list)
        
        if not rtv:
            self.drop_list.append(card)   # 不吃牌,則該牌進海底
            self.play_turn = self.aget_list.index(next_agent)
        else:
            self.disCard(next_agent, rtv) # 吃牌後丟一張牌
            #self.play_turn = (self.aget_list.index(next_agent)+1) % len(self.aget_list) # 吃牌則輪到下家
            #self.disCard(next_agent, rtv) 

    # 抽牌    
    def drawCard(self):
        if self.card_count > 0:
            bb_list = []
            if len(self.bamb_list)>0:
                for i in range(len(self.bamb_list)): bb_list.append(self.bamb_list)
            if len(self.wang_list)>0:
                for i in range(len(self.wang_list)): bb_list.append(self.wang_list)
            if len(self.tube_list)>0:
                for i in range(len(self.tube_list)): bb_list.append(self.tube_list)
            if len(self.flow_list)>0:
                for i in range(len(self.flow_list)): bb_list.append(self.flow_list)                
            if len(self.word_list)>0:
                for i in range(len(self.word_list)): bb_list.append(self.word_list)
            if len(self.wind_list)>0:
                for i in range(len(self.wind_list)): bb_list.append(self.wind_list)
            c_list = bb_list[random.randint(0, len(bb_list)-1)]
            p_idx = random.randint(0, len(c_list)-1)
            self.card_count-=1
            return c_list.pop(p_idx)        

    # 洗牌
    def shuffle(self):
        """ Shuffle. (洗牌)
        1. Clear all cards in sea bed(海底)
        2. Refill the card lists of gameboard. (砌牌)
        3. Clear drop history of each agent.
        4. Reset all agent
           4.1 Call API:clean() of each agent.
           4.2 Reset agent.win_card
           4.3 Clear agent.pong_list
        """
        del self.drop_list[:]
        self.win_agent = None
        del self.wind_list[:]
        self.wind_list.append('東')
        self.wind_list.append('西')
        self.wind_list.append('南')
        self.wind_list.append('北')
        self.wind_list = self.wind_list * 4
        self.wind_list.sort()
        del self.word_list[:]
        self.word_list.append('中')
        self.word_list.append('發')
        self.word_list.append('白')
        self.word_list = self.word_list * 4
        self.word_list.sort()
        del self.flow_list[:]
        self.flow_list.append('松')
        self.flow_list.append('蘭')
        self.flow_list.append('竹')
        self.flow_list.append('菊')
        self.flow_list.append('春')
        self.flow_list.append('夏')
        self.flow_list.append('秋')
        self.flow_list.append('冬')
        del self.wang_list[:]
        self.wang_list.append('1萬')
        self.wang_list.append('2萬')
        self.wang_list.append('3萬')
        self.wang_list.append('4萬')
        self.wang_list.append('5萬')
        self.wang_list.append('6萬')
        self.wang_list.append('7萬')
        self.wang_list.append('8萬')
        self.wang_list.append('9萬')
        self.wang_list = self.wang_list * 4
        self.wang_list.sort()
        del self.bamb_list[:]
        self.bamb_list.append('1條')
        self.bamb_list.append('2條')
        self.bamb_list.append('3條')
        self.bamb_list.append('4條')
        self.bamb_list.append('5條')
        self.bamb_list.append('6條')
        self.bamb_list.append('7條')
        self.bamb_list.append('8條')
        self.bamb_list.append('9條')
        self.bamb_list = self.bamb_list * 4
        self.bamb_list.sort()
        del self.tube_list[:]
        self.tube_list.append("1筒")
        self.tube_list.append("2筒")
        self.tube_list.append("3筒")
        self.tube_list.append("4筒")
        self.tube_list.append("5筒")
        self.tube_list.append("6筒")
        self.tube_list.append("7筒")
        self.tube_list.append("8筒")
        self.tube_list.append("9筒")
        self.tube_list = self.tube_list * 4
        self.tube_list.sort()
        self.drop_record.clear()
        self.card_count = len(self.wang_list) + len(self.bamb_list) + len(self.tube_list) + \
                          len(self.flow_list) + len(self.word_list) + len(self.wind_list)
        for agent in self.aget_list:
            agent.clean()
            #agent.win = False
            agent.win_card = None            
            del agent.pong_list[:]
            #print(agent)

class Agent(object):
    def __init__(self, name, gb):
        self.win = 0
        self.win_by_draw = 0
        self.lose = 0
        self.name = name
        self.gb = gb
        self.bamb_list = []
        self.wang_list = []
        self.tube_list = []
        self.flow_list = []
        self.word_list = []
        self.wind_list = []
        self.aget_list = []
        self.pong_list = []
        self.card_count = 0
        self.win_card = None
        self.debug = False
        gb.appendAgent(self)

    def dprint(self, msg_str):
        if self.debug:
            print(msg_str)

    # Drop all cards in hand
    def clean(self):
        del self.bamb_list[:]
        del self.wang_list[:]
        del self.tube_list[:]
        del self.flow_list[:]
        del self.word_list[:]
        del self.wind_list[:]
        del self.aget_list[:]
        del self.pong_list[:]
        self.card_count = 0
        
    # 抽牌
    def draw(self, keep=False):
        card = self.gb.drawCard()
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            self.dprint("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
            return
        self.dprint("\t[Test] {0} draw {1}...".format(self.name, card))
        ctype = GameBoard.CardType(card)
        if ctype==1:
            self.wang_list.append(card)            
            self.wang_list.sort()
            self.card_count+=1
        elif ctype==2:
            self.tube_list.append(card)
            self.tube_list.sort()
            self.card_count+=1
        elif ctype==3:
            self.bamb_list.append(card)
            self.bamb_list.sort()
            self.card_count+=1
        elif ctype==4:
            self.word_list.append(card)
            self.word_list.sort()
            self.card_count+=1
        elif ctype==5:
            self.wind_list.append(card)
            self.wind_list.sort()
            self.card_count+=1
        else:
            self.flow_list.append(card)
            self.flow_list.sort()
            return self.draw()

        dcard = None
        if not keep:
            dcard = self.drop()
            self.dprint("\t[Test] {0} drop {1}...".format(self.name, dcard))
            #self.gb.disCard(self, dcard)
        return dcard

    # 放棄手上一張牌
    def drop(self):
        card = ''
        if len(self.word_list)>0:
            card = self.word_list.pop()
        if (not card) and len(self.wind_list)>0:
            card = self.wind_list.pop()
        if (not card) and len(self.tube_list)>0:
            card = self.tube_list.pop()
        if (not card) and len(self.wang_list)>0:
            card = self.wang_list.pop()
        if (not card) and len(self.bamb_list)>0:
            card = self.bamb_list.pop()
        self.card_count-=1
        return card
    
    def _pong(self, c_list, count, card):        
        for i in range(count+1):
            self.pong_list.append(card)
            
        for i in range(count):
            c_list.remove(card)
            self.card_count-=1
        
        if count==2:
            dcard = self.drop()
            self.dprint("\t[Test] {0}: Pong '{1}' and drop {2}!".format(self.name, card, dcard))
            #self.gb.disCard(self, dcard)
            return dcard
        else:
            self.dprint("\t[Test] {0}: Gang '{1}'!".format(self.name, card))
            return self.draw(keep=False)
        
    # 碰! A callback by GameBoard. Return drop card or redraw card if you want.    
    def pong(self, agent, ctype, count, card):
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win+=1
            agent.close+=1
            self.dprint("\t[Test] Agent({0}) 碰胡 {1}!!".format(self.name, card))
            return
        
        # Greedy algorithm: Always pong!
        if ctype==1:
            return self._pong(self.wang_list, count, card)                
        elif ctype==2:
            return self._pong(self.tube_list, count, card)                
        elif ctype==3:
            return self._pong(self.bamb_list, count, card)                
        elif ctype==4:
            return self._pong(self.word_list, count, card)                
        elif ctype==5:
            return self._pong(self.wind_list, count, card)
                

    def _eat(self, olist, dlist, elist):
        self.pong_list.extend(elist)
        for e in dlist:
            olist.remove(e)
            self.card_count-=1
        dcard = self.drop()
        self.dprint("\t[Test] {0}: Eat '{1}' and drop {2}!".format(self.name, toCListStr(elist), dcard))
        #self.gb.disCard(self, dcard)
        return dcard

    # 吃牌. Callback by GameBoard
    def eat(self, agent, card, ctype, eat_list):
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win+=1
            agent.lose+=1
            self.dprint("\t[Test] Agent({0}) 吃胡 {1}!".format(self.name, card))
            return
        # Greedy algorithm: Always eat from the first choice
        if ctype==1:
            return self._eat(self.wang_list, eat_list[0][0], eat_list[0][1])
        elif ctype==2:
            return self._eat(self.tube_list, eat_list[0][0], eat_list[0][1])
        elif ctype==3:
            return self._eat(self.bamb_list, eat_list[0][0], eat_list[0][1])

    # 將牌放入
    def _feedCard(self, card):
        ctype = GameBoard.CardType(card)
        if ctype==1:
            self.wang_list.append(card)
            self.wang_list.sort()
            self.card_count+=1
            return True
        elif ctype==2:
            self.tube_list.append(card)
            self.tube_list.sort()
            self.card_count+=1
            return True
        elif ctype==3:
            self.bamb_list.append(card)
            self.bamb_list.sort()
            self.card_count+=1
            return True
        elif ctype==4:
            self.word_list.append(card)
            self.word_list.sort()
            self.card_count+=1
            return True
        elif ctype==5:
            self.wind_list.append(card)
            self.wind_list.sort()
            self.card_count+=1
            return True
        else:
            self.flow_list.append(card)
            self.flow_list.sort()

    def handleGang(self):
        drawFlag = False
        if len(self.wang_list)>3:
            for e in set(self.wang_list):
                if self.wang_list.count(e)==4:
                    self.pong_list.extend([e]*4)
                    while e in self.wang_list:
                        self.wang_list.remove(e)
                        self.card_count-=1
                    while not self._feedCard(self.gb.drawCard()):
                        pass # 直到抽到不是花牌
                    self.wang_list.sort()
                    drawFlag=True
        if len(self.tube_list)>3:
            for e in set(self.tube_list):
                if self.tube_list.count(e)==4:
                    self.pong_list.extend([e]*4)
                    while e in self.tube_list:
                        self.tube_list.remove(e)
                        self.card_count-=1
                    while not self._feedCard(self.gb.drawCard()):
                        pass # 直到抽到不是花牌
                    self.tube_list.sort()
                    drawFlag=True
        if len(self.bamb_list)>3:
            for e in set(self.bamb_list):
                if self.bamb_list.count(e)==4:
                    self.pong_list.extend([e]*4)
                    while e in self.bamb_list:
                        self.bamb_list.remove(e)
                        self.card_count-=1
                    while not self._feedCard(self.gb.drawCard()):
                        pass # 直到抽到不是花牌
                    self.bamb_list.sort()
                    drawFlag=True
        if len(self.word_list)>3:
            for e in set(self.word_list):
                if self.word_list.count(e)==4:
                    self.pong_list.extend([e]*4)
                    while e in self.word_list:
                        self.word_list.remove(e)
                        self.card_count-=1
                    while not self._feedCard(self.gb.drawCard()):
                        pass # 直到抽到不是花牌
                    self.word_list.sort()
                    drawFlag=True
        if len(self.wind_list)>3:
            for e in set(self.wind_list):
                if self.wind_list.count(e)==4:
                    self.pong_list.extend([e]*4)
                    while e in self.wind_list:
                        self.wind_list.remove(e)
                        self.card_count-=1
                    while not self._feedCard(self.gb.drawCard()):
                        pass # 直到抽到不是花牌
                    self.wind_list.sort()
                    drawFlag=True
        if drawFlag:
            self.handleGang()
            
    # 發牌        
    def assignCard(self):
        # 抽滿 16 張牌(扣掉花牌)
        while self.card_count < 16:
            card = self.gb.drawCard()
            self._feedCard(card)
                
        # 處理槓牌
        self.handleGang()
                    
            
    def __str__(self):
        self_str = "{0}({1}/{2}/{3}): [".format(self.name, self.win_by_draw, self.win, self.lose)
        for card in self.wang_list:
            self_str+="{0} ".format(card)
        for card in self.tube_list:
            self_str+="{0} ".format(card)
        for card in self.bamb_list:
            self_str+="{0} ".format(card)
        for card in self.word_list:
            self_str+="{0} ".format(card)
        for card in self.wind_list:
            self_str+="{0} ".format(card)    
        self_str = "{0}]".format(self_str)
        if len(self.flow_list) > 0:
            self_str+=" / [ "
            for card in self.flow_list:
                self_str+="{0} ".format(card)
            self_str+="]"
        else:
            self_str+=" / []"
        if len(self.pong_list) > 0:
            self_str+=" / [ "
            for card in self.pong_list:
                self_str+="{0} ".format(card)
            self_str+="]"
        else:
            self_str+=" / []"
        if self.win_card:
            self_str+=" -> {0}".format(self.win_card)
        return self_str           


# 2) Testing code
##gb = GameBoard()
##agent1 = Agent('Robot1', gb)
##agent2 = Agent('Robot2', gb)
##agent3 = Agent('Robot3', gb)
##agent4 = Agent('Self', gb)
##for i in range(50):
##    print("\t[Info] Play!")
##    gb.play()
##    print("\t[Info] 海底={0}".format(gb.drop_list))
##    print("\t[Info] Drop record:\n{0}".format(gb.drop_record))
##    print("\t[Info] Wash board")

