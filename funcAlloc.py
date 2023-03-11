from itertools import permutations

def get_permutations(companies):
    
    perms_memory = permutations(companies)
    perms_agg = list(perms_memory)
    perms = [*set(perms_agg)]
    return perms

#########################################################

def get_values(permutations,bids):

    revised_lists = []
    
    for i in range(len(permutations)):
        sublist = permutations[i]
        
        tots = []

        for j,i in enumerate(sublist):
                placehold = bids[j][i]
                tots.append(placehold)
                
        revised_lists.append(tots) 
    return revised_lists

#########################################################

def get_sorted_pairs(permutations,values):

    zipped = list(zip(permutations, values))
    zipped_sorted = sorted(zipped, key=lambda x: sum(x[1]))
    return zipped_sorted

#########################################################

def final_message(pairs):
    output = ""
    for i, combination in enumerate(pairs, start=1):
        output += f"Comb {i}: {', '.join(combination[0])} <> Total: ${sum(combination[1])}\n"
        
    return output

#########################################################
def optimized(pairs):
    output = ""
        
    output += f"Total: ${sum(pairs[0][1])} for {', '.join(pairs[0][0])}"
    return output

  
