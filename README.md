This project consists of a python script to create anki cards based on the contents of a text file. The file must be formated like this:<br>
Deck 1 name<br>
Front side - back side //will be added to deck 1<br>
Front side - back side //will be added to deck 1<br>
Deck 2 name<br>
Front side - back side //will be added to deck 2<br>
Front side - back side //will be added to deck 2<br>

The script also attaches a sound file with the pronunciation for the text on the front side.

You need to configure valid deck names, which can be currently done inside the python script. If the script runs with no errors, it also wipes the file and writes all the decks' names.

You can run the python script directly if Anki is open. You can use the bash script to open Anki automatically, but it requires some configuration (namely, the path for the files).

I personally use a tmux remap to run the bash script in a new window (using tmux neww bash - c "path/to/script"), so I can execute it directly from neovim after editing the file.
