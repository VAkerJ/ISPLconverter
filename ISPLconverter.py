from stratsynth_2.graph import *
import sys
import os
import numpy as np




def makeISPL(gamename):

    game = Game_graph(gamename+"/GK")
    game.deltaDic()
    graph = game.get_graph()
    loc = list(game.get_loc())
    noa = len(loc[0])

    directory = 'smc/smc_games'
    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(directory+"/"+gamename+".ispl", "w")
    
    f.write("Agent Enviroment\n    Vars:")

    states = [] #creates a list of the set of states each agent can observe
    for n in range(noa):
        f.write("\n        state_player_"+str(n)+" : {")
        temp = [s[n].replace(", ", "_") for s in loc]
        states.append(set(temp))

        for ids, state in enumerate(states[n]):
            f.write(state)
            if ids < len(states[n])-1: f.write(", ")
        f.write("};")
    
    f.write("\n    end Vars\n    Actions = {none};\n    Protocol:\n        Other : {none};\n    end Protocol\n    Evolution:\n")
    
    tDic = {} # creates a dictionary where the keys are observations and the values are dictionaries
              #where the keys are the actions available in the respective states and values are the
              #states one traverses to
              #tDic = {state : {action1 : next state1, action2 : next state2}}

    for node in graph:
        tDic.update({node : {}})

        for nNode in graph[node].get_adjacent_vert():
            actions = graph[node].get_actions(nNode)
            nextNode = nNode.get_id()


            for action in actions:
                if action in tDic[node]:
                    tDic[node][action].append(nNode.get_id())
                else:
                    tDic[node].update({action : [nextNode]})

    for fromNode in tDic.keys():
        for action in tDic[fromNode].keys():
            for idn, toNode in enumerate(tDic[fromNode][action]):
                if idn > 0: f.write("        or\n")
                
                f.write("        (")
                for ids, state in enumerate(toNode):
                    f.write("(state_player_" + str(ids) + " = " + state.replace(", ", "_") + ")")
                    if ids < len(states)-1: f.write(" and ")
                f.write(")\n")

            f.write("        if\n        (")

            for ids, state in enumerate(fromNode):
                if ids > 0: f.write(" and ")
                f.write("(state_player_" + str(ids) + " = " + state.replace(", ", "_") + ")")
            
            for ida, act in enumerate(action):
                if act != "-":
                    f.write(" and ")
                    f.write("(player_" + str(ida) + ".Action = " + act + ")")

            f.write(");\n\n")

    f.write("    end Evolution\nend Agent\n")

    pDic = {}
    for n in range(noa):
        pDic.update({n : {}})

    for key in tDic.keys():
        tStates = [s.replace(", ", "_") for s in key]
        actions = graph[key].get_adjacent_actions()

        for ids, state in enumerate(tStates):

            if state not in pDic[ids]: pDic[ids].update({state : []})
            
        for action in actions:

            for act in action:
                for ida, a in enumerate(act):
                    if a not in pDic[ida][tStates[ida]]:
                        pDic[ida][tStates[ida]].append(a)



    for n in range(noa):
        f.write("\nAgent player_" + str(n) + "\n    Lobsvars = {state_player_" + str(n) + "};\n    Vars:\n        dummy : {none};\n    end Vars\n    Actions = {any_move")
        actions = []
        
        for act in pDic[n].values():
            for a in act:
                if a not in actions: actions.append(a)
        for ida, act in enumerate(actions):
            if act != "-":
                f.write(", " + act)


        f.write("};\n    Protocol:\n")

        for ids, state in enumerate(states[n]):
            f.write("        state_player_" + str(n) + " = " + state + " : {")
            
            if pDic[n][state] != ["-"]:
                for ida, act in enumerate(pDic[n][state]):
                    if ida > 0: f.write(", ")
                    f.write(act)
            else:
                first = True
                for ida, act in enumerate(actions):
                    if act != "-":
                        if not first: f.write(", ")
                        f.write(act)
                        first = False


            if len(pDic[n][state]) == 0 : f.write("any_move")
            f.write("};\n")
            
        f.write("    end Protocol\n    Evolution:\n        dummy = none if dummy = none;\n    end Evolution\nend Agent\n")


    f.write("\nEvaluation\n    won if (")
    for n in range(np.shape(loc)[1]):
        if n > 0: f.write(" and ")
        f.write("Enviroment.state_player_" + str(n) + " = win")

    f.write(");\nend Evaluation\n\nInitStates\n    ")
    for n in range(np.shape(loc)[1]):
        if n > 0: f.write(" and ")
        f.write("Enviroment.state_player_" + str(n) + " = start")

    f.write(";\nend InitStates\n\nGroups\n    players = {")
    for n in range(np.shape(loc)[1]):
        if n > 0: f.write(", ")
        f.write("player_" + str(n))

    f.write("};\nend Groups\n\nFormulae\n    <players>F won;\nend Formulae")
    
if __name__ == "__main__":

    if len(sys.argv) > 1:
        name = str(sys.argv[1])
    try:
        makeISPL(name)
    except TypeError as e:
        print(e)
