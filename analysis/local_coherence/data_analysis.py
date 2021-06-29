import matplotlib.pyplot as plt
import numpy as np

AMBIGUOUS = ["brought", "painted", "sent", "allowed", "told", "offered", "taught", "served", "dyed", "cut", "rented", "nabbed"
             "recited", "brought", "tossed", "knitted", "mailed", "saved", "planted"]

UNAMBIGUOUS = ["chosen", "drawn", "flown", "forbidden", "forgiven", "given", "hidden", "shown", "stolen", "sung", "taken", "sewn"
               "thrown", "woven", "written", "given", "grown"]

UNAMBIG_DICT = {}
AMBIG_DICT = {}

OVERALL_DICT = {}
i = 0
for line in open("train_parses.txt", "r"):
    if i % 1000 == 0:
        print(i)
    i += 1
    line = [word.strip() for word in line.split()]
    curr_open_nt = ["NULL"]
    for word in line:
        if "(" in word:
            curr_open_nt.append(word.replace("(", ""))
        else:
            subtract = word.count(")")
            word = word.replace(")", "")
            if curr_open_nt[-1] == "VBN" and "(" not in word:
                if word not in OVERALL_DICT:
                    OVERALL_DICT[word] = 0
                OVERALL_DICT[word] += 1
            while subtract:
                del curr_open_nt[-1]
                subtract -= 1


    #
    # if any(unambig in line or unambig+")" in line for unambig in UNAMBIGUOUS):
    #     curr_open_nt = ["NULL"]
    #     for word in line:
    #         if "(" in word:
    #             curr_open_nt.append(word.replace("(", ""))
    #         else:
    #             subtract = ")" in word
    #             word = word.replace(")", "")
    #             if word in UNAMBIGUOUS:
    #                 if curr_open_nt[-1] not in UNAMBIG_DICT:
    #                     UNAMBIG_DICT[curr_open_nt[-1]] = 0
    #                 UNAMBIG_DICT[curr_open_nt[-1]] +=1
    #             if subtract:
    #                 del curr_open_nt[-1]
    # if any(ambig in line or ambig + ")" in line for ambig in AMBIGUOUS):
    #     curr_open_nt = ["NULL"]
    #     for word in line:
    #         if "(" in word:
    #             curr_open_nt.append(word.replace("(", ""))
    #         else:
    #             subtract = ")" in word
    #             word = word.replace(")", "")
    #             if word in AMBIGUOUS:
    #                 if curr_open_nt[-1] not in AMBIG_DICT:
    #                     AMBIG_DICT[curr_open_nt[-1]] = 0
    #                 AMBIG_DICT[curr_open_nt[-1]] += 1
    #             if subtract:
    #                 del curr_open_nt[-1]


# print(f"unambiguous: {UNAMBIG_DICT['VBN']/sum(UNAMBIG_DICT.values())}")
# print(f"ambiguous: {AMBIG_DICT['VBN']/sum(AMBIG_DICT.values())}")
# print(f"P(v_a|VBN) = {OVERALL_DICT['ambig']/sum(OVERALL_DICT.values())}")
# print(f"P(v_u|VBN) = {OVERALL_DICT['unambig']/sum(OVERALL_DICT.values())}")
ambig_avg = np.mean(np.asarray([OVERALL_DICT[word] for word in AMBIGUOUS if word in OVERALL_DICT]))/sum(OVERALL_DICT.values())
unambig_avg = np.mean(np.asarray([OVERALL_DICT[word] for word in UNAMBIGUOUS if word in OVERALL_DICT]))/sum(OVERALL_DICT.values())
print(f"P(v_a|VBN) = {ambig_avg}")
print(f"P(v_u|VBN) = {unambig_avg}")

UNAMBIG_DICT = {word :OVERALL_DICT[word] for word in UNAMBIGUOUS if word in OVERALL_DICT}
AMBIG_DICT = {word : OVERALL_DICT[word] for word in AMBIGUOUS if word in OVERALL_DICT}

fig, ax = plt.subplots(1,2)
wp = {'linewidth': 0.5, 'edgecolor': "black"}
ax[0].pie(UNAMBIG_DICT.values(), labels=UNAMBIG_DICT.keys(), startangle=90, autopct='%1.1f%%', wedgeprops=wp)
ax[0].set_title("unambiguous distribution")
ax[1].pie(AMBIG_DICT.values(), labels=AMBIG_DICT.keys(), startangle=90, autopct='%1.1f%%', wedgeprops=wp)
ax[1].set_title("ambiguous distribution")
plt.show()

