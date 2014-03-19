def cartesian():
    """User-input processing function. If a user's input ends with a backslash,
    according to the rules of bash, the prompt must wait for more input, unless
    the backslash has been escaped. 
    """
    cumulative_s = ""
    backslash_not_counted = True
    while backslash_not_counted or backslash_count%2 == 1:
        s = raw_input("Enter Input:")
        backslash_count = 0
        i = len(s) - 1
        while s[i] == "\\" and i > -1:
            backslash_count += 1
            i -= 1
        backslash_not_counted = False
        cumulative_s = cumulative_s + s
    cartesianProductPrinter(cumulative_s)

def cartesianProduct(string):
    """The main "public" method for Cartesian expansion. Returns
    the cartesian expansion of the input string, in the form of a
    list of strings. Note that when text entered in bash is undergoing
    Cartesian expansion, bash treats unescaped space characters as
    argument delimiters.

    An IndexError is raised if the final character is an unescaped backslash. 
    """
    args = split_with_escaping(string, split_char=" ")
    output_list = []
    for item in args:
        output_list.extend(resolve_string(item))
    return output_list

def resolve_string(string):
    """Returns a resultant list of strings from the Cartesian expansion
    of the input string. This function may be called to resolve a string
    at the top-level of the Cartesian Product string OR to resolve a string
    separated within a brace block by a comma.
    """
    #   Given any string undergoing Cartesian expansion, it is possible
    #   to split the string based on the content *before* a top level
    #   nested brace pair, the content after, and the content in braces.
    #
    #   The code can then act recursively on these segments until it
    #   reaches a base case. The base cases and some of the handling
    #   changes depending on whether the string had been captured in
    #   braces. For this reason, separating resolve_string and resolve_braces,
    #   while resulting in mild code repetition, helps to add mental
    #   organization to the problem flow.

    brace_pair = outer_brace_finder(string)
    if len(brace_pair) == 0:
        return [unescape_string(string)]
    obrace, cbrace = brace_pair[0], brace_pair[1]
    
    left = resolve_string(string[0:obrace])
    middle = resolve_braces(string[obrace+1:cbrace])
    output_list = stringListDistribute(left,middle)
    right = resolve_string(string[cbrace+1:])
    
    output_list = stringListDistribute(output_list, right)
    return output_list

def resolve_braces(string):
    """Returns a resultant list of strings from the Cartesian
    expansion of the input string, provided that the input string
    had been preceeded by an open brace and succeeded by a closed
    brace. More specifically, resolve_braces should only be called
    on a string that is located within a valid brace pair. 
    """
    brace_pair = outer_brace_finder(string)
    output_list = []
    if len(brace_pair) == 0:
        comma_separated = split_with_escaping(string)
        if len(comma_separated) == 1:
            return ["{" + unescape_string(comma_separated[0]) + "}"]
        else:
            for item in comma_separated:
                output_list.append(unescape_string(item))
            return output_list
    
    obrace, cbrace = brace_pair[0], brace_pair[1]
    left = string[0:obrace]
    middle = string[obrace+1:cbrace]
    right = string[cbrace+1:]

    # When a string is encapsulated in braces, top-level commas
    # are significant.
    # According to the "rules" of expansion, the last element
    # in the left list gets distributed over the elements
    # yielded from resolving the its adjacent brace pair.
    
    left_list = split_by_top_level_commas(left)
    rightmost_left = left_list.pop()
    for item in left_list:
        output_list.extend(resolve_string(item))

    mid_list = \
        stringListDistribute(resolve_string(rightmost_left),
                             resolve_braces(middle))

    right_list = split_by_top_level_commas(right)
    leftmost_right = right_list.pop(0)
 
    # Similar to the last element in the left list above, the first
    # element in the right list gets distributed. 
    mid_list = stringListDistribute(mid_list,
                                    resolve_string(leftmost_right))
    output_list.extend(mid_list)
    for item in right_list:
        output_list.extend(resolve_string(item))

    return output_list
    
def split_by_top_level_commas(string):
    """Returns a list of strings such that each element is as divided by
    the top-level commas only. A string has top-level commas if it contains
    a comma not enclosed in a valid pair of braces.

    Example:
    "a,b" returns ["a", "b"]
    ",{a,b}" returns ["", "{a,b}"]
    "ab{c,d}e,f" returns ["ab{c,d}e", "f"]
    """
    top_level_braces = top_level_brace_pairs(string)
    if len(top_level_braces) == 0:
        return split_with_escaping(string)
    output_list = []
    start_index = 0
    temp_string = ""
    
    # Essentially, this block runs a split on strings on either
    # side of braces, and makes sure to combine the last element
    # of the left-side array with the first element of the right-side
    # array, for each brace. 
    for pair in top_level_braces:
        s = split_with_escaping(string[start_index:pair[0]])
        temp_string += s.pop(0)
        if len(s) > 0:
            output_list.append(temp_string)
            temp_string = s.pop()
            output_list.extend(s)
        temp_string += string[pair[0]:pair[1]+1]
        start_index = pair[1] + 1
        
    s = split_with_escaping(string[start_index:])
    temp_string += s.pop(0)
    output_list.append(temp_string)
    output_list.extend(s)
    return output_list

def top_level_brace_pairs(string):
    """Returns a list of tuples containing indices of every top level brace
    pair in the string, ordered by lowest index first.

    Example:
    "{a}{b}" returns [(0, 2), (3, 5)]
    """
    top_level_brace_pairs = []
    last_closed_brace = -1
    next_top_level_braces = outer_brace_finder(string)
    while len(next_top_level_braces) > 1:
        open_brace = next_top_level_braces[0] + last_closed_brace + 1
        closed_brace = next_top_level_braces[1] + last_closed_brace + 1
        last_closed_brace = closed_brace
        
        top_level_brace_pairs.append((open_brace, closed_brace))
        next_top_level_braces = outer_brace_finder(string[closed_brace + 1:])
    return top_level_brace_pairs

def outer_brace_finder(string):
    """Returns the indices of the first valid non-nested brace pair in
    the string as a list. Returns an empty list if there are no valid
    pairs. 
    """
    i = 0
    depth_list = [] 
    depth = 0
    while i < len(string):
        if string[i] == '\\':
            i = i + 2
            continue
        elif string[i] == "{":
            if depth > len(depth_list)-1:
                depth_list.append([i])
            depth += 1
        elif string[i] == "}" and depth > 0:
            if depth_list[depth-1] and len(depth_list[depth-1])==1:
                depth_list[depth-1].append(i)
            depth -= 1
            if depth == 0:
                break
        else:
            pass
        i = i + 1
    try:
        return depth_list[depth]
    except IndexError:
        return []

def unescape_string(string, escape_char='\\'):
    """Reformats a string's escaped characters and returns a string. In bash,
    characters following escape_char are added to the output and escape_char is
    removed. 
    """
    i = 0
    temp_str_list = []
    while i < len(string):
        if string[i] == escape_char:
            try:
                temp_str_list.append(string[i+1])
                i+=2
            except IndexError:
                msg = "The string was terminated with an unescaped backslash."
                raise UnescapedBackslashTerminatedStringException(msg)
                                                    
        else:
            temp_str_list.append(string[i])
            i += 1
    return "".join(temp_str_list)

def split_with_escaping(string, split_char=',', escape_char='\\'):
    """Splits a string delimited by split_char, except when split_char has
    been escaped by escape_char. Returns a list of strings. 
    """
    output_list=[]
    temp_str_list = []
    i = 0
    while i < len(string):
        if string[i] == escape_char:
            temp_str_list.append(string[i])
            # check bash behavior here
            if i+1 < len(string):
                temp_str_list.append(string[i+1])
            i = i + 2
            continue
        elif string[i] == split_char:
            temp_str = "".join(temp_str_list)
            output_list.append(temp_str)
            temp_str_list = []
        else:
            temp_str_list.append(string[i])
        i += 1
    temp_str = "".join(temp_str_list)
    output_list.append(temp_str)
    return output_list
        
def stringListDistribute(stringlist1, stringlist2):
    """Returns a list of strings such that each element represents
    a concatenation of an element from stringlist1 and an element
    from stringlist2. The returned list contains all possible
    concatenations between stringlist1 and stringlist2.
    """
    if len(stringlist1) == 0:
        return stringlist2
    else:
        output_list = []
        for string1 in stringlist1:
            for string2 in stringlist2:
                output_list.append(string1 + string2)
        return output_list

def cartesianProductPrinter(string):
    print " ".join([i for i in cartesianProduct(string) if i != ""])

class UnescapedBackslashTerminatedStringException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
if __name__ == "__main__":
    cartesian()
