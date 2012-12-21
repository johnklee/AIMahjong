#-*- coding: utf-8 -*-
from GameBoard import *
import copy
import SmartAgent
import JAgent
import GreedyAgent

DropCount =10
PongLen = 10

class FAgent(SmartAgent.Agent):
    def __init__(self, name, gb):
        super(FAgent, self).__init__(name, gb)
        self.drop_count = 0
        
    # Drop all cards in hand
    def clean(self):
        del self.bamb_list[:]
        del self.wang_list[:]
        del self.tube_list[:]
        del self.flow_list[:]
        del self.word_list[:]
        del self.wind_list[:]
        del self.pong_list[:]
        self.card_count = 0
        self.drop_count = 0
    

    def drop(self):
        drop_count = 0
        self.dprint("dropcount".format(self.drop_count)) 
        self.drop_count+=1

        self.dprint("pong length".format(len(self.pong_list)))
        if self.drop_count > DropCount and len(self.pong_list) < PongLen:
	#for i in range(3):
            self.dprint("\t[Test] Simulation...")
	    gbtest = copy.deepcopy(self.gb)
	    gbtest.aget_list =[]
	    b1 = copy.deepcopy(self.gb.aget_list[0])
	    #b1.name = "BBB1"
	    gbtest.appendAgent(b1)
	    b2 = copy.deepcopy(self.gb.aget_list[1])
	    #b2.name = "BBB2"
	    gbtest.appendAgent(b2)
	    b3 = copy.deepcopy(self.gb.aget_list[2])
	    #b3.name = "BBB3"
	    gbtest.appendAgent(b3)
              
	    b4 = SmartAgent.Agent('F', gbtest)
	    b4.bamb_list = copy.deepcopy(self.gb.aget_list[3].bamb_list)
	    b4.wang_list = copy.deepcopy(self.gb.aget_list[3].wang_list)
	    b4.tube_list = copy.deepcopy(self.gb.aget_list[3].tube_list)
	    b4.flow_list = copy.deepcopy(self.gb.aget_list[3].flow_list)
	    b4.word_list = copy.deepcopy(self.gb.aget_list[3].word_list)
	    b4.wind_list = copy.deepcopy(self.gb.aget_list[3].wind_list)
	    b4.pong_list = copy.deepcopy(self.gb.aget_list[3].pong_list)
	    b4.card_count = copy.deepcopy(self.gb.aget_list[3].card_count)
            to_be_test =[] # Card in hand
	    for card in b4.bamb_list:
	        to_be_test.append(card)
	    for card in b4.wang_list:
	        to_be_test.append(card)
	    for card in b4.tube_list:
	        to_be_test.append(card)
	    for card in b4.flow_list:
	        to_be_test.append(card)
	    for card in b4.word_list:
	        to_be_test.append(card)
	    for card in b4.wind_list:
	        to_be_test.append(card)

            score = {}#紀錄每個牌的積分
	    for card in list(set(to_be_test)):
                #self.dprint "\n\n\n\n\npong length",len(b4.pong_list),"\n\n\n"
		score[card] = 0
		fangchang_before = b4.lose
		for count in range(10):
	            if card in b4.bamb_list: b4.bamb_list.remove(card)
	            if card in b4.wang_list: b4.wang_list.remove(card)
	            if card in b4.tube_list: b4.tube_list.remove(card)
	            if card in b4.flow_list: b4.flow_list.remove(card)
	            if card in b4.word_list: b4.word_list.remove(card)
	            if card in b4.wind_list: b4.wind_list.remove(card)
                    #self.dprint("\t[Simulation Test] {0} drop {1}...".format(b4.name, card))
                    gbtest.disCard(b4, card)

	            #self.dprint "\n=======================START     TO     SIMULATE   THE    GAME===========================   \n"
	            gbtest.testplay()
	            #self.dprint "\n#########################           game done!!!                ###########################\n"
	            
		    if gbtest.win_agent:
		        if gbtest.win_agent == b4:
                            score[card] += 3
	                elif b4.lose > fangchang_before:
		            score[card] -= 3
		        
		    del gbtest
	            del b1
	            del b2
	            del b3
		    del b4
	       		    
		    gbtest = copy.deepcopy(self.gb)
		    gbtest.aget_list =[]
		    b1 = copy.deepcopy(self.gb.aget_list[0])
		    gbtest.appendAgent(b1)
		    b2 = copy.deepcopy(self.gb.aget_list[1])
		    gbtest.appendAgent(b2)
		    b3 = copy.deepcopy(self.gb.aget_list[2])
		    gbtest.appendAgent(b3)
		      
		    b4 = SmartAgent.Agent('F', gbtest)
		    b4.bamb_list = copy.deepcopy(self.gb.aget_list[3].bamb_list)
		    b4.wang_list = copy.deepcopy(self.gb.aget_list[3].wang_list)
		    b4.tube_list = copy.deepcopy(self.gb.aget_list[3].tube_list)
		    b4.flow_list = copy.deepcopy(self.gb.aget_list[3].flow_list)
		    b4.word_list = copy.deepcopy(self.gb.aget_list[3].word_list)
		    b4.wind_list = copy.deepcopy(self.gb.aget_list[3].wind_list)
		    b4.pong_list = copy.deepcopy(self.gb.aget_list[3].pong_list)
		    b4.card_count = copy.deepcopy(self.gb.aget_list[3].card_count)

	    self.card_count-=1
	    card = [k for k,v in score.items() if v==max(score.values())][0]
	    if card in b4.bamb_list: self.bamb_list.remove(card)
	    if card in b4.wang_list: self.wang_list.remove(card)
	    if card in b4.tube_list: self.tube_list.remove(card)
	    if card in b4.flow_list: self.flow_list.remove(card)
	    if card in b4.word_list: self.word_list.remove(card)
	    if card in b4.wind_list: self.wind_list.remove(card)
	    return card     	    

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
        if len(self.gb.drop_record[rightAgt.name]) > 0:
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

   
    def pong_or_eat(gb, agent, card):
        next_pos = self.aget_list.index(agent)+1
        for sft in range(len(self.aget_list)-1):
            other_agent = self.aget_list[(next_pos+sft)%len(self.aget_list)]
            if GameBoard.GoalState(other_agent, card):
                self.win_agent = other_agent
                other_agent.win_card = card
                other_agent.win+=1
                agent.lose+=1
                self.dprint("\t[Test] Agent({0}) 胡牌 {1}!!!".format(other_agent.name, card))
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
        #self.dprint("\t[Test] next agent={0}...".format(next_agent.name))
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


    def draw(self, keep=False):
        card = self.gb.drawCard()
        if GameBoard.GoalState(self, card): # Check goal state
            self.gb.win_agent = self
            self.win_card = card
            self.win_by_draw+=1
            self.dprint("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
            return

        prewin_tiles = GameBoard.PreWinTiles(self)
        if len(prewin_tiles) > 0:
            return card

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
