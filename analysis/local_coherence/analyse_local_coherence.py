import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

WORDS = ["brought", "chosen", "brought", "chosen", "painted", "drawn", "painted", "drawn", "sent", "flown", "sent", "flown",
         "allowed", "forbidden", "allowed", "forbidden", "told", "forgiven", "told", "forgiven",
         "offered", "given", "offered", "given", "taught", "given", "taught", "given", "served", "given",
         "served", "given", "dyed", "hidden", "dyed", "hidden", "cut", "UNK-LC", "cut", "UNK-LC", "knitted", "sewn",
         "knitted", "sewn", "rented", "shown", "rented", "shown", "nabbed", "stolen", "nabbed", "stolen",
         "recited", "sung", "recited", "sung", "brought", "taken", "brought", "taken", "tossed", "thrown",
         "tossed", "thrown", "knitted", "woven", "knitted", "woven", "mailed", "written", "mailed", "written",
         "saved", "given", "saved", "given", "planted", "grown", "planted", "grown"]

TARGET_SUPRISAL_DICT = {}

for i in range(10):
    df = pd.read_csv(f"100-lc-{i+1}.txt", sep="\t")
    for sent_num in set(df["sentence_id"]):
        sentence = df[(df["sentence_id"] == sent_num)]
        words = list(sentence["token"])
        surprisals = list(sentence["surprisal"])
        index_zero = words.index(WORDS[sent_num-1])
        # start at 4 to the left of the target
        start_index = index_zero-4
        # if there was intervening material such as "who was", remove it
        if (sent_num-3) %4 == 0 or sent_num%4 == 0:
            start_index = start_index-2
        target_surprisals = surprisals[start_index: start_index+4] + surprisals[index_zero: index_zero+5]
        if sent_num not in TARGET_SUPRISAL_DICT:
            TARGET_SUPRISAL_DICT[sent_num] = []
        TARGET_SUPRISAL_DICT[sent_num].append(target_surprisals)

print(TARGET_SUPRISAL_DICT)

A_R = {}
A_U = {}
U_R = {}
U_U = {}
for key in TARGET_SUPRISAL_DICT:
    means = [np.mean(np.asarray([tar[i] for tar in TARGET_SUPRISAL_DICT[key]])) for i in range(9)]
    if key%4 == 0:
        U_U[key] = means
    elif (key-3)%4 ==0:
        U_R[key] = means
    elif (key-2)%4 == 0:
        A_U[key] = means
    else:
        A_R[key] = means

PLOT_LABELS = ["A/R",  "A/U", "U/R", "U/U"]
X = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
xlabels = ["-4\nsmiled","-3\nat", "-2\nthe", "-1\nplayer", "0\ntossed/\nthrown", "1\na", "2\nfrisbee", "3\nby", "4\nthe"]
fig, ax = plt.subplots()
plt.title(f"Local Coherence Effects for Particle Filter, k=100")
idx = 0
for key in [A_R, A_U, U_R, U_U]:
    print(key.values())
    means = [np.mean(np.asarray([x[i] for x in key.values()])) for i in range(9)]
    print("MEANS", means)
    stderrs = [np.std(np.asarray([x[i] for x in key.values()]))/np.sqrt(20) for i in range(9)]
    ax.errorbar(X, means, yerr=stderrs, label=PLOT_LABELS[idx])
    idx += 1
plt.ylabel("mean surprisal")
plt.xlabel("position in sentence")
ax.set_xticks(X)
ax.set_xticklabels(xlabels)
plt.legend()
plt.show()
