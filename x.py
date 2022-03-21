import enchant

dictionary = enchant.Dict ('en_US')
#dictionary = enchant.Dict ('en_GB')
must = 'ater'
may = 'qopdhjzxvbnm'
letters = must + may
for a in letters:
    if a in 'r': continue
    for b in letters:
        if b in 'a': continue
        for c in letters:
            if c in '': continue
            for d in letters:
                if d in 'te': continue
                for e in letters:
                    if e  in 'r': continue
                    candidate = f"{a}{b}{c}{d}{e}"
                    if dictionary.check (candidate):
                        truth =[c in candidate for c in must]
                        if all (truth):
                            #print (truth, candidate)
                            print (candidate)


