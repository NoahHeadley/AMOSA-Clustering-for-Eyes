import os
import sys

src = './'

total_a = 0
total_b = 0
total_l = 0
total_w = 0
for cluster_num in range(1, sys.maxsize):
    source = f"./{cluster_num}/"
    total = 0
    af = 0
    am = 0
    bf = 0
    bm = 0
    lf = 0
    lm = 0
    wf = 0
    wm = 0
    if not os.path.exists(f'./{source}/'):
        break
    files = os.listdir(source)
    for file in files:
        # hardcoding this for now
        demographic_info = file[4:6]
        if demographic_info == "AF":
            af += 1

        elif demographic_info == "AM":
            am += 1

        elif demographic_info == "BF":
            bf += 1

        elif demographic_info == "BM":
            bm += 1

        elif demographic_info == "LF":
            lf += 1

        elif demographic_info == "LM":
            lm += 1

        elif demographic_info == "WF":
            wf += 1

        elif demographic_info == "WM":
            wm += 1

        else:
            print(
                "error: unexpected entry. Please format your image as such '****AF...' where the first letter is [A,B,L,W] and the second is [F,M]")
            exit

        total += 1
    print(f'Cluster {cluster_num}:\n')
    print(f'Total Eyes:\t{total}')
    print(
        f'Asian Female:\t{af}\tAsian Male:\t{am}\tTotal Asians:\t\t{af + am}')
    print(
        f'Black Female:\t{bf}\tBlack Male:\t{bm}\tTotal Blacks:\t\t{bf + bm}')
    print(
        f"Latino Female:\t{lf}\tLatino Male:\t{lm}\tTotal Latinos:\t{lf + lm}")
    print(f'White Female:\t{wf}\tWhite Male:\t{wm}\tTotal Whites:\t{wf + wm}')
    print(
        f'Total Females:\t{af+bf+lf+wf}\tTotal Males:\t{am+bm+lm+wm}\tTotal Eyes:\t\t{total}\n')
    total_a += af+am
    total_b += bf + bm
    total_l += lf + lm
    total_w += wf + wm

print(f'Total Asians: {total_a}')
print(f'Total Blacks: {total_b}')
print(f'Total Latinos: {total_l}')
print(f'Total Whites: {total_w}')
