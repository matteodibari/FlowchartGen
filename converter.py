import yaml
import gvgen

previous_block = 0
fork_block = 0
yes_flag = 0
no_flag = 0
if_flag = 0
close_if = 0    

def add_block(g, label, style):
    b = g.newItem(label)
    g.styleApply(style, b)
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

def do_close_if(g):
    global previous_block
    global fork_block
    global if_flag
    block = add_block(g, '', 'point')      
    l = add_link(g, fork_block, block)
    g.styleApply('line', l) 
    l = add_link(g, previous_block, block)
    g.styleApply('line', l)
    previous_block = block

def converter_rec(key, values):
    global previous_block
    global fork_block
    global yes_flag
    global no_flag
    global if_flag
    global close_if

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

            for item in values:
                counter += 1
                if counter == 1: continue
                key, values = list(item.items())[0]
                converter_rec(key, values)   

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
            #resetto l if flag
            previous_if_flag = if_flag
            if_flag = 0
            close_if = 0       

            for item in values:
                key, values = list(item.items())[0]
                converter_rec(key, values)

            
            fork_block = last_true_block
            if_flag = previous_if_flag
            do_close_if(g)
            

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
            for item in values:
                counter += 1
                if counter == 1: continue
                key, values = list(item.items())[0]
                converter_rec(key, values)   

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
    global previous_block

    start = g.newItem('Inizio')
    end = g.newItem('Fine')
    g.styleApply("terminal_style", start)
    g.styleApply("terminal_style", end)

    previous_block = start
    for item in code:
        key, values = list(item.items())[0]
        converter_rec(key, values)
    add_link(g, previous_block, end)
    return       

def converter_function(code, g):
    global previous_block

    start = g.newItem('START')
    end = g.newItem('END')
    pseudostart = g.newItem('')
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
            case _:
                print('ERROR: the function is not written correctly')
                exit()

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
    
    key, values = list(data[0].items())[0]
    if (key == 'main'):
        converter_function(values, g)
    else:
        converter(data, g)

    f = open("output.dot", "w")
    g.dot(f)
    f.close()