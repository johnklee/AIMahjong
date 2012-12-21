#-*- coding: utf-8 -*-
from GameBoard import GameBoard
from GameBoard import toCListStr

class Agent:
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
        2. Register to Gameboard(gb).
        * Argument:
          name - Agent's name
          gb - GameBoard object."""
        self.win = 0            # Hu/胡 次數
        self.win_by_draw = 0    # Self-Mo/自摸 次數
        self.lose = 0           # 放槍次數
        self.name = name        # Agent name
        self.gb = gb            # GameBoard 實例.
        self.bamb_list = []     # 條子牌列
        self.wang_list = []     # 萬字牌列
        self.tube_list = []     # 筒子牌列
        self.flow_list = []     # 花牌牌列
        self.word_list = []     # 字牌牌列 (中發白)
        self.wind_list = []     # 風牌牌列 (東南西北)
        self.pong_list = []     # Meld/順子,刻子,槓子 牌列.
        self.card_count = 0     # 手上牌數
        self.win_card = None    # 贏牌時吃進來的那張牌
        gb.appendAgent(self)    # 向 GameBoard 實例 register

    # Drop all cards in hand
    def clean(self):
        """ Reset all card lists in hand."""
        del self.bamb_list[:]
        del self.wang_list[:]
        del self.tube_list[:]
        del self.flow_list[:]
        del self.word_list[:]
        del self.wind_list[:]
        del self.pong_list[:]
        self.card_count = 0
        self.win_card = None
        
    # 抽牌
    def draw(self, keep=False):
        """ Draw card. (Required API by Agent)
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
            print("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
            return
        #print("\t[Test] {0} draw {1}...".format(self.name, card))
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
            #print("\t[Test] {0} drop {1}...".format(self.name, dcard))
            #self.gb.disCard(self, dcard)
        return dcard

    # 放棄手上一張牌
    def drop(self):
        """ Drop card from hand. (Required API by Agent)
        This API will implement the algorithm to deside the dropped card. It will be called during game when necessary.
        Agent is responsible for removing dropped card from hand when make decision.
        * Return
          Dropped card which being removed from hand.
        """
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
        """ Handle Pong/Kong during gaming.
        Called by API:pong() to handle pong/kong."""
        for i in range(count+1):
            self.pong_list.append(card)
            
        for i in range(count):
            c_list.remove(card)
            self.card_count-=1
        
        if count==2:
            dcard = self.drop()
            #print("\t[Test] {0}: Pong '{1}' and drop {2}!".format(self.name, card, dcard))
            #self.gb.disCard(self, dcard)
            return dcard
        else:
            #print("\t[Test] {0}: Gang '{1}'!".format(self.name, card))
            return self.draw(keep=False)
        
    # 碰! A callback by GameBoard. Return drop card or redraw card if you want.    
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
            print("\t[Test] Agent({0}) 碰胡 {1}!!".format(self.name, card))
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
        #print("\t[Test] {0}: Eat '{1}' and drop {2}!".format(self.name, toCListStr(elist), dcard))
        #self.gb.disCard(self, dcard)
        return dcard

    # 吃牌. Callback by GameBoard
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
            print("\t[Test] Agent({0}) 吃胡 {1}!".format(self.name, card))
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
        """ Dealing.
        Drawing card until you have sixteen cards in hand (Not including flower cards)."""
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
