#-*- coding: utf-8 -*-
from GameBoard import *
from Algorithm import *
import SmartAgent

class JAgent(SmartAgent.Agent):
    def hu(self, card):
        """ Callback by Gameboard to inform winning. (Not necessary API for Agent)"""
        print("\t[Test] Agent({0}) 胡牌! ({1})".format(self, card))

##    def eat(self, agent, card, ctype, eat_list):
##        if GameBoard.GoalState(self, card): # Check goal state
##            self.gb.win_agent = self
##            self.win_card = card
##            self.win+=1
##            agent.lose+=1
##            self.dprint("\t[Test] Agent({0}) 吃胡 {1}!".format(self.name, card))
##            return
##        sol_tuple = None
##        if ctype==1:
##            clist = self.wang_list[:]
##            clist.append(card)
##            sol_tuple = SearchBestWinTileCompost(clist, self.gb.awang_list(), \
##                                                 self.tube_list, self.gb.atube_list(), \
##                                                 self.bamb_list, self.gb.abamb_list(), \
##                                                 self.word_list, self.gb.aword_list(), \
##                                                 self.wind_list, self.gb.awind_list())
##        elif ctype==2:
##            clist = self.tube_list[:]
##            clist.append(card)
##            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
##                                                 clist, self.gb.atube_list(), \
##                                                 self.bamb_list, self.gb.abamb_list(), \
##                                                 self.word_list, self.gb.aword_list(), \
##                                                 self.wind_list, self.gb.awind_list())
##        elif ctype==3:
##            clist = self.bamb_list[:]
##            clist.append(card)
##            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
##                                                 self.tube_list, self.gb.atube_list(), \
##                                                 clist, self.gb.abamb_list(), \
##                                                 self.word_list, self.gb.aword_list(), \
##                                                 self.wind_list, self.gb.awind_list())
##        elif ctype==4:
##            clist = self.word_list[:]
##            clist.append(card)
##            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
##                                                 self.tube_list, self.gb.atube_list(), \
##                                                 self.bamb_list, self.gb.abamb_list(), \
##                                                 clist, self.gb.aword_list(), \
##                                                 self.wind_list, self.gb.awind_list())
##        elif ctype==5:
##            clist = self.wind_list[:]
##            clist.append(card)
##            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
##                                                 self.tube_list, self.gb.atube_list(), \
##                                                 self.bamb_list, self.gb.abamb_list(), \
##                                                 self.word_list, self.gb.aword_list(), \
##                                                 clist, self.gb.awind_list())
##        
##        # 如果吃的牌在 suggest eat list 中則吃.
##        if not sol_tuple or card in sol_tuple[2]:
##            if ctype==1:
##                return self._eat(self.wang_list, eat_list[0][0], eat_list[0][1])
##            elif ctype==2:
##                return self._eat(self.tube_list, eat_list[0][0], eat_list[0][1])
##            elif ctype==3:
##                return self._eat(self.bamb_list, eat_list[0][0], eat_list[0][1])
            

    def pong(self, agent, ctype, count, card):
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win+=1
            agent.close+=1
            self.dprint("\t[Test] Agent({0}) 碰胡 {1}!!".format(self.name, card))
            return
        sol_tuple = None
        if ctype==1:
            clist = self.wang_list[:]
            clist.append(card)
            sol_tuple = SearchBestWinTileCompost(clist, self.gb.awang_list(), \
                                                 self.tube_list, self.gb.atube_list(), \
                                                 self.bamb_list, self.gb.abamb_list(), \
                                                 self.word_list, self.gb.aword_list(), \
                                                 self.wind_list, self.gb.awind_list())
        elif ctype==2:
            clist = self.tube_list[:]
            clist.append(card)
            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
                                                 clist, self.gb.atube_list(), \
                                                 self.bamb_list, self.gb.abamb_list(), \
                                                 self.word_list, self.gb.aword_list(), \
                                                 self.wind_list, self.gb.awind_list())
        elif ctype==3:
            clist = self.bamb_list[:]
            clist.append(card)
            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
                                                 self.tube_list, self.gb.atube_list(), \
                                                 clist, self.gb.abamb_list(), \
                                                 self.word_list, self.gb.aword_list(), \
                                                 self.wind_list, self.gb.awind_list())
        elif ctype==4:
            clist = self.word_list[:]
            clist.append(card)
            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
                                                 self.tube_list, self.gb.atube_list(), \
                                                 self.bamb_list, self.gb.abamb_list(), \
                                                 clist, self.gb.aword_list(), \
                                                 self.wind_list, self.gb.awind_list())
        elif ctype==5:
            clist = self.wind_list[:]
            clist.append(card)
            sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
                                                 self.tube_list, self.gb.atube_list(), \
                                                 self.bamb_list, self.gb.abamb_list(), \
                                                 self.word_list, self.gb.aword_list(), \
                                                 clist, self.gb.awind_list())

        # 1. 碰的牌沒有在 drop list 裡就碰
        # 2. 還沒有機會快速聽牌, 能碰就碰.
        if not sol_tuple or not card in sol_tuple[1]:
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
        

    def drop(self):
        """ Drop card from hand. (Overwrite)
        This API will implement the algorithm to deside the dropped card. It will be called during game when necessary.
        Agent is responsible for removing dropped card from hand when make decision.
        Different from extended class, JAgent define its' dropping algorithm:
        1. Call API:SearchBestWinTileCompost(Algorithm.py) to retrieve suggest dropped card list. 
        2. From dropped card list:
           2.1 字/風 牌先丟.
           2.2 下家最近一次丟過的牌先丟. (避免被吃)
           2.3 上家最近一次丟過的牌先丟. (避免被胡)
           2.4 隨便從 suggest dropped card list 挑一張丟.
        * Return
          Dropped card which being removed from hand.
        """
        sol_tuple = SearchBestWinTileCompost(self.wang_list, self.gb.awang_list(), \
                                             self.tube_list, self.gb.atube_list(), \
                                             self.bamb_list, self.gb.abamb_list(), \
                                             self.word_list, self.gb.aword_list(), \
                                             self.wind_list, self.gb.awind_list()) 
        if sol_tuple:
            #print("\t[Test] Drop suggestion: {0}->{1}".format(toCListStr(sol_tuple[1]), self))
            for t in self.gb.fwind_list:
                if t in sol_tuple[1]:
                    self.wind_list.remove(t)
                    return t
            for t in self.gb.fword_list:
                if t in sol_tuple[1]:
                    self.word_list.remove(t)
                    return t
            for t in sol_tuple[1]:
                ct = GameBoard.CardType(t)
                if ct == 1 and len(self.wang_list) == 1:
                    self.wang_list.remove(t)
                    return t
                elif ct == 2 and len(self.tube_list) == 1:
                    self.tube_list.remove(t)
                    return t
                elif ct == 3 and len(self.bamb_list) == 1:
                    self.bamb_list.remove(t)
                    return t

            # 下家丟過先丟
            rightAgt = self.gb.rightOpponent(self)
            if rightAgt and rightAgt.name in self.gb.drop_record and len(self.gb.drop_record[rightAgt.name]) > 0:
                right_drop_tile = self.gb.drop_record[rightAgt.name][-1]
                if right_drop_tile in sol_tuple[1]:
                    ct = GameBoard.CardType(right_drop_tile)
                    if ct == 1:
                        self.wang_list.remove(right_drop_tile)
                    elif ct == 2:
                        self.tube_list.remove(right_drop_tile)
                    else:
                        self.bamb_list.remove(right_drop_tile)
                    return right_drop_tile
            # 上家丟過先丟
            leftAgt = self.gb.leftOpponent(self)
            if leftAgt and leftAgt.name in self.gb.drop_record and len(self.gb.drop_record[leftAgt.name]) > 0:
                left_drop_tile = self.gb.drop_record[leftAgt.name][-1]
                if left_drop_tile in sol_tuple[1]:
                    ct = GameBoard.CardType(left_drop_tile)
                    if ct == 1:
                        self.wang_list.remove(left_drop_tile)
                    elif ct == 2:
                        self.tube_list.remove(left_drop_tile)
                    else:
                        self.bamb_list.remove(left_drop_tile)
                    return left_drop_tile
                
            # 邊張的先丟
            for t in sol_tuple[1]:
                if t.startswith('1') or t.startswith('9'):
                    ct = GameBoard.CardType(t)
                    if ct == 1:
                        self.wang_list.remove(t)
                    elif ct == 2:
                        self.tube_list.remove(t)
                    else:
                        self.bamb_list.remove(t)
                    return t

            # 隨便丟一張
            ct = GameBoard.CardType(sol_tuple[1][0])
            if ct == 1:
                self.wang_list.remove(sol_tuple[1][0])
            elif ct == 2:
                self.tube_list.remove(sol_tuple[1][0])
            else:
                self.bamb_list.remove(sol_tuple[1][0])
            #print('\t[Test] After={0}'.format(self.__str__()))
            return sol_tuple[1][0]
        
        # Use basic rule to drop card
        card = ''
        # 1. 只有獨張的風牌或中發白就丟.
        if (not card) and len(self.word_list) == 1:
            card = self.word_list.pop()
            self.card_count-=1
            return card
        else:
            for c in set(self.word_list):
                if self.word_list.count(c)==1:
                    self.word_list.remove(c)
                    self.card_count-=1
                    return c

        if (not card) and len(self.wind_list) == 1:
            card = self.wind_list.pop()
            self.card_count-=1
            return card
        else:
            for c in set(self.wind_list):
                if self.wind_list.count(c)==1:
                    self.wind_list.remove(c)
                    self.card_count-=1
                    return c
        
        # 2. 下家丟過先丟
        rightAgt = self.gb.rightOpponent(self)
        if rightAgt.name in self.gb.drop_record and len(self.gb.drop_record[rightAgt.name]) > 0:
            dc = self.gb.drop_record[rightAgt.name][-1]
            ct = GameBoard.CardType(dc)
            if ct == 1 and dc in self.wang_list:
                self.wang_list.remove(dc)
                self.card_count-=1
                return dc
            elif ct == 2 and dc in self.tube_list:
                self.tube_list.remove(dc)
                self.card_count-=1
                return dc
            elif ct == 3 and dc in self.bamb_list:
                self.bamb_list.remove(dc)
                self.card_count-=1
                return dc
            elif ct == 4 and dc in self.word_list:
                self.word_list.remove(dc)
                self.card_count-=1
                return dc
            elif ct == 5 and dc in self.wind_list:
                self.wind_list.remove(dc)
                self.card_count-=1
                return dc

        # 3. 任意丟一張 萬/筒/條
        if (not card) and len(self.tube_list)>0:
            card = self.tube_list.pop()
            self.card_count-=1
            return card
        if (not card) and len(self.wang_list)>0:
            card = self.wang_list.pop()
            self.card_count-=1
            return card
        if (not card) and len(self.bamb_list)>0:
            card = self.bamb_list.pop()
            self.card_count-=1
            return card
    
    def draw(self, keep=False):
        """ Draw card. (Overwrite)
        Gameboard will call this API to informat agent to draw card. Here should be responsible for:
        1. Call API:drawCard() from GameBoard object to draw card.
        2. Add drawn card into hand.
        3. Return card as dropped card. (In general, you will call API:drop() for dropped card)
        * Return:
          Dropped card."""
        card = self.gb.drawCard()
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            print("\t[Test] Agent({0}) 自摸 {1}!".format(self, card))
            return

        prewin_tiles = GameBoard.PreWinTiles(self)
        if card in prewin_tiles:
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            print("\t[Test] Agent({0}) 自摸 {1}! (wrong here)".format(self, card))
            self.wrong=False
            print("\t[Test] {0}".format(self.__str__()))
            return

        if len(prewin_tiles) > 0:
            self.pwin_flag = True
            for tile in prewin_tiles:
                ctype = GameBoard.CardType(tile)
                if ctype == 1:
                    if not tile in self.gb.wang_list:
                        self.pwin_flag = False
                        break
                elif ctype == 2:
                    if not tile in self.gb.tube_list:
                        self.pwin_flag = False
                        break
                elif ctype == 3:
                    if tile in self.gb.bamb_list:
                        self.pwin_flag = False
                        break
                elif ctype == 4:
                    if tile in self.gb.word_list:
                        self.pwin_flag = False
                        break
                elif ctype == 5:
                    if tile in self.gb.wind_list:
                        self.pwin_flag = False
                        break
            if self.pwin_flag:
                return card

        #print("\t[Test] {0} draw {1}:{2}...".format(self.name, card, self.__str__()))
        ctype = GameBoard.CardType(card)
        if ctype==1:
            if self.wang_list.count(card)==3: # 確認槓牌
                self._kong(ctype, card)
                return self.draw()
            self.wang_list.append(card)
            self.wang_list.sort()
            self.card_count+=1
        elif ctype==2:
            if self.tube_list.count(card)==3: # 確認槓牌
                self._kong(ctype, card)
                return self.draw()
            self.tube_list.append(card)
            self.tube_list.sort()
            self.card_count+=1
        elif ctype==3:
            if self.bamb_list.count(card)==3: # 確認槓牌
                self._kong(ctype, card)
                return self.draw()
            self.bamb_list.append(card)
            self.bamb_list.sort()
            self.card_count+=1
        elif ctype==4:
            if self.word_list.count(card)==3: # 確認槓牌
                self._kong(ctype, card)
                return self.draw()
            self.word_list.append(card)
            self.word_list.sort()
            self.card_count+=1
        elif ctype==5:
            if self.wind_list.count(card)==3: # 確認槓牌
                self._kong(ctype, card)
                return self.draw()
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
            #print("\t[Test] {0} drop {1}...".format(self.name, dcard))
            #self.gb.disCard(self, dcard)
        return dcard
    
    def __str__(self):
        self_str = "*{0}*({1}/{2}/{3}): [".format(self.name, self.win_by_draw, self.win, self.lose)
        for card in self.wang_list:
            self_str+="{0} ".format(card)
        self_str+="|"
        for card in self.tube_list:
            self_str+="{0} ".format(card)
        self_str+="|"
        for card in self.bamb_list:
            self_str+="{0} ".format(card)
        self_str+="|"
        for card in self.word_list:
            self_str+="{0} ".format(card)
        self_str+="|"
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
        else:
            prewin_tiles = GameBoard.PreWinTiles(self)
            if len(prewin_tiles) > 0:
                self_str+=" / 聽 {0}".format(toCListStr(prewin_tiles))    
        return self_str
