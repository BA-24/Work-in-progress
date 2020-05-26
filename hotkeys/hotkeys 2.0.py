print('starting application...')

#gets detection keys
f = open('hotkeys.txt', 'r')
keys = []
for r in f:    
    if r != '\n':
        keys = keys + [r.split()[0]]
f.close()

#gets messages
f = open('hotkeys.txt', 'r')
keys = []
for r in f:    
    if r != '\n':
        keys = keys + [r.replace( ((r.split()[0]) + ' '), '', 1).replace('\n', '', 1)]
f.close()

