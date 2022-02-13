#compiler for molecuscript

#currently getting and outputting the length alkanes -done!
#now getting the other molecules within 
#goes up to 99 for the main chain


#cyclic molecules get turned into single chains as i never need to loop over them more than once
#still would be good to tell wether they are a cyclic or not tho

#this should print "e":
#  3-(1-phospho-1-(2,4-bis(methyl)cyclobutyl)methyl)-4-(1-sulfyl-1-phosphoethyl)hexane

#hello world:
# 1-(1-oxy-1-sulfyl-1-(2-(2,3,4-tris(methyl)cyclobutyl)-3-(2-ethylcyclopropyl)cyclopropyl)methyl)-1-(1-oxy-1-sulfyl-1-(2-(2-methyl-4-octylcyclobutyl)-3-(2-methylcyclopropyl)cyclopropyl)methyl)-4-(1-phospho-1-(2-heptyl-3-ethylcyclopropyl)methyl)-5-(1-phospho-1-(2,4-bis(methyl)cyclobutyl)methyl)-7,7,18-tris(1-phospho-2-oxy-2-(2-methylcyclopropyl)ethyl)-10,15-bis(1-phospho-2-oxy-2-(2-ethylcyclopropyl)ethyl)-11-(1-phospho-1-(2-propyl-3-ethylcyclopropyl)methyl)-12-(1-phospho-1-(2,3-bis(butyl)cyclopropyl)methyl)-13-(1-phospho-1-(2-octyl-3-heptylcyclopropyl)methyl)-16-(1-phospho-1-(2,3-bis(methyl)-4-butylcyclobutyl)methyl)-19-(1-phospho-1-(2-methylcyclobutyl)methyl)-20-(1-phospho-1-(2,3-bis(propyl)cyclopropyl)methyl)-21-(1-sulfyl-1-phosphomethyl)henicosane

"""
add H
allocate o and l to memory
add e
add l from memory
add l from memory
add o from memory
add ,
add  
add W
add o from memory
add r
add l from memory
add d
add !
"""


"""
work out and slice off the base alkane from the end of splitted res first, itl make things easier
"""

def is_int(string: str) -> int:
    """
    Checks wether the given string represents an integer.
    """
    try:
        int(string)
        return True
    except:
        return False

def underscore_nested(chain: str) -> str:
    """
    Converts the dashes inside brackets to underscores for splitting
    """
    inbracket = 0
    chain = list(chain)
    for index, char in enumerate(chain):
        if char == "(":
            inbracket += 1
        elif char == ")":
            inbracket -= 1
        if inbracket != 0 and char == "-":
            chain[index] = '_'
    chain = ''.join(chain)
    return chain

def split_chain(chain: str) -> str:
    """
    parses the chain a bit, mostly splitting, assumes the base alkane has been cut off the end
    example: 
        "1-iodo-1,2-bis(2,3_difluoropropyl)-5-ethyl" -> [[[1], 'iodo'], [[1, 2], 'bis(2,3-difluoropropyl)'], [[5], 'ethyl']]
    """

    chain = underscore_nested(chain).split("-")
    #print(chain)
    chain = [chain[i:i+2] for i in range(0, len(chain), 2)]
    #print(chain)
    chain = [[[int(i) for i in elm[0].split(",")], elm[1].replace("_", "-")] for elm in chain]
    #print(chain)

    return chain

def strip_base_alkane(chain: str, end:str="ane") -> list:
    """
    Gets rid of the base alkane from a chain and returns both the stripped chain and the length of the stripped alkane.
    """

    # nona pentacont yl
    # nona pentacont

    singles = {
        "meth": 1,
        "eth": 2,
        "prop": 3,
        "but": 4,
        "pent": 5,
        "hex": 6,
        "hept": 7,
        "oct": 8,
        "non": 9,
    }
    prefixes = {
        "hen": 1,
        "do": 2,
        "tri": 3,
        "tetra": 4,
        "penta": 5,
        "hexa": 6,
        "hepta": 7,
        "octa": 8,
        "nona": 9,
    }
    suffixes = {
        "dec": 10,
        "cos": 20,
        "triacont": 30,
        "tetracont": 40,
        "pentacont": 50,
        "hexacont": 60,
        "heptacont": 70,
        "octacont": 80,
        "nonacont": 90,
    }

    if not chain.endswith(end):
        #print(chain, end)
        #raise ValueError(f"Chain didnt have suffix {end}")
        return chain
    chain = chain[:-len(end)]
    length = 1

    for suffix in suffixes:
        if chain.endswith(suffix):
            if suffix == "dec":
                prefixes.pop("hen")
                prefixes.update({"un": 1})
            elif suffix == "cos":
                prefixes.pop("hen")
                prefixes.update({"heni": 1})
                prefixes.update({"i": 0})
            chain = chain[:-len(suffix)]
            length = suffixes[suffix]
    
    if length == 1:#one of the singles that isnt decane
        length = 0
        for prefix in singles:
            if chain.endswith(prefix):
                chain = chain[:-len(prefix)]
                length = singles[prefix]
        if length == 0:
            raise ValueError(f"Chain was invalid.")
    
    for prefix in prefixes:
        if chain.endswith(prefix):
            chain = chain[:-len(prefix)]
            length += prefixes[prefix]

    is_cyclic = False
    if chain.endswith("cyclo"):
        chain = chain[:-5]
        is_cyclic = True
        #length = float(length)


    return [chain, length, is_cyclic]

def format_bracketed(elm: list) -> list:
    """
    Formats nested chains into their own list, if it fails it returns the same object that was passed to it.
    """
    nested_prefixes = { #used to see wether the next thing is a nested bracket
        "bis": 2,
        "tris": 3,
        "tetrakis": 4,
        "pentakis": 5,
        "hexakis": 6,
        "heptakis": 7,
        "octakis": 8,
        "nonakis": 9
    }
    chain = elm[1]
    indexes = elm[0]
    given_chain = elm[1]

    multiplier = 0

    for prefix in nested_prefixes:
        if chain.startswith(prefix):
            multiplier = nested_prefixes[prefix]
            chain = chain[len(prefix):]

    if chain.startswith("(") and chain.endswith(")"):
        if multiplier == 0:
            multiplier = 1
        chain = chain[1:-1]

    if multiplier == 0:
        return [indexes, given_chain]
    else:
        return [indexes, chain]

    if len(indexes) != multiplier:
        raise ValueError("Number of indexes does not match multiplier parsed.") #might be a bug here where its only worth raising an error if it truly is meant to be nested

def strip_alkyne(elm: list) -> list:
    #print(elm)
    chain = elm[1]
    given_chain = elm[1]
    index_list = elm[0]
    try: 
        #print(chain, 'e')
        chain, length, is_cyclic = strip_base_alkane(chain, "yl")
        #print(chain, length, 'e')
        if chain == "":
            return [[], length]
    except:
        return [index_list, given_chain]

def format_halogen(elm: list) -> list:
    """
    Attempts to format halogen groups to their elements, if it fails it returns the same object as was passed to it.
    """
    #inputs and results would be [[1, 2, 3], "tribromopropyl"] -> same
    # [[2, 4], "difluoro"] -> [[2, 4], "F"]
    num_prefixes = { #ill make this go up to 100 later
        "di": 2,
        "tri": 3,
        "tetra": 4,
        "penta": 5,
        "hexa": 6,
        "hepta": 7,
        "octa": 8,
        "nona": 9,
        "deca": 10,
    }
    elem_prefixes = {
        "bromo": "Br",
        "chloro": "Cl",
        "iodo": "I",
        "fluoro": "F", #ill add tennesine later
        "astato": "At",
        "oxy": "O",
        "phospho": "P",
        "nitro": "N",
        "sulfyl": "S"
    }
    if len(elm[1]) == 0:
        return elm

    given_chain = elm[1]
    chain = elm[1]
    indexes = elm[0]
    multiplier = 0
    for prefix in num_prefixes:
        if chain.startswith(prefix):
            if prefix == "tri":
                if chain.startswith("tria"):
                    continue
            if prefix == "tetra":
                if chain.startswith("tetrac"):
                    continue
            multiplier = num_prefixes[prefix]
            chain = chain[len(prefix):]
    
    for prefix in elem_prefixes:
        if chain.startswith(prefix):
            mol = elem_prefixes[prefix]
            chain = chain[len(prefix):]
            if multiplier == 0:
                multiplier = 1

    #print(multiplier, indexes, chain, elm, given_chain)
    if multiplier != len(indexes):
        return [indexes, given_chain] #probably bis(blehbleh)
        raise ValueError("Number of indexes doesnt match multiplier prefix")
    


    if chain == "": #properly formatted
        #print(indexes, chain)
        return [indexes, mol]
    else:#not single halogen
        return [indexes, given_chain]

def format_input(chain: str, end:str) -> list:
    #print(chain, end)
    chain, length, is_cyclic = strip_base_alkane(chain, end)
    #print(chain, end)
    
    if chain == "":
        #print(is_cyclic)
        if is_cyclic:
            return tuple([[], length])#tuple([() for g in range(length)])
        return [[], length]#tuple([() for g in range(length)])
    chain = underscore_nested(chain)
    chain = split_chain(chain)
    #print(chain)
    for index, elm in enumerate(chain):
        old_elm = elm
        #elm = strip_base_alkane(chain, "yl")
        #print(elm)
        #elm = strip_alkyne(elm)
        #print(elm)

        #if elm == old_elm:
        elm = format_halogen(elm)
        
        if elm == old_elm:
            elm = format_bracketed(elm)
            #print(elm)
            elm[1] = format_input(chain=elm[1], end="yl")
        chain[index] = elm
    if is_cyclic:
        return (chain, length)
    return [chain, length]

def turn_into_molecule(elm: list, molecule: list) -> list:
    """
    formats the tree of molecules to a list of the groups

    propane
    [[], [], []]

    1-bromopropane
    [['Br'], [], []]

    1-ethyl-1-bromopropane
    ( (  'Br', ( (), () )  ), (), () )

    """

    #print("evaluating: ", elm)
    if type(elm[1]) == int: #unformatted chain
        #print("A")
        #do thing with new molecule
        length = elm[1]
        content = elm[0]
        #is_cyclic = False
        #if type(length) == float:
        #    is_cyclic = True
        #    length = int(length)

        molecule = [[] for g in range(length)] #new molecule

        for group in content:
            molecule = turn_into_molecule(group, molecule)
    elif type(elm[1]) == str: #halogen
        #print("B")
        indexlist = elm[0]
        halogen = elm[1]
        for index in indexlist:
            molecule[index-1] += [halogen]
            #print(molecule)
    elif type(elm[1]) == list or type(elm[1]) == tuple: #unformatted nested
        #print("C")
        indexlist = elm[0]
        group = elm[1]
        group = turn_into_molecule(group, [])
        for index in indexlist:
            molecule[index-1] += [group]
            #print(molecule)

    if type(elm) == tuple:
        molecule = tuple(molecule)
    return molecule

def check(molecule):
    """
    makes sure molecule is valid
    """
    for group in molecule:
        pass#if len(group) > 2:
        #    raise ValueError("each carbon cannot have more than side branches")

def convert_to_number(ring, memory:list=[]):
    uses_pointer = False
    if type(ring) == list:
        if len(ring) == 2 and ring[0] == "O":
            uses_pointer = True
            ring = ring[1]
            
    #print('a', ring)
    #if type(ring) == list and len(ring) == 1:
    #    ring = ring[0]
    #ring = ring[1:]
    #print('b', ring)
    number = ""
    for index, group in enumerate(ring):
        if len(group) == 1:
            #if len(group[0]) != 0:
            number = number + str(len(group[0]))
        else:
            number = number + '0'
        #print(number, index, group)
        #number = number+str(len(group))
        #total += len(group)*(10**index)
    
    #print(total, ring)
    #print(number, ring)
    if uses_pointer:
        #print(memory, number, int(number))
        number = memory[int(number)]
    else:
        number = int(number)
    return number

def execute(molecule):
    index = 0
    memory = [0 for g in range(99)]
    print_buffer = []

    while index < len(molecule):
        
        groups = molecule[index]


        if groups == []:
            index += 1 
            continue

        #groups = groups[0]
        #print(groups)

        is_sulfur = False
        value = 0
        for group in groups:
            if len(group) == 1:
                group = group[0]
            if "S" in group:
                is_sulfur = True
                group.remove("S")
            #print(group, is_sulfur)

            #print(group, is_sulfur, "X", [f"{index}: {value}" for index, value in enumerate(memory) if value != 0])
            if is_sulfur:
                if "P" in group: #print flush
                    group.remove("P")
                    print(''.join(print_buffer))
                    print_buffer = []

                if "O" in group: #write to memory as well as get value
                    #print("AAAA")
                    group.remove("O")
                    #the only thing in the group left should be a cyclopropane
                    #and the cyclopropane has a number ring at index 2 which is the value
                    #and also a number ring at index 3 which is the pointer
                    cyclopropane = group[0]
                    value = cyclopropane[1][0]
                    pointer = cyclopropane[2][0]

                    pointer = convert_to_number(pointer)

                    value = convert_to_number(value)
                    #print(cyclopropane, value, pointer)

                    memory[pointer] = value
                    #print(sum(memory))
            else:
                #print("F", group)
                if type(group[0]) == list:
                    starting_token = group[0][0]
                    other = group[1]
                else:
                    starting_token = group[0]
                    other = group[1]
                if starting_token == "P":
                    char = chr(convert_to_number(other, memory))
                    #print(char, ord(char))
                    print_buffer += [char]
                #if len(group) == 1:
                #    starting_token = group[0]
                #    group = group[1]
                #
                #else:
                #    starting_token = group[0][0]
                ##starting_token = group[0]
                #
                #if starting_token == "P": #add to print buffer
                #    #oxygen check is already implemented
                #    print('e', group)
                
                    

                #print(group)
                continue
                print("A", group)
                if "P" in group[0]: #add to print buffer
                    if len(group) == 1:
                        pass
                    print('e', group)
                    if "O" in group: #get from memory
                        print("EEEEE")
                        group.remove("O")
                        pointer_ring = group[0]
                        pointer_value = convert_to_number(pointer_ring)
                        value = memory[pointer_value]
                    else: 
                        value_ring = group[0]
                        value = convert_to_number(value_ring)
                    print_buffer += [chr(value)]
                    #print("PPPPP ", group)
        
        
        #print(f"break, print buffer is: {print_buffer}, memory sum is {sum(memory)}")

        #group = group[0]
        ##print(group, sum(memory), print_buffer, index)
#
        #now its guranteed to actually have something in it



        #if "P" in group[0]:
            ##print("A")
            #if is_sulfur:
            #    print(''.join(print_buffer))
            #    print_buffer = []
            #    #print("B")
            #else:
            #    #print("C")
            #    group[0].remove("P")
            #    using_pointer = False
            #    if "O" in group[0]:
            #        using_pointer = True
            #        group[0].remove("O")
#
            #    #removed 2 values maximum, group[0] must be a ring
            #    value = convert_to_number(ring=group[0][0])
            #    #print(value, group)
            #    if using_pointer:
            #        value = memory[value]
                #
            #    print_buffer += [str(chr(value))]

        
        
        
        index += 1

    
def main():
    #print(strip_base_alkane("tetratriacontyl", end="yl"))
    while 1:
        chain = input("> ")
        try:
            res = format_input(chain, "ane")
            molecule = turn_into_molecule(res, [[] for g in range(res[1])])
            print("\nMolecule:\n", molecule, "\n")
            print("Executing...")#: {molecule}")
            execute(molecule)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
