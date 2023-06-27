# FlowchartGen

YAML-based programming language developed and designed in collaboration with the research laboratories of the University of Modena and Reggio Emilia with the aim of simplifying the operation of creating flowcharts.

The entire project is based on three separate files: 
- The `console.yaml` file is the user interface for writing code. 
- The `parser.py` file allows the code to be converted to the DOT language.
- Finally, the `output.dot` file contains the resulting DOT code.

The language is entirely based on YAML. Accordingly, we recognize
general features such as the presence of dictionaries with key-object pairs and indentation
which defines to which dictionary a given pair will belong. Within the project this
feature has been used to define typeInstruction-command pairs that allow
to create combinations of instructions and constructs of any type. 
It is possible to write comment using `#` at the beginning of the line.
The possibility of defining two separate graphs is not present.
separated within the same code. All graphs start with the BEGIN block and end with the
END block. To write multiline strings, the character `|` is used. To write comments
the character `#` should be inserted. Writing two instructions one after the other corresponds to linking
graphically two blocks

## If-else construct
The construct is initialized with the keyword `if` to which is assigned as a value the entire set of
instructions to be executed in the case of a positive test. The first instruction must necessarily be
identified by the keyword `test` and has as its value the label to be assigned to the graph node, that is, the 
condition to be tested.
It is possible to add a set of instructions to be executed in the case of a negative test by entering them
as the value field of the keyword `else`, to be inserted at the same level as if. In the `else` it is not
required the test field.
Two arrows will come out of the conditional block, one with label `True`, which follows the path in
case of a true condition, one labeled `False`, which follows the instruction path (if any) in
case of a false condition.
