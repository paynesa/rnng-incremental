"""Analyses the distribution of ambiguous and nonambiguous VBNs and compares
P(v_a| VBN) with P(v_u | VBN)"""
import matplotlib.pyplot as plt
import numpy as np

# lists of ambiguous and unambiguous verb forms from Experiment 1 from the Tabor et al 2004
AMBIGUOUS = ["brought", "painted", "sent", "allowed", "told", "offered", "taught", "served", "dyed", "cut", "rented", "nabbed"
             "recited", "brought", "tossed", "knitted", "mailed", "saved", "planted"]

UNAMBIGUOUS = ["chosen", "drawn", "flown", "forbidden", "forgiven", "given", "hidden", "shown", "stolen", "sung", "taken", "sewn"
               "thrown", "woven", "written", "given", "grown"]

# dictionaries to store the NT distribution for these verbs
UNAMBIG_DICT = {}
AMBIG_DICT = {}
# dictionary to store the distribution of words appearing in the VBN position
OVERALL_DICT = {}
i = 0
# iterate through the gold parses from the training file
for line in open("train_parses_ptb.txt", "r"):
    if i % 1000 == 0:
        print(i)
    i += 1
    line = [word.strip() for word in line.split()]
    # initialize a stack on which we'll store the current open NTs
    curr_open_nt = ["NULL"]
    for word in line:
        # open a new NT if needed
        if "(" in word:
            curr_open_nt.append(word.replace("(", ""))
        else:
            # keep track of how many NTs we need to close
            subtract = word.count(")")
            word = word.replace(")", "")
            # if the current open NT is a VBN, then update the word distribution
            if curr_open_nt[-1] == "VBN" and "(" not in word:
                if word not in OVERALL_DICT:
                    OVERALL_DICT[word] = 0
                OVERALL_DICT[word] += 1
            # if the word is ambiguous, then update the NT distribution
            if word in AMBIGUOUS:
                if curr_open_nt[-1] not in AMBIG_DICT:
                    AMBIG_DICT[curr_open_nt[-1]] = 0
                AMBIG_DICT[curr_open_nt[-1]] += 1
            # if the word in unambiguous, then update the NT distribution
            if word in UNAMBIGUOUS:
                if curr_open_nt[-1] not in UNAMBIG_DICT:
                    UNAMBIG_DICT[curr_open_nt[-1]] = 0
                UNAMBIG_DICT[curr_open_nt[-1]] += 1
            # pop all the closed NT's off the stack
            while subtract:
                del curr_open_nt[-1]
                subtract -= 1

# calculate the average probility of a single ambiguous / unambiguous verb, as well as the probability of each of the classes
ambig_avg = np.mean(np.asarray([OVERALL_DICT[word] for word in AMBIGUOUS if word in OVERALL_DICT]))/sum(OVERALL_DICT.values())
unambig_avg = np.mean(np.asarray([OVERALL_DICT[word] for word in UNAMBIGUOUS if word in OVERALL_DICT]))/sum(OVERALL_DICT.values())
ambig_sum = np.sum(np.asarray([OVERALL_DICT[word] for word in AMBIGUOUS if word in OVERALL_DICT]))/sum(OVERALL_DICT.values())
unambig_sum = np.sum(np.asarray([OVERALL_DICT[word] for word in UNAMBIGUOUS if word in OVERALL_DICT]))/sum(OVERALL_DICT.values())
print(f"P(v_a|VBN) = {ambig_avg} on average, while class probability is {ambig_sum}")
print(f"P(v_u|VBN) = {unambig_avg} on average, while class probability is {unambig_sum}")

# plot the distribution of NTs for the ambiguous and unambiguous verbs
fig, ax = plt.subplots(1,2)
wp = {'linewidth': 0.5, 'edgecolor': "black"}
ax[0].pie(UNAMBIG_DICT.values(), labels=UNAMBIG_DICT.keys(), startangle=90, autopct='%1.1f%%', wedgeprops=wp)
ax[0].set_title("unambiguous distribution")
ax[1].pie(AMBIG_DICT.values(), labels=AMBIG_DICT.keys(), startangle=90, autopct='%1.1f%%', wedgeprops=wp)
ax[1].set_title("ambiguous distribution")
plt.show()

# update the dictionaries to store the lexical distribution for ambiguous and nonambiguous verbs
UNAMBIG_DICT = {word :OVERALL_DICT[word] for word in UNAMBIGUOUS if word in OVERALL_DICT}
AMBIG_DICT = {word : OVERALL_DICT[word] for word in AMBIGUOUS if word in OVERALL_DICT}

# plot the distribution of words for each of the two cases 
fig, ax = plt.subplots(1,2)
wp = {'linewidth': 0.5, 'edgecolor': "black"}
ax[0].pie(UNAMBIG_DICT.values(), labels=UNAMBIG_DICT.keys(), startangle=90, autopct='%1.1f%%', wedgeprops=wp)
ax[0].set_title("unambiguous distribution")
ax[1].pie(AMBIG_DICT.values(), labels=AMBIG_DICT.keys(), startangle=90, autopct='%1.1f%%', wedgeprops=wp)
ax[1].set_title("ambiguous distribution")
plt.show()


