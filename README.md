# ISPLconverter
A tool for converting game graphs from one the format created by the MKBSC-tool by Helmer and Nylen, found at https://github.com/helmernylen/mkbsc, into .ISPL syntax.

##`Limitations`
The tool converts the game and assumes that the winning condition is always when all agents enter the 'win' state. To expand upon this and check for more complex conditions than if the agents have won, modifications to rows 140-155 are needed.

##`Requirements`
The tool uses a the parts from our strategy synthesiser tool found at https://github.com/VAkerJ/strategysynthesiser_2 to parse data, and therefore, placing these tools in the same folder is required for the program to run.

Another requirement is regarding the filemanagement, as the tool expects there to be a directory called 'pictures' in the same folder as the tool, and that this directory contains subfolder named after each game to be converted.

##`Tutorial`
To run the program, first download the tool found at https://github.com/VAkerJ/strategysynthesiser_2 and place it in the same folder as ISPLconverter.py. Then call the ISPLconverter.py script with the input parameter being the name of the subfolder containing the game to be converted.

As in, if the folder system has a path called 'pictures\chemical\' which contains the game after it's been expanded by Helmer and Nylens tool. The ISPLconverter.py function makeISPL() should be called as makeISPL('chemical')
