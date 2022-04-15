import enchant
# seem to need this, or the default values change between calls to the function (!!)

from copy import deepcopy

dictionary = enchant.Dict ('en_US')
#dictionary = enchant.Dict ('en_GB')
must = 'ah'
may = 'qwrypfjkzxv'
may = 'qwypfjzxv'
ys={1: '', 2: '', 3: '', 4: '', 5:''}
ns={1: '', 2: '', 3: '', 4: '', 5:''}

def candidates (must, may, sure_y={1: '', 2: '', 3: '', 4: '', 5:''}, sure_n={1: '', 2: '', 3: '', 4: '', 5:''}):
    sure_yes = deepcopy (sure_y)
    sure_no   = deepcopy (sure_n)
    #print ("inbound", must, may, sure_yes, sure_no)
    letters = must + may
    for k in range(1,6):
        #breakpoint()
        if sure_yes[k] == '':
            sure_yes[k] = letters
    candidates = []
    #print ('in candidates', must, may, sure_yes, sure_no)
    #breakpoint()
    for a in letters:
        #if a  in '': continue
        if (a in sure_no[1]) or (a not in sure_yes[1]): continue
        for b in letters:
            #print ("b", a,b, b in sure_no[2], b not in sure_yes[2], f"sn {sure_no[2]}, sy {sure_yes[2]}") #if b  in '': continue
            if (b in sure_no[2]) or (b not in sure_yes[2]): continue
            for c in letters:
                #if c  in  '': continue
                #print ("c", a,b, c) #if b  in '': continue
                if (c in sure_no[3]) or (c not in sure_yes[3]): continue
                for d in letters:
                    #print ("d", a,b,c,d, d in sure_no[4], d not in sure_yes[4], sure_yes[4]) #if d  in '': continue
                    if (d in sure_no[4]) or (d not in sure_yes[4]): continue
                    for e in letters:
                        #print ("e", a,b,c,d, e, e in sure_no[5], e not in sure_yes[5], f"y {sure_yes[5]} n: {sure_no[5]}") #if d  in '': continue
                        #if e  in '': continue
                        if (e in sure_no[5]) or (e not in sure_yes[5]): continue
                        candidate = f"{a}{b}{c}{d}{e}"
                        if dictionary.check (candidate):
                            truth =[c in candidate for c in must]
                            #print ("cand", candidate, truth)
                            if all (truth):
                                #print ("got one", truth, candidate)
                                candidates.append (candidate)
    return candidates

if __name__ == "__main__":
    print (candidates(must, may, sure_yes={1:'h',2:'',3:'',4:'',5:''}))
    

