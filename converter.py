import yaml
import gvgen
import numpy as np

x_pos = 0
y_pos = 0
lower_y = 0
if_heights = [list(), 0]
#if_heights[0][] = array of lenghts of the true branch (LIFO queue)
#if_heights[1] = lenght of the false branch

previous_block = 0
fork_block = 0
yes_flag = 0
no_flag = 0
if_flag = 0
close_if = 0    

blocks_matrix = np.zeros([255, 255], dtype=dict)

def block_height_from_string(string):
    numbers = string.split(',')
    second_number = int(numbers[1][:-1])  
    return second_number
    

def slide_columns(g):
    global blocks_matrix
    
    x = len(blocks_matrix) - 1      #starting from the last column
    while x > x_pos - 1:            #stopping on the current column
        for y in range(255):
            b = blocks_matrix[x][y]
            if b != 0:
                g.propertyAppend(b, 'pos', position(x + 2, - y))
            blocks_matrix[x][y] = 0
            if x + 2 < 255:
                blocks_matrix[x + 2][y] = b
        x -= 2
    

def position(x_pos, y_pos):
    return str(x_pos) + ',' + str(y_pos) + '!'

def add_block(g, label, style):
    global x_pos, y_pos, lower_y 
    global blocks_matrix
    b = g.newItem(label)
    g.styleApply(style, b)
    g.propertyAppend(b, 'pos', position(x_pos, y_pos))
    if lower_y > y_pos: lower_y = y_pos
    
    if blocks_matrix[abs(x_pos)][abs(y_pos)] != 0: 
        slide_columns(g)
    blocks_matrix[abs(x_pos)][abs(y_pos)] = b

    y_pos = y_pos - 1
    return b

def add_link(g, block1, block2):
    global yes_flag
    global no_flag
    l = g.newLink(block1, block2)
    if yes_flag:
        g.propertyAppend(l, 'taillabel', 'True')
        yes_flag = 0
    if no_flag:
        g.propertyAppend(l, 'taillabel', 'False')
        no_flag = 0
    return l

def do_close_if(g, last_true_block =  None):
    global previous_block
    global fork_block
    global if_flag
    global x_pos, y_pos, if_heights

    y = if_heights[0].pop()

    if if_heights[1] > y:
        y_pos = y_pos - if_heights[1] + 1
    else:
        y_pos = y_pos - y + 1

    block = add_block(g, '', 'point')  

    if if_heights[1] == 0:
        l = add_link(g, fork_block, block)
        g.styleApply('line', l)  

    l = add_link(g, previous_block, block)

    g.styleApply('line', l)
    previous_block = block

def converter_rec(key, values):
    global previous_block, fork_block
    global yes_flag
    global no_flag
    global if_flag
    global close_if
    global x_pos, y_pos, if_heights

    while_block = None
    label = None

    match key:
            
        case 'do':
            if close_if == 1:
                do_close_if(g)
                close_if = 0
            if type(values) == list:
                for label in values:
                    block = add_block(g, label, 'do_style')
                    add_link(g, previous_block, block)
                    previous_block = block
            else:
                block = add_block(g, values, 'do_style')
                add_link(g, previous_block, block)
                previous_block = block

        case 'IO':
            if close_if == 1:
                do_close_if(g)
                close_if = 0
            if type(values) == list:
                str = ""
                for label in values:
                    str = str + label + "\n"            
                block = add_block(g, str, 'IO_style')
                add_link(g, previous_block, block)
                previous_block = block
            else:
                block = add_block(g, values, 'IO_style')
                add_link(g, previous_block, block)
                previous_block = block

        case 'if':
            if close_if == 1:
                do_close_if(g)
                close_if = 0
            try:
                label = values[0]['test']
            except KeyError:
                print("ERROR: missing \'test\' field in the if construct")
                exit(3)
            block = add_block(g, label, 'if_style')
            add_link(g, previous_block, block)
            
            previous_block = block
            fork_block = block
            previous_if_flag = if_flag   
            if_flag = 1  
            yes_flag = 1
            counter = 0

            prev_position = [x_pos, y_pos]
            prev_if_heights = if_heights.copy()
            x_pos += 2
            y_pos += 1  #per partire dallo stesso livello del blocco condizionale

            for item in values:
                counter += 1
                if counter == 1: continue
                key, values = list(item.items())[0]
                converter_rec(key, values)   

            if_heights[0].append(abs(prev_position[1] - y_pos))

            x_pos = prev_position[0] 
            y_pos = prev_position[1]

            fork_block = block
            no_flag = 1
            if_flag = previous_if_flag      
            close_if = 1                    
            
        case 'else':
            if close_if != 1:
                print("ERRORE: else cannot be inserted without an associated if")     
                exit()
            last_true_block = previous_block
            previous_block = fork_block
            previous_if_flag = if_flag
            if_flag = 0
            close_if = 0       

            prev_if_heights = if_heights.copy()
            if_heights[1] = 0
            prev_y  = y_pos

            for item in values:
                key, values = list(item.items())[0]
                converter_rec(key, values)

            if close_if == 1:
                do_close_if(g)
                close_if = 0

            if_heights[1] = abs(prev_y - y_pos) + 1
            y_pos = prev_y
            do_close_if(g, last_true_block)
            if_heights = prev_if_heights.copy()
            
            if_flag = previous_if_flag
            l = add_link(g, last_true_block, previous_block)
            g.styleApply('line', l)
            

        case 'loop':
            if close_if == 1:
                do_close_if(g)
                close_if = 0
            try:
                label = values[0]['test']
            except KeyError:
                print("ERROR: missing \'test\' field in the loop")
                exit(4)
            while_block = add_block(g, label, 'if_style')
            add_link(g, previous_block, while_block)
            
            previous_block = while_block
            yes_flag = 1
            counter = 0
            x_pos += 2
            y_pos += 1  
            for item in values:
                counter += 1
                if counter == 1: continue
                key, values = list(item.items())[0]
                converter_rec(key, values)   
            x_pos -= 2
            if close_if == 1:
                do_close_if(g)
                close_if = 0

            add_link(g, previous_block, while_block)
            previous_block = while_block
            no_flag = 1
    
        case _:
            print('ERROR: unrecognised keyword')
            exit(1)
    return

def converter(code, g):
    global previous_block, close_if
    global x_pos, y_pos

    start = g.newItem('Inizio')
    end = g.newItem('Fine')
    g.styleApply("terminal_style", start)
    g.propertyAppend(start, 'pos', position(x_pos, y_pos))
    y_pos = y_pos - 1
    g.styleApply("terminal_style", end)

    previous_block = start
    for item in code:
        key, values = list(item.items())[0]
        converter_rec(key, values)
    add_link(g, previous_block, end)
    if close_if == 1:
        do_close_if(g)
        close_if = 0

    g.propertyAppend(end, 'pos', position(x_pos, y_pos))
    return       

def converter_function(code, g):
    global previous_block, close_if
    global x_pos, y_pos, lower_y

    pseudostart = g.newItem('')
    g.propertyAppend(pseudostart, 'pos', position(x_pos - 2, y_pos))
    
    start = g.newItem('START')
    g.propertyAppend(start, 'pos', position(x_pos, y_pos))
    y_pos -= 1
    
    end = g.newItem('END')
    pseudoend = g.newItem('')

    g.styleApply("terminal_style", start)
    g.styleApply("terminal_style", end)
    g.styleApply("point", pseudostart)
    g.styleApply("point", pseudoend)

    previous_block = start

    for item in code:    
        key, values = list(item.items())[0]

        match key:
            case 'args':
                args = '[ '
                args += ', '.join(values) 
                args += ' ]'          
                l = g.newLink(pseudostart, start)
                g.propertyAppend(l, "headlabel", args)
            case 'ret':
                ret = '[ '
                ret += ', '.join(values) 
                ret += ' ]'       
                l = g.newLink(end, pseudoend)
                g.propertyAppend(l, "taillabel", ret)
            case 'body':
                for item in values:
                    key, values = list(item.items())[0]
                    converter_rec(key, values)
                if close_if == 1:
                    do_close_if(g)
                    close_if = 0              
            case _:
                print('ERROR: the function is not written correctly')
                exit()

    g.propertyAppend(end, 'pos', position(x_pos, lower_y - 1))
    g.propertyAppend(pseudoend, 'pos', position(x_pos + 2, lower_y - 1))
    
    add_link(g, previous_block, end)
    return 


if __name__ == '__main__':    
    with open("console.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    g = gvgen.GvGen() 
    g.styleAppend("terminal_style","shape","ellipse")         #style for terminal nodes
    g.styleAppend("if_style","shape","diamond")               #style for decision nodes
    g.styleAppend("do_style", "shape", "box")                 #style for instruction nodes
    g.styleAppend("point", "shape", "point")                  #style for the pseudoblock
    g.styleAppend("line", "arrowhead", "none")                #style for the lines without arrows
    g.styleAppend("IO_style", "shape", "parallelogram")       #style for IO nodes
   
    g.setOptions(nodesep=1)
    g.setOptions(ranksep=0.5)
    g.setOptions(splines='ortho')
    g.setOptions(layout='neato')
    g.setOptions(overlap='scalexy')
    
    key, values = list(data[0].items())[0]
    if (key == 'main'):
        converter_function(values, g)
    else:
        converter(data, g)

    f = open("output.dot", "w")
    g.dot(f)
    f.close()