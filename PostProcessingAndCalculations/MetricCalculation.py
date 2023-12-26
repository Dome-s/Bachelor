true_positive = 0
false_positive = 0
true_negative = 0
false_negative = 0

def precision(true_positive, false_negative):
    if(true_positive + false_negative <= 0):
        return 0
    return true_positive/(true_positive+false_negative)

def recall(true_positive, false_positives):
    if(true_positive + false_positives <= 0):
        return 0
    return true_positive/(true_positive+false_positives)

def f1(true_positive,false_negative, false_positives):
    if(recall(true_positive,false_positives)+precision(true_positive,false_negative) <= 0):
       return 0
    return 2*recall(true_positive,false_positives)*precision(true_positive,false_negative) / (recall(true_positive,false_positives)+precision(true_positive,false_negative))

S_l = 0  #elements in smaller schema
S_L = 0  # elements in larger schema
E = 0 # matches in ground truth
M = 0 # discovered Matches
R = 0 # number of correctly discovered Matches

def nui(S_l,S_L,E,M,R):
    effort_prec = M
    if(M == 0):
        return S_l * S_L
    else:
        freq = 1
        if(E-R > 0):
            freq = (S_l - R) / (E - R)

        effort_rec = 0
        for i in range(1,S_l-R,1):
            effort_rec += S_L-R-(i/freq)-((M-R)/(S_l-R))

        return effort_prec + effort_rec

def pme(S_l,S_L,E,M,R):
    return nui(S_l,S_L,E,M,R)/(S_L * S_l)

def hsr(S_l,S_L,E,M,R):
    return 1 - nui(S_l,S_L,E,M,R)/(S_L * S_l)