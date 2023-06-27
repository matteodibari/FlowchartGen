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
