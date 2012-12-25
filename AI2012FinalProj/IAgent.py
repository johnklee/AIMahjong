#-*- coding: utf-8 -*-
import platform
from GameBoard import GameBoard
from GameBoard import toCListStr

# Change History:
#   - 2012/12/03 John K Lee
#     * Able to be interactive in Pong/Klong case.
#     * Fix bug on showing eating card list.
#   - 2012/12/25 John K Lee
#     * Replace Tab with Space.
#     * Print tile list in hand when pong/eat condition occurs.
#
if platform.python_version().split('.')[0] == '2':
    input = raw_input
    
class Agent:
    def __init__(self, name, gb):
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

    # Drop all cards in hand
    def clean(self):
        del self.bamb_list[:]
        del self.wang_list[:]
        del self.tube_list[:]
        del self.flow_list[:]
        del self.word_list[:]
        del self.wind_list[:]
        #del self.aget_list[:]
        del self.pong_list[:]
        self.card_count = 0

    def _chooseDropCard(self):
        dcard = None
        while not dcard:            
            cate = input("\t[Info] Choose Drop Card Type(1(萬)/2(筒)/3(條)/4(字)/5(風)): ")
            if len(cate) == 0: break
            ctype = int(cate)
            if ctype==1:
                wang_len = len(self.wang_list)
                if wang_len == 1:
                    dcard = self.wang_list[0]
                    del self.wang_list[0]
                elif wang_len > 0:
                    print('\t[Info] Choose Card Index(1-{0}): '.format(wang_len))
                    msg = '\t'
                    for i in range(wang_len):
                        msg+="{0}:{1} ".format(i+1, self.wang_list[i])
                    di = input(msg)
                    if len(di)==0: continue;
                    if int(di)-1<wang_len:
                        dcard = self.wang_list[int(di)-1]
                        del self.wang_list[int(di)-1]
                    else:
                        print('\t[Warn] Out of range!')
                        continue
                else:
                    print('\t[Warn] Wang card list is empty!')
                    continue
            elif ctype==2:
                tube_len = len(self.tube_list)
                if tube_len == 1:
                    dcard = self.tube_list[0]
                    del self.tube_list[0]
                elif tube_len > 0:
                    print('\t[Info] Choose Card Index(1-{0}): '.format(tube_len))
                    msg = '\t'
                    for i in range(tube_len):
                        msg+="{0}:{1} ".format(i+1, self.tube_list[i])
                    di = input(msg)
                    #di = input('\t[Info] Choose card index(1-{0}): '.format(tube_len))
                    if len(di)==0: continue;
                    if int(di)-1<tube_len:
                        dcard = self.tube_list[int(di)-1]
                        del self.tube_list[int(di)-1]
                    else:
                        print('\t[Warn] Out of range!')
                        continue
                else:
                    print('\t[Warn] Tube card list is empty!')
                    continue
            elif ctype==3:
                clen = len(self.bamb_list)
                if clen == 1:
                    dcard = self.bamb_list[0]
                    del self.bamb_list[0]
                elif clen > 0:
                    print('\t[Info] Choose Card Index(1-{0}): '.format(clen))
                    msg = '\t'
                    for i in range(clen):
                        msg+="{0}:{1} ".format(i+1, self.bamb_list[i])
                    di = input(msg)
                    #di = input('\t[Info] Choose card index(1-{0}): '.format(clen))
                    if len(di)==0: continue;
                    if int(di)-1<clen:
                        dcard = self.bamb_list[int(di)-1]
                        del self.bamb_list[int(di)-1]
                    else:
                        print('\t[Warn] Out of range!')
                        continue
                else:
                    print('\t[Warn] Bamboo card list is empty!')
                    continue
            elif ctype==4:
                clen = len(self.word_list)
                if clen == 1:
                    dcard = self.word_list[0]
                    del self.word_list[0]
                elif clen > 0:
                    print('\t[Info] Choose Card Index(1-{0}): '.format(clen))
                    msg = '\t'
                    for i in range(clen):
                        msg+="{0}:{1} ".format(i+1, self.word_list[i])
                    di = input(msg)
                    #di = input('\t[Info] Choose card index(1-{0}): '.format(clen))
                    if len(di)==0: continue
                    if len(di)-1<clen:
                        dcard = self.word_list[len(di)-1]
                        del self.word_list[len(di)-1]
                    else:
                        print('\t[Warn] Out of range!')
                        continue
                else:
                    print('\t[Warn] Word card list is empty!')
                    continue
            elif ctype==5:
                clen = len(self.wind_list)                    
                if clen == 1:
                    dcard = self.wind_list[0]
                    del self.wind_list[0]
                elif clen > 0:
                    print('\t[Info] Choose Card Index(1-{0}): '.format(clen))
                    msg = '\t'
                    for i in range(clen):
                        msg+="{0}:{1} ".format(i+1, self.wind_list[i])
                    di = input(msg)
                    #di = input('\t[Info] Choose card index(1-{0}): '.format(clen))
                    if len(di)==0: continue;
                    if int(di)-1<clen:
                        dcard = self.wind_list[int(di)-1]
                        del self.wind_list[int(di)-1]
                    else:
                        print('\t[Warn] Out of range!')
                        continue
                else:
                    print('\t[Warn] Wind card list is empty!')
                    continue
            else:
                print('\t[Warn] Unknown Card Type!')
                continue
        return dcard
    
    def idraw(self):
        card = self.gb.drawCard()
        dctype = GameBoard.CardType(card)
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            print("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
            return
        
        if dctype > 5:
            self.flow_list.append(card)
            self.flow_list.sort()
            return self.idraw()
        print("\t[Info] {0}: You draw {1}...".format(self, card))

        # 確認槓牌
        if dctype==1:
            if self.wang_list.count(card)==3: # 確認槓牌
                kong_opt = input('\t[Info] Kong {0} (y/n): '.format(card))
                if len(kong_opt)>0 and (kong_opt == 'y' or kong_opt=='Y'): 
                    self._kong(dctype, card)
                    return self.idraw()
        elif dctype==2:
            if self.tube_list.count(card)==3: # 確認槓牌
                kong_opt = input('\t[Info] Kong {0} (y/n): '.format(card))
                if len(kong_opt)>0 and (kong_opt == 'y' or kong_opt=='Y'): 
                    self._kong(dctype, card)
                    return self.idraw()
        elif dctype==3:
            if self.bamb_list.count(card)==3: # 確認槓牌
                kong_opt = input('\t[Info] Kong {0} (y/n): '.format(card))
                if len(kong_opt)>0 and (kong_opt == 'y' or kong_opt=='Y'): 
                    self._kong(dctype, card)
                    return self.idraw()
        elif dctype==4:
            if self.word_list.count(card)==3: # 確認槓牌
                kong_opt = input('\t[Info] Kong {0} (y/n): '.format(card))
                if len(kong_opt)>0 and (kong_opt == 'y' or kong_opt=='Y'): 
                    self._kong(dctype, card)
                    return self.idraw()                
        elif dctype==5:
            if self.wind_list.count(card)==3: # 確認槓牌
                kong_opt = input('\t[Info] Kong {0} (y/n): '.format(card))
                if len(kong_opt)>0 and (kong_opt == 'y' or kong_opt=='Y'): 
                    self._kong(dctype, card)
                    return self.idraw()
        
        # choose drop card
        dcard = self._chooseDropCard()

        if dcard:
            if dctype==1:                
                self.wang_list.append(card)            
                self.wang_list.sort()
                self.card_count+=1
            elif dctype==2:                
                self.tube_list.append(card)
                self.tube_list.sort()
                self.card_count+=1
            elif dctype==3:                
                self.bamb_list.append(card)
                self.bamb_list.sort()
                self.card_count+=1
            elif dctype==4:                        
                self.word_list.append(card)
                self.word_list.sort()
                self.card_count+=1
            elif dctype==5:                
                self.wind_list.append(card)
                self.wind_list.sort()
                self.card_count+=1
            print("\t[Test] {0} drop card={1}...".format(self.name, dcard))
            #self.gb.disCard(self, dcard)
            return dcard
        else:
            print("\t[Test] {0} drop draw card={1}...".format(self.name, card))
            #self.gb.disCard(self, card)
            return card
        
    # 抽牌
    def draw(self, keep=False):
        card = self.gb.drawCard()
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            print("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
            return        
        
        print("\t[Test] {0} draw {1}...".format(self.name, card))        
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
            print("\t[Test] {0} drop {1}...".format(self.name, dcard))
            #self.gb.disCard(self, dcard)
        if len(self.word_list)%3+len(self.wind_list)%3+len(self.tube_list)%3+len(self.wang_list)%3+len(self.bamb_list)%3 != 2:
            self.wrong = True
        return dcard

    # 根據下面原則放棄手牌
    # 1. 只有獨張的風牌或中發白
    # 2. 沒有機會形成 Triplet 或 Sequence 的萬/筒/條 (只有單張)
    # 3. 頭尾的先丟. (Ex. 1萬/9萬/1筒/9筒/1條/9條)
    # 4. 任意丟一張 萬/筒/條.
    def drop(self):
        card = ''
        # 1.
        if len(self.word_list) == 1:
            card = self.word_list.pop()
            return card
        else:
            for c in set(self.word_list):                
                if self.word_list.count(c)==1:
                    self.word_list.remove(c)
                    self.card_count-=1
                    return c
        if len(self.wind_list) == 1:
            card = self.wind_list.pop()
            return card
        else:
            for c in set(self.wind_list):
                if self.wind_list.count(c)==1:                    
                    self.wind_list.remove(c)
                    self.card_count-=1
                    return c
        # 2        
        if (not card) and len(self.tube_list)>0:
            for c in set(self.tube_list):
                #number = int(card[:1])
                if self.tube_list.count(c)>1:
                    continue
                elif GameBoard.PrevCard(c) in self.tube_list or GameBoard.NextCard(c) in self.tube_list:
                    continue
                else:
                    self.tube_list.remove(c)
                    return c
            if (not card) and '1筒' in self.tube_list:
                card = '1筒'
                self.tube_list.remove('1筒')
                return card
            elif (not card) and '9筒' in self.tube_list:
                card = '9筒'
                self.tube_list.remove('9筒')
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
                self.wang_list.remove('1萬')
                return card
            elif (not card) and '9萬' in self.wang_list:
                card = '9萬'
                self.wang_list.remove('9萬')
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

        # 任意丟一張 萬/筒/條
        if (not card) and len(self.tube_list)>0:
            card = self.tube_list.pop()
        if (not card) and len(self.wang_list)>0:
            card = self.wang_list.pop()
        if (not card) and len(self.bamb_list)>0:
            card = self.bamb_list.pop()
        self.card_count-=1
        return card
    
    def _pong(self, c_list, count, card):
        print('\t[Info] {0}'.format(self))
        pong_opt = input('\t[Info] Pong/Kong {0}? (y/n): '.format(card))
        if len(pong_opt) == 0 or (pong_opt == 'n' or pong_opt == 'N'):
            return
        
        #for i in range(count+1):
        #    self.pong_list.append(card)
        self.pong_list.extend(card*(count+1))
            
        for i in range(count):
            c_list.remove(card)
            self.card_count-=1
        
        if count==2:
            #dcard = self.drop()
            dcard = None
            while not dcard:
                dcard = self._chooseDropCard()
            print("\t[Test] {0}: Pong '{1}' and drop {2}!".format(self.name, card, dcard))
            #self.gb.disCard(self, dcard)
            return dcard
        else:
            print("\t[Test] {0}: Kong '{1}'!".format(self.name, card))
            return self.draw(keep=True)
        
    # 碰! A callback by GameBoard. Return drop card or redraw card if you want.    
    def pong(self, agent, ctype, count, card):
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
                

    def _eat(self, card, olist, dlist, elist):
        self.pong_list.extend(elist)
        for e in dlist:
            olist.remove(e)
            self.card_count-=1

        # choose drop card
        dcard = self._chooseDropCard()
        if not dcard:
            dcard = self.drop()
            print('\t[Info] Random choose drop card="{0}"'.format(dcard))
                
        print("\t[Test] {0}: Eat '{1}' and drop {2}!".format(self.name, elist, dcard))
        #self.gb.disCard(self, dcard)
        return dcard

    # 吃牌. Callback by GameBoard
    def eat(self, agent, card, ctype, eat_list):
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win+=1
            agent.lose+=1
            print("\t[Test] Agent({0}) 吃胡 {1}!".format(self.name, card))
            return
        # Greedy algorithm: Always eat from the first choice
        print('\t[Info] {0}'.format(self))
        print('\t[Info] Eat {0} has option(s):'.format(card))
        if ctype==1:
        #if len(eat_list)==1: return self._eat(card, self.wang_list, eat_list[0][0], eat_list[0][1])
            for i in range(len(eat_list)):
                print("\t{0}:{1} ".format(i+1, toCListStr(eat_list[i][1])))
            choice_opt = input('\t: ')
            if len(choice_opt) > 0: 
                return self._eat(card, self.wang_list, eat_list[int(choice_opt)-1][0], eat_list[int(choice_opt)-1][1])
        elif ctype==2:
        #if len(eat_list)==1: return self._eat(card, self.tube_list, eat_list[0][0], eat_list[0][1])
            for i in range(len(eat_list)):
                print("\t{0}:{1} ".format(i+1, toCListStr(eat_list[i][1])))
            choice_opt = input('\t: ')
            if choice_opt == 'n' or choice_opt == 'N':
                return
            if len(choice_opt) > 0:
                return self._eat(card, self.tube_list, eat_list[int(choice_opt)-1][0], eat_list[int(choice_opt)-1][1])
        elif ctype==3:
        #if len(eat_list)==1: return self._eat(card, self.bamb_list, eat_list[0][0], eat_list[0][1])
            for i in range(len(eat_list)):
                print("\t{0}:{1} ".format(i+1, toCListStr(eat_list[i][1])))
            choice_opt = input('\tChoose 1-{0}: '.format(len(eat_list)))
            if len(choice_opt) > 0:
                return self._eat(card, self.bamb_list, eat_list[int(choice_opt)-1][0], eat_list[int(choice_opt)-1][1])

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
        print("\t[Test] Agent({0}) 槓 {1}!".format(self.name, card))
        if ctype==1:
            while card in self.wang_list:
                print('\t[Test] Remove {0}...'.format(card))
                self.wang_list.remove(card)
                self.pong_list.append(card)
                self.card_count-=1
            self.pong_list.append(card)
        elif ctype==2:
            while card in self.tube_list:
                print('\t[Test] Remove {0}...'.format(card))
                self.tube_list.remove(card)
                self.pong_list.append(card)
                self.card_count-=1
            self.pong_list.append(card)
        elif ctype==3:
            while card in self.bamb_list:
                print('\t[Test] Remove {0}...'.format(card))
                self.bamb_list.remove(card)
                self.pong_list.append(card)
                self.card_count-=1
            self.pong_list.append(card)
        elif ctype==4:
            while card in self.word_list:
                print('\t[Test] Remove {0}...'.format(card))
                self.word_list.remove(card)
                self.pong_list.append(card)
                self.card_count-=1
            self.pong_list.append(card)
        elif ctype==5:
            while card in self.wind_list:
                print('\t[Test] Remove {0}...'.format(card))
                self.wind_list.remove(card)
                self.pong_list.append(card)
                self.card_count-=1
            self.pong_list.append(card)
                
    def concealedKong(self):
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
                    self.card_count+=1
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
                    self.card_count+=1
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
                    self.card_count+=1
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
                    self.card_count+=1
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
                    self.card_count+=1
                    drawFlag=True
                    
        if drawFlag:
            self.concealedKong()
            
    # 發牌        
    def assignCard(self):
        # 抽滿 16 張牌(扣掉花牌)
        while self.card_count < 16:
            card = self.gb.drawCard()
            self._feedCard(card)
                
        # 處理槓牌
        self.concealedKong()
                    
            
    def __str__(self):
        self_str = "{0}({1}/{2}/{3}): [".format(self.name, self.win_by_draw, self.win, self.lose)
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
