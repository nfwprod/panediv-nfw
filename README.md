# panediv_nfw
Generate tmux layout string from simple format.

# Install
```
$ pip3 install panediv-nfw

$ export PATH=$PATH:~/.local/bin/

```

# PaneDiv
Automate tmux layout generation tools.
With options, print layout information only.
Without options, start tmux with the layout.
Run this script on the outside of tmux.

## Usage

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

## Examples
Open tmux with complex layout from simple string.

![example01](https://user-images.githubusercontent.com/78602998/147897737-4397d457-8600-4dd9-a2fa-27623487697a.gif)

### Simple 3 rows
- panediv '[,,]'
- panediv '[3]'

### Simple 3 columns
- panediv '{,,}'
- panediv '{3}'

### Simple 3 rows with commands
- panediv '[/usr/games/sl,"figlet \\"pane 2\\"",]'

### Specify size, 10 lines, 15 lines, left
- panediv '[(,10),(,15),]'

### Specify size, 20 percent, 30 percent, left
- panediv '[(,20%),(,30%),]'

### Specify command and size
- panediv '[(/usr/games/sl,20%),("figlet \\"pane 2\\"",10),]'

### Complex layout
- panediv '{[{,[2]},,{[2],}],,[{[2],},,{,[2]}]}'
- panediv '{([4], 70%),,}'

### Export TmuxInator configuration.
- panediv -i /tmp/layout '{/usr/games/sl, [1,"figlet \\"pane 3\\"",2],}' && tmuxinator start -p /tmp/layout

# pdv, pdc
Simply split current pane evenly.

## Usage

```
$ pdv.py
usage: pdv.py [-h] [--vertical] num

Split pane evenly.

positional arguments:
  num             Divide pane into num. default: horiszontally.

optional arguments:
  -h, --help      show this help message and exit
  --vertical, -v  Divide vertically.

```

```
$ pdc -h
usage: pdc.py [-h] [--file FILE] [--vertical] [--instant] [commands [commands ...]]

Split pane and run commands. Input commands as args, filename(-f) or from pipe.

positional arguments:
  commands              Commands.

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Commands file or \n separated stdin
  --vertical, -v        Divide vertically.
  --instant, -i         Kill the pane when the command finished.

```

## Examples

### Split current pane horizontally
- pdv 3

### Split current pane vertically
- pdv -v 3

### Split current pane horizontally and run commands
- pdc "echo 1" "echo 2"
- echo "echo 1\necho 2" | pdc
- for i in {1..2}; do echo "echo ${i}"; done | pdc 'echo 1' 'echo 2'
- echo "echo 1\necho 2" > ./commands.txt && pdc -f ./commands.txt

### Split current pane vertically
- pdc -v "echo 1" "echo 2"

### Split current but close then when command done.
- pdc -i "echo 1" "echo 2; sleep 3"
