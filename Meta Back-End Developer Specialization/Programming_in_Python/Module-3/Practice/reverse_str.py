# slice
# str[start:stop:step]

trial = "reversal"
new_trial = trial[::-1]

print(trial)
print(new_trial)


# recursion

def str_reverse(str) :
    if len(str) == 0 :
        return str
    else :
        return str_reverse(str[1:])+str[0]
    
print("Using recursion - " + str_reverse(trial))