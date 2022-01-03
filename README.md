# panediv_nfw
Generate tmux layout string from simple format.

# Install
```
$ pip3 install panediv-nfw
$ sudo ln -s ~/.local/bin/panediv /usr/local/bin

```

# Usage
```
$ panediv -h
usage: panediv [-h] [--tmuxinator] [--show_layout] [--show_commands] [--show_matrix] layout

Generate layout string from simple format.

positional arguments:
  layout               Layout string, ex.) {,}. Without other options, start tmux.

optional arguments:
  -h, --help           show this help message and exit
  --tmuxinator, -i     Export tmuxnator configuration.
  --show_layout, -l    Print layout string.
  --show_commands, -c  Print command list.
  --show_matrix, -m    Print pane number matrix.

```

# Examples
Open tmux with complex layout from simple string.

![example01](https://user-images.githubusercontent.com/78602998/147897737-4397d457-8600-4dd9-a2fa-27623487697a.gif)

## Simple 3 rows
- panediv '[,,]'
- panediv '[3]'

## Simple 3 columns
- panediv '{,,}'
- panediv '{3}'

## Simple 3 rows with commands
- panediv '[/usr/games/sl,"figlet \\"pane 2\\"",]'

## Specify size, 10 lines, 15 lines, left
- panediv '[(,10),(,15),]'

## Specify size, 20 percent, 30 percent, left
- panediv '[(,20%),(,30%),]'

## Specify command and size
- panediv '[(/usr/games/sl,20%),("figlet \\"pane 2\\"",10),]'

## Complex layout
- panediv '{[{,[2]},,{[2],}],,[{[2],},,{,[2]}]}'

## Export TmuxInator configuration.
- panediv -i /tmp/layout '{/usr/games/sl, [1,"figlet \\"pane 3\\"",2],}' && tmuxinator start -p /tmp/layout
