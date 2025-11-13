

def check_neighbors(adjacency, node, assigned, col):
    neighs = adjacency[node]
    for neigh in neighs:
        if assigned[neigh] == col: return False
    return True

def calc_chromatic_number(adjacency):
    colors = {}
    degs = [(len(adjacency[i]), i) for i in adjacency.keys()]
    degs.sort(reverse=True)
    
    for deg, vert in degs:
        neighbor_colors = {colors.get(neigh) for neigh in adjacency[vert]}
        colors[vert] = next(color for color in adjacency.keys() if color not in neighbor_colors)
    return len(set(colors.values()))


def init_depth_first(adjacency, colors, forward_checking=False, propagation=False, heuristics=False):
    #Sort adjacency list
    #sorted_keys = ad#sorted(adjacency, key=lambda k: len(adjacency[k]), reverse=True)
    #adjacency = {sorted_keys[i]:adjacency[sorted_keys[i]] for i in range(len(sorted_keys))}

    global BACKTRACKING
    BACKTRACKING = 0

    #Generate domain, and an empty list to hold color assignments
    domains = {key:list(colors) for key in adjacency.keys()}
    assigned = {key:'' for key in adjacency.keys()}
    
    #Begin search
    #print(forward_checking, propagation)
    res = depth_first(adjacency, colors, assigned, domains, forward_checking=forward_checking, propagation=propagation, heuristics=heuristics)
    #print(f'Backtracking: {BACKTRACKING}')
    return res, BACKTRACKING

def depth_first(adjacency, colors, assigned, domains, forward_checking=False, propagation=False, heuristics=False):
    #Find next unassigned node if no heuristics
    if not heuristics:
        node = next(iter(x for x in assigned if assigned[x]==''), 'SUCC')
        sorted_colors = domains[node]
    else:
        #Check if all nodes have been assigned
        unassigned = [x for x in assigned if assigned[x] == '']
        if not unassigned:
            node = 'SUCC'
        else: #Order variables based on the following heuristics: MRV, degree constraint, domain sorted by LCV
            #Minimum remaining value
            min_domain = min(len(domains[v]) for v in unassigned)
            mrv = [v for v in unassigned if len(domains[v]) == min_domain]

            #Degree constraint
            if len(mrv) > 1:
                node = max(mrv, key=lambda v: sum(1 for n in adjacency[v] if assigned[n] == ''))
            else:
                node = mrv[0]

            #Define key for Least Constraining Value
            def lcv_sort(color):
                #Count neighbor domain conflicts
                conflicts = 0
                for neigh in adjacency[node]:
                    if assigned[neigh] == '':
                        if color in domains[neigh]:
                            conflicts += 1
                return conflicts
            #Sort domain by key
            sorted_colors = sorted(domains[node], key=lcv_sort) #Sort by number of conflicts for each color (less is better)

    
    if node == 'SUCC': #All nodes have been assigned, return assignments
        return assigned

    #Test each color
    for col in sorted_colors:
        global BACKTRACKING
        if check_neighbors(adjacency=adjacency, node=node, assigned=assigned, col=col) == True:
            #No neighbors share a color; assign it to the node, and continue searching
            assigned[node] = col

            #Backup domains for backtracking
            old_domains = {key: list(val) for key, val in domains.items()}

            #Perform forward checking
            if forward_checking:
                cont = True
                for neigh in adjacency[node]: #Check each unassigned neighbor
                    if assigned[neigh] == '':
                        if col in domains[neigh]:
                            domains[neigh].remove(col)
                            #Only continue checking if this assignment doesn't make the neighbor domain empty
                            if not domains[neigh]:
                                cont = False
                                break
                if not cont:
                    #Unassign color and backtrack
                    BACKTRACKING +=1
                    domains = old_domains
                    assigned[node] = ''
                    continue
            
            #Propogation through singleton domains
            if propagation:
                changed = True
                while changed:
                    changed = False
                    cont = True

                    #Find all singleton domains and iterate through them
                    singletons = [n for n in adjacency if assigned[n] == '' and len(domains[n]) == 1]
                    for s in singletons:
                        if not domains[s]:
                            cont = False
                            break
                        forced_color = domains[s][0]

                        if check_neighbors(adjacency, s, assigned, forced_color):
                            assigned[s] = forced_color
                            # Apply forward checking again for this forced node
                            for neigh in adjacency[s]:
                                if assigned[neigh] == '':
                                    if forced_color in domains[neigh]:
                                        domains[neigh].remove(forced_color)
                                        if not domains[neigh]:
                                            cont = False
                                            break
                            if not cont:
                                break
                            changed = True
                        else:
                            cont = False
                            break
                    if not cont:
                        break
                if not cont:
                    BACKTRACKING +=1
                    domains = old_domains
                    for n in assigned:
                        if n not in old_domains: continue
                    assigned[node] = ''
                    continue

            #Continue search
            res = depth_first(adjacency=adjacency, colors=colors, assigned=assigned, domains=domains, forward_checking=forward_checking, propagation=propagation)
            if res != False: #Success state found
                return res
            
            #Backtrack
            BACKTRACKING +=1
            assigned[node] = ''
            domains = old_domains

            
            
    return False #No colors checked found a success state, return false