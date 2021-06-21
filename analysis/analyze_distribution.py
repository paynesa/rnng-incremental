import json
import numpy as np
import matplotlib.pyplot as plt


META_DATA = []
mvrr_json = json.load(open("mvrr.json"))
for item in mvrr_json["items"]:
    for sub_item in item["conditions"]:
        if sub_item["condition_name"] == "reduced_unambig":
            for region in sub_item["regions"]:
                if region["region_number"] == 5:
                    word = region["content"].split()[-1]
                    if word == "chased":
                        word = "UNK-LC-ed"
                    META_DATA.append(word)
print(META_DATA)

ALL_ACTIONS = ["ITERS", "REDUCE", "SHIFT", "NT(S)", "NT(PP)", "NT(NP)", "NT(PRN)", "NT(VP)", "NT(ADVP)", "NT(SBAR)", "NT(ADJP)", "NT(QP)", "NT(UCP)", "NT(WHNP)", "NT(SINV)", "NT(FRAG)", "NT(NAC)", "NT(WHADVP)", "NT(PRT)", "NT(NX)", "NT(WHPP)", "NT(SQ)", "NT(SBARQ)", "NT(CONJP)", "NT(WHADJP)", "NT(INTJ)", "NT(X)", "NT(RRC)", "NT(LST)" ]

overall_sentences = []
for i in range(10):
    sentences = []
    target_idx = 0
    target_word = META_DATA[target_idx]
    print("PROCESSING FILE", i)
    for line in open(f"k_1/second_reduced_unambig_{i+1}.txt"):
        line = line.strip().split("\t")
        if len(line) > 1:
            word = line[0]
            if word == target_word:
                probabilities = [word.split(":") for word in line[1:]]
                prob_map = {action : 0 for action in ALL_ACTIONS}
                print(prob_map)
                for action, prob in probabilities:
                    prob_map[action] = float(prob)
                sentences.append(prob_map)
                target_idx += 1
                if target_idx < len(META_DATA):
                    target_word = META_DATA[target_idx]
    assert len(sentences) == len(META_DATA)
    overall_sentences.append(sentences)

averaged_lists = []
for i in range(len(META_DATA)):
    #averaged_map = {action : np.mean(np.asarray([overall_sentences[j][i][action]])) for action in ALL_ACTIONS}
    #average = np.mean(curr_list[])
    averaged_map = {action : np.mean(np.asarray([curr_list[i][action] for curr_list in overall_sentences])) for action in ALL_ACTIONS}
    averaged_lists.append(averaged_map)

means = [np.mean(np.asarray([curr[action] for curr in averaged_lists])) for action in ALL_ACTIONS]
stderrs = [np.std(np.asarray([curr[action] for curr in averaged_lists]))/len(averaged_lists) for action in ALL_ACTIONS]

ALL_ACTIONS = [ALL_ACTIONS[i] for i in range(len(ALL_ACTIONS)) if means[i]  > 0.001][1:]

stderrs = [stderrs[i] for i in range(len(stderrs)) if means[i] > 0.001][1:]
means = [mean for mean in means if mean > 0.001][1:]
print(means)
print(stderrs)

fig, ax = plt.subplots()
plt.ylabel("Probability")
plt.xlabel("Next Parse Step")
plt.title("Probability Distribution at Second Parse Action for Reduced Unambiguous")
x = np.arange(len(ALL_ACTIONS))
ax.set_xticks(x)
ax.set_xticklabels(ALL_ACTIONS)
ax.bar(x, means, yerr=stderrs)
#ax.bar(x+0.25, blocking, width=0.25, label="Blocking", yerr=blocking_stds)
#plt.legend()
plt.show()


# means = [2.3333, 2.48148, 2.7777, 2.5555, ]
# stds = [0.03, 0.029, 0.029, 0.035, ]
# x = [0,1,2,3]
# fig, ax = plt.subplots()
# ax.bar(x, means, yerr=stds)
# ax.set_xticks(x)
# plt.title("Number of Parse Actions for Disambiguator")
# plt.ylabel("mean number of parse actions")
# plt.xlabel("condition")
# ax.set_xticklabels(["reduced_unambig", "reduced_ambig", "unreduced_unambig", "unreduced_ambig"])
# plt.show()

