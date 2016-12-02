###This project involves writing a program (grammar.py) that parses, using _recursive descent_, a GUI definition language defined below and generates the GUI that it defines. The Backus–Naur form (BNF) grammar for this language is defined below:

>    gui ::=
>        Window STRING '(' NUMBER ',' NUMBER ')' layout widgets End '.'
>
>    layout ::=
>        Layout layout_type ':'
>
>    layout_type ::=
>        Flow |
>        Grid '(' NUMBER ',' NUMBER [',' NUMBER ',' NUMBER] ')'
>
>    widgets ::=
>        widget widgets |
>        widget
>
>    widget ::=
>        Button STRING ';' |
>        Group radio_buttons End ';' |
>        Label STRING ';' |
>        Panel layout widgets End ';' |
>        Textfield NUMBER ';'
>
>    radio_buttons ::=
>        radio_button radio_buttons |
>        radio_button
>
>    radio_button ::=
>        Radio STRING ';'

####Below is an explanation of the meaning of some of the symbols in the above productions that should help you understand the actions that are to be performed when each of the productions is parsed:

>In the window production the string is name that is to appear in the top border of the window and the two numbers are the width and height of the window
>In the production for layout_type that define the grid layout, the first two numbers represent the number of rows and columns, and the optional next two the horizontal and vertical gaps
>In the production for widget that defines a button, the string is the name of the button
>In the production for widget that defines a label, the string is text that is to be placed in the label
>In the production for widget that defines a text field, the number is the width of the text field
>In the production for radio_button, the string is the label of the button

###This project also includes a program (calculator.py) that reads a grammar input file (calculator.txt) and generates a working calculator application.