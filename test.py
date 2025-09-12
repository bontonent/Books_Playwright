# anytime I can delete with my friends others process
kol  = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# ok
len_kol = len(kol)
for i,ko in enumerate(reversed(kol)):

    # first, give and delete, if don't get all data, recovery

    kol.pop(len_kol - i - 1)

    if i > 0:
        break

print(kol)