import matplotlib.pyplot as plt
from matplotlib import gridspec
import textwrap
import gspread
import json
import os
import sys
sys.path.insert(0,os.path.expanduser("~/Documents/BergmanLab_repos/oliver/scripts/"))
from olivers_utils import jprint

def setting_graph(data, questions):
    names = [name for name in data]
    jprint(data)

    fig, axes = plt.subplots(4,3, figsize=(10,10))
    plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.3)
    axis = [0,0]
    setting_likert = ["","Uninterested","Somewhat uninterested","Neutral","Somewhat interested","Interested","Very interested!"]
    likert_colors = ["grey","firebrick","orange","gold","greenyellow","green","turquoise"]

    for q in range(12):
        print(questions[q])
        plot = axes[axis[0],axis[1]]
        plot.set_title(questions[q].split("[")[1].split("]")[0].split("(")[0].strip())
        q_data = [setting_likert.index(data[person][q]) for person in data]
        q_names = [names[i] for i in range(5) if q_data[i]]
        q_data = [i for i in q_data if i]
        try:
            q_colors = [likert_colors[i] for i in q_data]
        except: print(q_data)
        q_data = [i-0.9 for i in q_data if i]
        plot.barh(q_names,q_data,color=q_colors)
        plot.set_xlim(xmax=5.3)
        plot.get_xaxis().set_visible(False)
        if axis[1] < 2:
            axis[1] += 1
        else:
            axis[1] = 0
            axis[0] += 1
    
    plt.show()

def preferences_graph(data, questions):
    names = [name for name in data]

    people_colors = {
        "Sam":"blue",
        "Rory":"green",
        "Des":"purple",
        "Grey":"teal"
    }

    options = [
        ["You all tell me what your characters plan to do at the end of the campaign, and I extrapolate everything from there, taking over decision making for those characters and how they react to changes in the world.","You tell me what your characters plan to do at the end of the campaign. Whenever I think their decisions might affect the course of history, I ask you what they would do in that situation.","I give you hints and updates about the planning process.","I ask for your input about major historical events that don't necessarily involve your characters.","I tell you as little as possible!"],
        ["It's a secret. Make your characters rediscover it.","Find a way for your characters to already know the broad strokes."],
        ["History is a mystery. Make your characters uncover what has happened since the end of Archia 1.","You already know any major historical events that wouldn't involve some plot reason for knowledge to be lost."],
        ["Keep it a secret","Share the knowledge with a trusted few or an organization","Disseminate the knowledge pretty widely"],
        ["Characters don't know/aren't connected to each other and meet for the first time","Characters don't know each other but are drawn together based similar knowledge/connections","Characters already work together or are associated with the same organization","Characters all have some secret and/or specialized knowledge about the first arc conflict","Characters are only as knowledgeable as the average person about plot info"]
    ]
    wrapped_options = [[textwrap.fill(q,150,break_long_words=False) for option in o] for o in options]
    plot_heights = [len("\n".join(o).split("\n"))+0.5*(len(o)-1) for o in wrapped_options]
        
    fig, axes = plt.subplots(5,10, figsize=(10,10))
    gs = gridspec.GridSpec(5,10,height_ratios=[])
    plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.3)
    axis = [0,0]

    for q in range(14,19):
        plot = axes[q-14,9]
        for x in range(9):
            axes[q-14,x].set_visible(False)
        plot.set_title(questions[q])
        plot.set_xlim(xmax=4.5)
        q_options = options[q-14]
        plot.set_yticks(range(len(q_options)))
        wrapped_qs = [textwrap.fill(q,150,break_long_words=False) for q in q_options]
        plot.set_yticklabels(wrapped_qs)
        plot_height = len("\n".join(wrapped_qs).split("\n"))+0.5*(len(q_options)-1)
        plot.set_figsize(plot_height)
        dot_plot_counts = [0.5 for _ in q_options]
        for player in people_colors:
            player_column = [player for player in data].index(player)
            player_x = []
            player_y = []
            for a in range(len(q_options)):
                if q_options[a] in data[player][q]:
                    player_y.append(a)
                    player_x.append(dot_plot_counts[a])
                    dot_plot_counts[a] += 1
            plot.scatter(player_x,player_y,color=people_colors[player])
    
    for q in range(14,19):
        print(questions[q])
    
    #plt.show()



def main():
    gc = gspread.service_account()
    table = gc.open_by_key("1-aTmGRGf3Aw2lNxl2lZEH4hMfhA3uUKHS5pv7bKW0tA").worksheet("Form Responses 1").get_values()

    data = {line[1]:line[2:] for line in table[1:]}
    questions = table[0][2:]
    #setting_graph(data,questions)

    preferences_graph(data,questions)
    



if __name__ == "__main__":
    main()