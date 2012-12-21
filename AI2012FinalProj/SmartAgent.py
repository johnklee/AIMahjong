#-*- coding: utf-8 -*-
from GameBoard import GameBoard
from GameBoard import toCListStr

# Change history:
#   - 2012/12/04 John K Lee
#     * Enhance draw algorithm to keep hand cards while entering pre-win status etc.
#     * Enhance drop algorithm to keep drop records of right opponent in to consideration.
#   - 2012/12/05 John K Lee
#     * Fix bug counting wrong the card while kong during drawing card.
#   - 2012/12/14 John K Lee
#     * Add Field:debug and API:dprint(msg) to class:Agent.
# 
class Agent(object):
    def __init__(self, name, gb):
        """ Constructor
        Withing constructor, below actions will be done:
        1. Initialize
           self.win=0 (Hu/胡 次數)
           self.win_by_draw=0 (Self-Mo/自摸 次數)
           self.lose=0 (放槍次數)
           self.wang_list (手上萬子牌), self.bamb_list (手上條子牌), self.tube_list (手上筒字牌),
           self.word_list (手上字牌), self.wind_list(手上風牌), self.flow_list(手上花牌)
           self.pong_list (Triplet/Sequence 吃/碰進來的 Meld)
           self.card_count (手上的牌數).
           self.win_card=None (贏的那張牌)
           self.pwin_flag=False (進入聽牌狀態)
           self.debug=False (Debug 使用)
        2. Register to Gameboard(gb).
        * Argument:
          name - Agent's name
          gb - GameBoard object."""
        self.win = 0                # 記錄胡場數
        self.win_by_draw = 0        # 紀錄自摸場數
        self.lose = 0               # 紀錄放槍場數
        self.name = name            # Agent 的名字
        self.gb = gb                # GameBoard 實例.
        self.bamb_list = []         # 條子
        self.wang_list = []         # 萬子
        self.tube_list = []         # 筒子
        self.flow_list = []         # 花牌
        self.word_list = []         # 中發白
        self.wind_list = []         # 風牌       
        self.pong_list = []         # 吃/碰 的排組
        self.card_count = 0         # 手上剩餘牌數
        self.win_card = None        # 贏的時候的那張牌
        gb.appendAgent(self)        # 將 Agent 加入 GameBoard
        self.wrong = False          # Wrong flag
        self.pwin_flag = False        # Enter pre-win state
        self.debug = False

    def dprint(self, msg):
        """ Debug print function"""
        if self.debug:
            print(msg)

    # Drop all cards in hand
    def clean(self):
        """ Reset all card lists in hand."""
        del self.bamb_list[:]
        del self.wang_list[:]
        del self.tube_list[:]
        del self.flow_list[:]
        del self.word_list[:]
        del self.wind_list[:]
        #del self.aget_list[:]
        del self.pong_list[:]
        self.card_count = 0
        self.pwin_flag = False
        self.win_card = None

    def _isPrewin(self):
        """ Check if entering pre-win(ready hand) status."""
        prewin_tiles = GameBoard.PreWinTiles(self)
        if len(prewin_tiles) > 0:
            for tile in prewin_tiles:
                ctype = GameBoard.CardType(tile)
                if ctype == 1:
                    if tile in self.gb.wang_list:
                        return True
                elif ctype == 2:
                    if tile in self.gb.tube_list:
                        return True
                elif ctype == 3:
                    if tile in self.gb.bamb_list:
                        return True
                elif ctype == 4:
                    if tile in self.gb.word_list:
                        return True
                elif ctype == 5:
                    if tile in self.gb.wind_list:
                        return True
        
    def draw(self, keep=False):
        """ Draw card. (Required API by Agent)
        Gameboard will call this API to informat agent to draw card. Here should be responsible for:
        1. Call API:drawCard() from GameBoard object to draw card.
        2. Add drawn card into hand.
        3. Return card as dropped card. (In general, you will call API:drop() for dropped card)

        Different from the extended class, SmartAgent has its' own algorithm in drawing card:
        1. 使用 self.gb.drawCard() 從牌桌抽一張牌.
        2. 檢查是否滿足 Goal State (自摸).
           2.1 如果已經聽牌, 則打出抽到的牌.
        3. 檢查是否可以槓
           3.1 如果槓, 可以再抽一張.
        4. 選擇要放棄的牌.
        * Return:
          Dropped card."""
        card = self.gb.drawCard()
        prewin_tiles = GameBoard.PreWinTiles(self)
        if card in prewin_tiles:
        #if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            self.dprint("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
            return       
        elif len(prewin_tiles) > 0:
            self.pwin_flag = True
            for tile in prewin_tiles:
                ctype = GameBoard.CardType(tile)
                if ctype == 1:
                    if tile in self.gb.wang_list:
                        return card 
                elif ctype == 2:
                    if tile in self.gb.tube_list:
                        return card
                elif ctype == 3:
                    if tile in self.gb.bamb_list:
                        return card
                elif ctype == 4:
                    if tile in self.gb.word_list:
                        return card
                elif ctype == 5:
                    if tile in self.gb.wind_list:
                        return card
        
        self.dprint("\t[Test] {0} draw {1}...".format(self.name, card))
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

        dcard=None     
        if not keep:
            dcard = self.drop()
            self.dprint("\t[Test] {0} drop {1}...".format(self.name, dcard))
            #self.gb.disCard(self, dcard)
        if (len(self.word_list)%3+len(self.wind_list)%3+len(self.tube_list)%3+len(self.wang_list)%3+len(self.bamb_list)%3) == 0:
            self.wrong = True
        return dcard

    def drop(self):
        """ Drop card from hand. (Required API by Agent)
        This API will implement the algorithm to deside the dropped card. It will be called during game when necessary.
        Agent is responsible for removing dropped card from hand when make decision.
        The implemented dropping card algorithm as below:
        1. 只有獨張的風牌或中發白
        2. 沒有機會形成 Triplet 或 Sequence 的萬/筒/條 (只有單張)
        3. 頭尾的先丟. (Ex. 1萬/9萬/1筒/9筒/1條/9條)
        4. 下家有丟過的先丟.
        5. 最後都沒有滿足, 任意丟一張 萬/筒/條.
        * Return
          Dropped card which being removed from hand.
        """
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
        # 2. 沒有機會形成 Triplet 或 Sequence 的萬/筒/條 (只有單張)
        # 3. 頭尾的先丟. (Ex. 1萬/9萬/1筒/9筒/1條/9條)
        if (not card) and len(self.tube_list)>0:
            for c in set(self.tube_list):
                #number = int(card[:1])
                if self.tube_list.count(c)>1:
                    continue
                elif GameBoard.PrevCard(c) in self.tube_list or GameBoard.NextCard(c) in self.tube_list:
                    continue
                else:
                    self.tube_list.remove(c)
                    self.card_count-=1
                    return c
            if (not card) and '1筒' in self.tube_list:
                card = '1筒'
                self.tube_list.remove(card)
                self.card_count-=1
                return card
            elif (not card) and '9筒' in self.tube_list:
                card = '9筒'
                self.tube_list.remove(card)
                self.card_count-=1
                return card
            
        if (not card) and len(self.wang_list)>0:
            for c in set(self.wang_list):
                if self.wang_list.count(c)>1:
                    continue
                elif GameBoard.PrevCard(c) in self.wang_list or GameBoard.NextCard(c) in self.wang_list:
                    continue
                else:
                    self.wang_list.remove(c)
                    self.card_count-=1
                    return c
            if (not card) and '1萬' in self.wang_list:
                card = '1萬'
                self.wang_list.remove(card)
                self.card_count-=1
                return card
            elif (not card) and '9萬' in self.wang_list:
                card = '9萬'
                self.wang_list.remove(card)
                self.card_count-=1
                return card
            
        if (not card) and len(self.bamb_list)>0:
            for c in set(self.bamb_list):
                if self.bamb_list.count(c)>1:
                    continue
                elif GameBoard.PrevCard(c) in self.bamb_list or GameBoard.NextCard(c) in self.bamb_list:
                    continue
                else:
                    self.bamb_list.remove(c)
                    self.card_count-=1
                    return c                    
            if (not card) and '1條' in self.bamb_list:
                card = '1條'
                self.bamb_list.remove(card)
                self.card_count-=1
                return card
            elif (not card) and '9條' in self.bamb_list:
                card = '9條'
                self.bamb_list.remove(card)
                self.card_count-=1
                return card

        # 4. 下家有丟過的先丟
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

        # 5. 任意丟一張 萬/筒/條
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
    
    def _pong(self, c_list, count, card):
        """ Handle Pong/Kong during gaming.
        Called by API:pong() to handle pong/kong."""
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
            self.dprint("\t[Test] {0}: Gong '{1}'!".format(self.name, card))
            return self.draw()
       
    def pong(self, agent, ctype, count, card):
        """ Pong callback. (Required API by Agent)
        This API will be called by Gameboard object when Gameboard detect you being able to pong.
        When you decide to pong, you should handle pong and call API:draw() from Gameboard to draw another card and return dropped card.
        If you don't want to pong, just return None or do nothing.
        * Argument
          agent - The Agent which dropped card.
          ctype - Cared type of dropped card.
          count - 2=Pong/3=Kong.
          card - Dropped card which you can pong/kong.
        * Return
          Dropped card if pong/kong; None to give up pong/kong."""
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win+=1
            agent.close+=1
            self.dprint("\t[Test] Agent({0}) 碰胡 {1}!!".format(self.name, card))
            return
        #if self._isPrewin():
	#    return
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

    def eat(self, agent, card, ctype, eat_list):
        """ Eat callback. (Required API by Agent)
        This API will be called by Gameboard when it detect you being able to eat card dropped from previous agent(上家).
        When you decide to eat, a dropped card from hand should be returned. Otherwise return None or do nothing.
        * Argument
          agent - Agent to dropped the card
          card - Dropped card
          ctype - Card type of dropped card
          eat_list - Tuple(card in hand to generate the sequence by dropped card, sequence formed by dropped card) list.
        * Return
          Dropped card if decide to eat; None to give up chance to eat."""
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win+=1
            agent.lose+=1
            self.dprint("\t[Test] Agent({0}) 吃胡 {1}!".format(self.name, card))
            return
	if self._isPrewin():
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

    def _kong(self, ctype, card):
        self.dprint("\t[Test] Agent({0}) 槓 {1}!".format(self.name, card))
        if ctype==1:
            while card in self.wang_list:
                self.wang_list.remove(card)
                self.pong_list.append(card)
            self.pong_list.append(card)
        elif ctype==2:
            while card in self.tube_list:
                self.tube_list.remove(card)
                self.pong_list.append(card)
            self.pong_list.append(card)
        elif ctype==3:
            while card in self.bamb_list:
                self.bamb_list.remove(card)
                self.pong_list.append(card)
            self.pong_list.append(card)
        elif ctype==4:
            while card in self.word_list:
                self.word_list.remove(card)
                self.pong_list.append(card)
            self.pong_list.append(card)
        elif ctype==5:
            while card in self.wind_list:
                self.wind_list.remove(card)
                self.pong_list.append(card)
            self.pong_list.append(card)
                
    def concealedKong(self):
        """ Handle Kong-Cards when dealing."""
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
                    #self.card_count+=1
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
                    #self.card_count+=1
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
                    #self.card_count+=1
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
                    #self.card_count+=1
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
                    #self.card_count+=1
                    drawFlag=True
                    
        if drawFlag:
            self.concealedKong()
                    
    def assignCard(self):
        """ Dealing.
        Drawing card until you have sixteen cards in hand (Not including flower cards)."""
        # 抽滿 16 張牌(扣掉花牌)
        while self.card_count < 16:
            card = self.gb.drawCard()
            self._feedCard(card)
            #self.dprint('\t[Test] card={0}, {1}'.format(card, self.card_count))
                
        # 處理槓牌
        self.concealedKong()
        if self.card_count != (16-3*len((set(self.pong_list)))):
            self.dprint('\t[Test] Conceal kong error: {0}'.format(self))
            self.wrong = True
                    
            
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
        else:
            prewin_tiles = GameBoard.PreWinTiles(self)
            if len(prewin_tiles) > 0:
                self_str+=" / 聽 {0}".format(toCListStr(prewin_tiles))
        return self_str
