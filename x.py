import enchant

dictionary = enchant.Dict ('en_US')
#dictionary = enchant.Dict ('en_GB')
must = 'sai'
may = 'qopdhjzxvbnm'
letters = must + may
for a in letters:
    if a in '': continue
    for b in letters:
        if b not in 'a': continue
        for c in letters:
            if c not in 's': continue
            for d in letters:
                if d in '': continue
                for e in letters:
                    if e  in '': continue
                    candidate = f"{a}{b}{c}{d}{e}"
                    if dictionary.check (candidate):
                        truth =[c in candidate for c in must]
                        if all (truth):
                            #print (truth, candidate)
                            print (candidate)

