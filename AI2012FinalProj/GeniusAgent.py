#-*- coding: utf-8 -*-
from GameBoard import GameBoard
from GameBoard import toCListStr

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
		self.pwin_flag = False      # Enter pre-win state
	
	def hu(self, card):
		print("\t[Test] Agent({0}) 胡牌! ({1})".format(self, card))
	
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
		self.pwin_flag = False

	def _isPrewin(self):
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

	# 抽牌
	# 1. 使用 self.gb.drawCard() 從牌桌抽一張牌.
	# 2. 檢查是否滿足 Goal State (自摸).
	#    2.1 如果已經聽牌, 則打出抽到的牌.
	# 3. 檢查是否可以槓
	#    3.1 如果槓, 可以再抽一張.
	# 4. 選擇要放棄的牌.
	def draw(self, keep=False):
		card = self.gb.drawCard()
		#print "\tGeniusAgent draw: {0}".format(card)
		prewin_tiles = GameBoard.PreWinTiles(self)
		if card in prewin_tiles:
		#if GameBoard.GoalState(self, card): # Check goal state
			self.gb.win_agent = self
			self.win_card = card
			self.win_by_draw+=1
			print("\t[Test] Agent({0}) 自摸 {1}!".format(self.name, card))
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
		
		#print("\t[Test] {0} draw {1}...".format(self.name, card))
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
			#print("\t[Test] {0} drop {1}...".format(self.name, dcard))
			#self.gb.disCard(self, dcard)
		if (len(self.word_list)%3+len(self.wind_list)%3+len(self.tube_list)%3+len(self.wang_list)%3+len(self.bamb_list)%3) == 0:
			self.wrong = True
		return dcard

	# BD: Recursive look for all combination of specific card type list.
	# Argument:
	#    ctype - Card type
	#    cards - Card list
	#    comb_str - Current combination
	#    combination - ?
	# Return:
	#    List of combination result.  
	def find_all_combination(self, ctype, cards, comb_str, combination):
		""" Recursive look for all combination of specific card type list.
		* Argument:
		  ctype - Card type
		  cards - Card list
		  comb_str - Current combination
		  combination - ?
		* Return:
		  List of combination result
		"""
		if len(cards) == 0:
			combination.append(comb_str)
			return combination
		card = cards[0]
		ctype = GameBoard.CardType(card)
		if (ctype == 1) or (ctype == 2) or (ctype == 3):
			count = cards.count(card)
			if count == 3: # 刻
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if count == 2: # 雀眼
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			n = GameBoard.NextCard(card)
			if n != None: nn = GameBoard.NextCard(n)
			else: nn = ""
			if (n in cards) and (nn in cards): # 順
				copy = list(cards)
				copy.remove(card)
				copy.remove(n)
				copy.remove(nn)
				new = "{0} {1} {2}\t".format(card, n, nn)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if n in cards:
				copy = list(cards)
				copy.remove(card)
				copy.remove(n)
				new = "{0} {1}\t".format(card, n)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if nn in cards:
				copy = list(cards)
				copy.remove(card)
				copy.remove(nn)
				new = "{0} {1}\t".format(card, nn)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			cards.remove(card)
			new = "{0}\t".format(card)
			self.find_all_combination(ctype, cards, comb_str + new, combination)

		if (ctype == 4) or (ctype == 5):
			count = cards.count(card)
			if count == 3:
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			if count == 2:
				copy = list(cards)
				copy.remove(card)
				copy.remove(card)
				new = "{0} {0}\t".format(card)
				self.find_all_combination(ctype, copy, comb_str + new, combination)
			cards.remove(card)
			new = "{0}\t".format(card)
			self.find_all_combination(ctype, cards, comb_str + new, combination)

		return combination

	def way_to_prewin(self, one):
		"""
		kind = [triple, pair, neighbor, single]
		useful: how many cards can we get one more triple
		score: a metric to evaluate how good
			triple = 3, pair/consecutive neighbor = 2, non-consecutive = 1, single = 0
		"""
		kind = [0, 0, 0, 0] 
		useful = []
		score = 0
		for part in one.split("\t"):
			#print "part: {0}".format(part)
			tmp = part.split()
			length = len(tmp)
			if (length == 3):		# triple
				kind[0] += 1
				score += 3
			elif (length == 1):		# single
				kind[3] += 1
			elif (tmp[0] == tmp[1]):# pair
				kind[1] += 1
				useful.append("{0}".format(tmp[0]))
				score += 2
			else:
				kind[2] += 1
				n = GameBoard.NextCard(tmp[0])
				p = GameBoard.PrevCard(tmp[0])
				nn = GameBoard.NextCard(tmp[1])
				if (n == tmp[1]):	# consecutive neighbor
					score += 2
					if (p != None): useful.append(p)
					if (nn != None): useful.append(nn)
				else:
					useful.append(n)
					score += 1

		#print "kind: {0}".format(kind)
		""" how many cards can we probably get """
		useful_amount = 0
		for card in set(useful):
			ctype = GameBoard.CardType(card)
			if (ctype == 1): a = self.wang_list.count(card)
			elif (ctype == 2): a = self.tube_list.count(card)
			elif (ctype == 3): a = self.bamb_list.count(card)
			elif (ctype == 4): a = self.word_list.count(card)
			else: a = self.wind_list.count(card)
			b = self.gb.drop_list.count(card)
			useful_amount += (4 - a - b)

		"""
		1. enumerate, because goal state not too much
		2. counting pong_list so that we can focus on 16 cards
		3. check prewin first	
		"""
		goals = [[4, 1, 1, 0], [5, 0, 0, 1], [4, 2, 0, 0]]
		gpattern = [["***", "***", "***", "***", "##", "$$"],["***", "***", "***", "***", "***", "/"],
					["***", "***", "***", "***", "##", "##"]]
		result = [0, 0, 0]
		size = len(self.pong_list) / 3
		if ((size + kind[0]) > 4): return [0, useful_amount, score]
		for i in range(size): 
			gpattern[0].remove("***")
			gpattern[1].remove("***")
			gpattern[2].remove("***")
		for number in range(3):
			k0 = kind[0]
			k1 = kind[1]
			k2 = kind[2]
			k3 = kind[3]
			p1 = gpattern[number]
			for i in range(k0): p1.remove("***")
			for i in range(min(k1, goals[number][1])): 
				k1 -= 1
				p1.remove("##")
			for i in range(min(k2, goals[number][2])):
				k2 -= 1
				p1.remove("$$")
			#print "p1: {0}, size: {1}".format(p1, (k1+k2)*2+k3)
			step = 0
			two = k1 + k2
			for i in range(len(p1)):
				length = len(p1[i])
				if (length == 3):
					if two:
						two -= 1
						step += 1
					else:
						step += 2
				elif (length == 2):
					step += 1
			result[number] = step
		#print "steps to goal: {0}, useful: {1}".format(result, len(useful))
		
		return [min(result), useful_amount, score]

	def count_steps(self):
		wang_combination = self.find_all_combination(1, list(self.wang_list), "", [])
		tube_combination = self.find_all_combination(2, list(self.tube_list), "", [])
		bamb_combination = self.find_all_combination(3, list(self.bamb_list), "", [])
		word_combination = self.find_all_combination(4, list(self.word_list), "", [])
		wind_combination = self.find_all_combination(5, list(self.wind_list), "", [])
		all_combination = []
		size = 0
		for w in wang_combination:
			for t in tube_combination:
				for b in bamb_combination:
					for wo in word_combination:
						for wi in wind_combination:
							all_combination.append("{0}{1}{2}{3}{4}".format(w, t, b, wo, wi))
							size += 1
		mini = 99
		useful_amount = 0
		score = 0
		for i in range(size):
			one = all_combination[i]
			#print "one: {0}".format(one)
			r = self.way_to_prewin(one.strip())
			if (r[0] < mini): mini = r[0]
			if (r[1] > useful_amount): useful_amount = r[1]
			if (r[2] > score): score = r[2]

		return mini, useful_amount, score

	def sorting_by_criteria(self, result):
		""" sort by steps to prewin (small -> big) """
		result = sorted(result, key=lambda r: r[0])
		flag = False
		m = result[0][0]
		for i in range(len(result)):
			if (result[i][0] == m): continue
			flag = True
			break
		if not flag: i += 1
		result = result[:i]
		""" in prewin status, compare useful_amount only """
		if (result[0][0] == 0):
			result = sorted(result, key=lambda r: r[1], reverse=True)
			#+++++++
			test = ""
			for r in result:
				test += "[{0}, {1}, {2}, {3}], ".format(r[0], r[1], r[2], r[3])
			#print "prewin status: {0}".format(test)
			#++++++
			return result[0][3]
		#####
		#test = ""
		#for r in result:
		#	test += "[{0}, {1}, {2}, {3}], ".format(r[0], r[1], r[2], r[3])
		#print "{0} steps to win: {1}".format(r[0], test)
		#####
		""" sort by score (big -> small) """
		result = sorted(result, key=lambda r: r[2], reverse=True)
		flag = False
		m = result[0][2]
		for i in range(len(result)):
			if (result[i][2] == m): continue
			flag = True
			break
		if not flag: i += 1
		result = result[:i]
		#--------------
		#test = ""
		#for r in result:
		#	test += "[{0}, {1}, {2}, {3}], ".format(r[0], r[1], r[2], r[3])
		#print "sort by score: {0}".format(test)
		#--------------
		""" sort by useful card amount (big -> small) """
		result = sorted(result, key=lambda r: r[1], reverse=True)
		#####
		#test = ""
		#for r in result:
		#	test += "[{0}, {1}, {2}, {3}], ".format(r[0], r[1], r[2], r[3])
		#print "sort by useful amount: {0}".format(test)
		#####
		""" choose one to discard """
		dcard = result[0][3]
		m = result[0][1]
		for r in result:
			if (r[1] != m): break
			ctype = GameBoard.CardType(r[3])
			if (ctype == 4) and (self.word_list.count(r[3]) == 1): dcard = r[3]
			if (ctype == 5) and (self.wind_list.count(r[3]) == 1): dcard = r[3]
		#print "\tdiscard: {0}".format(dcard)
		return dcard

	def drop(self):
		""" try to discard every card to find the best """
		#print "drop_list: {0}".format(" ".join(self.gb.drop_list))
		result = []
		all_cards = [self.wang_list, self.tube_list, self.bamb_list, self.word_list, self.wind_list]
		previous = ""
		for cards in all_cards:
			for i in range(len(cards)):
				""" avoid running same card """
				if (cards[i] == previous): continue
				c = cards.pop(i)
				previous = c
				mini, useful_amount, score = self.count_steps()
				cards.insert(i, c)
				result.append([mini, useful_amount, score, c])
				#print "min: {0}, useful_amount: {1}, score: {2}, dcard: {3}".format(mini, useful_amount, score, c)

		dcard = self.sorting_by_criteria(result)
		#print "\t[Test] {0}: drop {1}".format(self, dcard)
		ctype = GameBoard.CardType(dcard)
		all_cards[ctype-1].remove(dcard)
		self.card_count -= 1
		return dcard

	def _pong(self, c_list, count, card):        
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
			#print("\t[Test] {0}: Gong '{1}'!".format(self.name, card))
			return self.draw()
		
	# 碰! A callback by GameBoard. Return drop card or redraw card if you want.    
	def pong(self, agent, ctype, count, card):
		if GameBoard.GoalState(self, card): # Check goal state
			self.gb.win_agent = self
			self.win_card = card
			self.win+=1
			agent.close+=1
			#print("\t[Test] Agent({0}) 碰胡 {1}!!".format(self.name, card))
			return
		#if self._isPrewin():
	#    return
		#print "\tGeniusAgent pong: {0}".format(card)
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
		if GameBoard.GoalState(self, card): # Check goal state
			self.gb.win_agent = self
			self.win_card = card
			self.win+=1
			agent.lose+=1
			#print("\t[Test] Agent({0}) 吃胡 {1}!".format(self.name, card))
			return
		if self._isPrewin():
			return
		#print "\tGeniusAgent eat: {0}".format(card)
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
		#print("\t[Test] Agent({0}) 槓 {1}!".format(self.name, card))
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
			
	# 發牌        
	def assignCard(self):
		# 抽滿 16 張牌(扣掉花牌)
		while self.card_count < 16:
			card = self.gb.drawCard()
			self._feedCard(card)
			#print('\t[Test] card={0}, {1}'.format(card, self.card_count))
				
		# 處理槓牌
		self.concealedKong()
		if self.card_count != (16-3*len((set(self.pong_list)))):
			#print('\t[Test] Conceal kong error: {0}'.format(self))
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


