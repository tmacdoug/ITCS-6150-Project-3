import matplotlib.pyplot as plt
import networkx as nx
import time
import random

from algs import calc_chromatic_number, init_depth_first

#Function to transform an adjacency list into a list of edges for use in networkx
def generate_edges(adjacency):
    edges = []
    for item in adjacency.keys():
        for value in adjacency[item]:
            if (value, item) not in edges: edges.append((item, value))
    return edges


if __name__ == "__main__":
    #All possible colors (will be cut down based on chromatic number)
    colors = ['y', 'g', 'r', 'b', 'm']

    #Arguments to loop through
    args = {
        'Vanilla depth first search:': [False, False],
        'Forward checking, no singleton prop': [True, False],
        'Forward checking and singleton prop': [True, True]
    }
    heuristics = {
        'NO HEURISTICS': False,
        'MRV, DEGREE CONSTRAINT, LEAST CONSTRAINING VALUE': True
    }

    #US States adjacency list
    us_states = {
        "AL": ["FL", "GA", "MS", "TN"],
        "AK": [],
        "AZ": ["CA", "NV", "UT", "CO", "NM"],
        "AR": ["LA", "MS", "MO", "OK", "TN", "TX"],
        "CA": ["AZ", "NV", "OR"],
        "CO": ["AZ", "NM", "OK", "KS", "NE", "WY", "UT"],
        "CT": ["NY", "MA", "RI"],
        "DE": ["MD", "PA", "NJ"],
        "FL": ["AL", "GA"],
        "GA": ["FL", "AL", "TN", "NC", "SC"],
        "HI": [],
        "ID": ["WA", "OR", "NV", "UT", "WY", "MT"],
        "IL": ["WI", "IA", "MO", "KY", "IN"],
        "IN": ["MI", "OH", "KY", "IL"],
        "IA": ["MN", "WI", "IL", "MO", "NE", "SD"],
        "KS": ["NE", "MO", "OK", "CO"],
        "KY": ["IL", "IN", "OH", "WV", "VA", "TN", "MO"],
        "LA": ["AR", "MS", "TX"],
        "ME": ["NH"],
        "MD": ["DE", "PA", "VA", "WV"],
        "MA": ["CT", "NH", "NY", "RI", "VT"],
        "MI": ["WI", "IN", "OH"],
        "MN": ["IA", "WI", "ND", "SD"],
        "MS": ["AL", "AR", "TN", "LA"],
        "MO": ["IA", "IL", "KY", "TN", "AR", "OK", "KS", "NE"],
        "MT": ["ID", "ND", "SD", "WY"],
        "NE": ["SD", "IA", "MO", "KS", "CO", "WY"],
        "NV": ["ID", "UT", "AZ", "CA", "OR"],
        "NH": ["ME", "MA", "VT"],
        "NJ": ["DE", "PA", "NY"],
        "NM": ["AZ", "UT", "CO", "OK", "TX"],
        "NY": ["NJ", "PA", "VT", "MA", "CT"],
        "NC": ["VA", "TN", "GA", "SC"],
        "ND": ["MN", "SD", "MT"],
        "OH": ["PA", "WV", "KY", "IN", "MI"],
        "OK": ["KS", "MO", "AR", "TX", "NM", "CO"],
        "OR": ["CA", "NV", "ID", "WA"],
        "PA": ["NY", "NJ", "DE", "MD", "WV", "OH"],
        "RI": ["CT", "MA"],
        "SC": ["GA", "NC"],
        "SD": ["ND", "MN", "IA", "NE", "WY", "MT"],
        "TN": ["KY", "VA", "NC", "GA", "AL", "MS", "AR", "MO"],
        "TX": ["NM", "OK", "AR", "LA"],
        "UT": ["ID", "WY", "CO", "NM", "AZ", "NV"],
        "VT": ["NY", "NH", "MA"],
        "VA": ["KY", "MD", "NC", "TN", "WV"],
        "WA": ["ID", "OR"],
        "WV": ["OH", "PA", "MD", "VA", "KY"],
        "WI": ["MI", "MN", "IA", "IL"],
        "WY": ["MT", "SD", "NE", "CO", "UT", "ID"]
    }
    
    #Australian states adjacency lits
    au_states = {
        'ACT': ['NSW'],
        'NSW': ['ACT', 'QLD', 'SA', 'VIC'],
        'NT': ['QLD', 'SA', 'WA'],
        'QLD': ['NSW', 'NT', 'SA'],
        'SA': ['NSW', 'NT', 'QLD', 'VIC', 'WA'],
        'TAS': [],
        'VIC': ['NSW', 'SA'],
        'WA': ['NT', 'SA']
    }
    

    
    #Do US states
    edges = generate_edges(us_states)
    
    #Display chromatic number of US
    chromatic_num = calc_chromatic_number(us_states)
    print('Chromatic number of US states:', chromatic_num)
    
    #Keep track of stats
    stats = {key:{'backtracks':0, 'time':0} for key in args.keys()}

    #Limit domain of colors to the chromatic number
    colors_domain = colors[0:chromatic_num]
    print('----USA----')
    #Iterate through each required combination of arguments
    for h in heuristics.keys():
        print(f'-----{h}------')
        for i in range(5): #Repeat 5 times for each argument (new order of states each time)
            #Randomize state order
            shuffled_keys = list(us_states.keys())
            random.shuffle(shuffled_keys)
            us_states_shuffled = {key:us_states[key] for key in shuffled_keys}
            for arg in args.keys():
                #Perform depth-first search for US
                start = time.time()
                res, backtracks = init_depth_first(us_states_shuffled, colors_domain, forward_checking=args[arg][0], propagation=args[arg][1], heuristics=heuristics[h])
                end = time.time()
                print(f'---{arg} (Trial {i+1})---')
                print(f'Backtracks: {backtracks}\tExecution time: {end-start}')
                
                #Add trial to stats
                stats[arg]['backtracks'] += backtracks
                stats[arg]['time'] += end-start

        #Take average of stats
        for key in stats.keys():
            for i in stats[key].keys():
                stats[key][i] = stats[key][i]/5
        #Display stats
        print(f'-----Final Averages-----\n{stats}')
    
    #Display final result
    G = nx.Graph()
    G.add_nodes_from(us_states_shuffled)
    G.add_edges_from(edges)
    node_colors = [res.get(node) for node in G.nodes()]
    nx.draw_circular(G, with_labels=True, node_color=node_colors)
    plt.show()
    
    #Do AU states
    edges = generate_edges(au_states)
    
    #Display chromatic number of AU
    chromatic_num = calc_chromatic_number(au_states)
    print('Chromatic number of AU states:', chromatic_num)

    #Keep track of stats
    stats = {key:{'backtracks':0, 'time':0} for key in args.keys()}
    
    #Limit domain of colors to the chromatic number
    colors_domain = colors[0:chromatic_num]
    print('----Australia----')
    #Iterate through each required combination of arguments
    for h in heuristics.keys():
        print(f'-----{h}------')
        for i in range(5): #Repeat 5 times for each argument (new order of states each time)
            #Randomize state order
            shuffled_keys = list(au_states.keys())
            random.shuffle(shuffled_keys)
            au_states_shuffled = {key:au_states[key] for key in shuffled_keys}
            for arg in args.keys():
                #Perform depth-first search for AU
                start = time.time()
                res, backtracks = init_depth_first(au_states_shuffled, colors_domain, forward_checking=args[arg][0], propagation=args[arg][1], heuristics=heuristics[h])
                end = time.time()
                print(f'---{arg} (Trial {i+1})---')
                print(f'Backtracks: {backtracks}\tExecution time: {end-start}')

                #Add trial to stats
                stats[arg]['backtracks'] += backtracks
                stats[arg]['time'] += end-start
    
        #Take average of stats
        for key in stats.keys():
            for i in stats[key].keys():
                stats[key][i] = stats[key][i]/5
        #Display stats
        print(f'-----Final Averages-----\n{stats}')
    
    
    #Show AU
    G = nx.Graph()
    G.add_nodes_from(au_states)
    G.add_edges_from(edges)
    node_colors = [res.get(node) for node in G.nodes()]
    nx.draw_circular(G, with_labels=True, node_color=node_colors)
    plt.show()