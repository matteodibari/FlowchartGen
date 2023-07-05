# FlowchartGen

YAML-based programming language developed and designed in collaboration with the research laboratories of the University of Modena and Reggio Emilia with the aim of simplifying the operation of creating flowcharts.

The entire project is based on three separate files: 
- The **console.yaml** file is the user interface for writing code. 
- The **parser.py** file allows the code to be converted to the DOT language.
- Finally, the **output.dot** file contains the resulting DOT code.

The language is entirely based on YAML. Accordingly, it is possible to recognize
general features such as the presence of dictionaries with key-object pairs and indentation
which defines to which dictionary a given pair will belong. Within the project this
feature has been used to define *typeInstruction-command* pairs that allow
to create combinations of instructions and constructs of any type. 
It is possible to write comment using `#` at the beginning of the line.
The possibility of defining two separate graphs is not present.
separated within the same code. All graphs start with the BEGIN block and end with the
END block. To write multiline strings, the character `|` is used. To write comments
the character `#` should be inserted. Writing two instructions one after the other corresponds to linking
graphically two blocks

## Instruction command
The instruction command corresponds to the definition of a process node within the final graph. It is identified by the keyword `do` and as value it is given the label of the node.

```YAML
- do: A = 3
- do: B = 4
- do: C = 4
```

## IO command
The Input/Output command corresponds to the definition of an Input/Output node within the
graph (parallelogram). It is identified by the keyword `IO` and as a value requires the label
of the node.

```YAML
- IO: Insert A
- IO: Return B
```

## If-else construct
The construct is initialized with the keyword `if` to which is assigned as a value the entire set of
instructions to be executed in the case of a positive test. The first instruction must necessarily be
identified by the keyword `test` and has as its value the label to be assigned to the graph node, that is, the 
condition to be tested.
It is possible to add a set of instructions to be executed in the case of a negative test by entering them
as the value field of the keyword `else`, to be inserted at the same level as if. In the `else` it is not
required the test field.
Two arrows will come out of the conditional block, one with label "True", which follows the path in
case of a true condition, one labeled "False", which follows the instruction path (if any) in
case of a false condition.

```YAML
− if: 
    − test: A < 4
    − do: A += 1
− else:
    − do: A −= 1
```

## Loop construct
This construct is initialized with the keyword `loop` and corresponds to the creation of a loop
within the resulting graph. The keyword has to be followed, as seen for the if,  with all the
instructions to be executed within the loop, with the exception of the first instruction, which must
necessarily be identified by the keyword `test` and must contain as its value the label of the
conditional block of the loop, that is, the condition for which the logical process remains within the loop.

```YAML
- do: A = 0
- do: B = 10
- loop:
    - test: A < 10
    - do: A++
    - do: B--
```

## Functions
There is also the possibility of graphically creating flowcharts rappresenting functions, thus with input parameters and return values. To do this it is necessary to
use the keyword `func` and assign as its value a list of three specific elements:
- The first element of this list must be identified with the keyword `args` and must have
as its value the function arguments (which will be drawn as the label of the arrow
entering the BEGIN block).
- The second element must be identified with the keyword `body` and must contain all the
operations performed internally by the function.
- The last element must be identified with the keyword `ret` and must have as its value
the elements to be returned by the function in the output (drawn as the label of the arrow
coming out of the END block).

```YAML
- func:
    - args: [a, b]
    - body:
        - do: a = b + 1
        - do: c = a + b
    - ret: [c]
```
