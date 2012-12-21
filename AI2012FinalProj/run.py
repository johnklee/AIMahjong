#!/usr/bin/python
#-*- coding: utf-8 -*-
from __future__ import print_function
import GameBoard
import GreedyAgent
import SmartAgent
import IAgent
import sys
import JAgent
import GeniusAgent
#import FAgent

# 建立 GameBoard
gb = GameBoard.GameBoard()
#gb.debug = True
	
print("Please enter loop:(1~100):")
#loop = 500 
loop = sys.stdin.readline()

if int(loop) > 0:
    # 建立 Agent
    a1 = SmartAgent.Agent('S1', gb)
    a2 = SmartAgent.Agent('S2', gb)
    a3 = GeniusAgent.Agent('G', gb)
    a4 = JAgent.JAgent('J', gb)
    for i in range(int(loop)):
        print("\t[Info] Round {0}:".format(i+1))
        gb.play()

	win_cnt = 0
	win_by_draw_cnt = 0
	lose_cnt = 0
	for agt in gb.aget_list:
		win_cnt += agt.win
		win_by_draw_cnt += agt.win_by_draw
		lose_cnt += agt.lose

	for agt in gb.aget_list:
		print("\t[SI] Agent({0} {1}/{2}/{3}): ".format(agt.name, agt.win_by_draw, agt.win, agt.lose), end='')
		if win_by_draw_cnt > 0:
			print("Self-Mo Rate={:.1%}; ".format(float(agt.win_by_draw)/win_by_draw_cnt), end='')
		else:
			print("Self-Mo Rate=0%; ", end='')

		if win_cnt > 0:
			print("Hu Rate={:.1%}; ".format(float(agt.win)/win_cnt), end='')
		else:
			print("Hu Rate=0%; ", end='')

		if lose_cnt > 0:
			print("Lose Rate={:.1%}".format(float(agt.lose)/lose_cnt))
		else:
			print("Lose Rate=0%")
    # Win count at each round
    #for (key, val) in gb.win_round.items():
    #    print("Win in Round{0}={1}".format(key, val))
    # Pre-win count at each round
    pwf = open('prewin_dist.log', 'w')
    for (key, val) in gb.pwin_round.items():
        pwf.write("Pwin dist at round{0}:\r\n".format(key))
        #print("Pewin dist at round{0}:".format(key))
        for (key, val) in val.items():
            #print("\tPre-win agent count={0}->{1}".format(key, val))
            pwf.write("\tPre-win agent count={0}->{1}\r\n".format(key, val))
    pwf.close()
    #print("\t[SI] Wrong count={0}!".format(gb.wrong_count))
else:
    a1 = GreedyAgent.Agent('R1', gb)
    a2 = GreedyAgent.Agent('R2', gb)
    a3 = GreedyAgent.Agent('R3', gb)
    a4 = IAgent.Agent('I', gb)
    gb.play()
