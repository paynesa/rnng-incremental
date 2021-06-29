"""Analyze the probability distribution over model predictions"""
import json
import numpy as np
import matplotlib.pyplot as plt

# get the target word for each of the sentences using the MVRR metadata
META_DATA = []
mvrr_json = json.load(open("../mvrr_analysis/mvrr.json"))
for item in mvrr_json["items"]:
    for sub_item in item["conditions"]:
        if sub_item["condition_name"] == "reduced_unambig":
            for region in sub_item["regions"]:
                if region["region_number"] == 5:
                    word = region["content"].split()[-1]
                    # one UNK-ification we need to deal with
                    if word == "chased":
                        word = "UNK-LC-ed"
                    META_DATA.append(word)

# all possible actions that the model could take as a next step
ALL_ACTIONS = ["REDUCE", "SHIFT", "NT(S)", "NT(PP)", "NT(NP)", "NT(PRN)", "NT(VP)", "NT(ADVP)", "NT(SBAR)", "NT(ADJP)", "NT(QP)", "NT(UCP)", "NT(WHNP)", "NT(SINV)", "NT(FRAG)", "NT(NAC)", "NT(WHADVP)", "NT(PRT)", "NT(NX)", "NT(WHPP)", "NT(SQ)", "NT(SBARQ)", "NT(CONJP)", "NT(WHADJP)", "NT(INTJ)", "NT(X)", "NT(RRC)", "NT(LST)" ]

overall_sentences = []
# average over the ten sentences in the input
for i in range(10):
    sentences = []
    target_idx = 0
    target_word = META_DATA[target_idx]
    print("PROCESSING FILE", i)
    for line in open(f"second_action/second_reduced_unambig_{i+1}.txt"):
        line = line.strip().split("\t")
        if len(line) > 1:
            word = line[0]
            # read in the probabilities for the current sentence if we are at the target
            if word == target_word:
                probabilities = [word.split(":") for word in line[1:]]
                prob_map = {action : 0 for action in ALL_ACTIONS}
                for action, prob in probabilities:
                    prob_map[action] = float(prob)
                sentences.append(prob_map)
                # update the target word to be the next sentence's target word
                target_idx += 1
                if target_idx < len(META_DATA):
                    target_word = META_DATA[target_idx]
    # make sure that we have the probabilities for each of the target words
    assert len(sentences) == len(META_DATA)
    overall_sentences.append(sentences)

averaged_lists = []
# average the probability distribution for each sentence separately
for i in range(len(META_DATA)):
    averaged_map = {action : np.mean(np.asarray([curr_list[i][action] for curr_list in overall_sentences])) for action in ALL_ACTIONS}
    averaged_lists.append(averaged_map)

# get the means and standard deviations across the means calculated above
means = [np.mean(np.asarray([curr[action] for curr in averaged_lists])) for action in ALL_ACTIONS]
stderrs = [np.std(np.asarray([curr[action] for curr in averaged_lists]))/len(averaged_lists) for action in ALL_ACTIONS]

# trim to only those with probability greater than 0.001 since there is a really long tail
ALL_ACTIONS = [ALL_ACTIONS[i] for i in range(len(ALL_ACTIONS)) if means[i]  > 0.001]
stderrs = [stderrs[i] for i in range(len(stderrs)) if means[i] > 0.001]
means = [mean for mean in means if mean > 0.001]

# plot the results
fig, ax = plt.subplots()
plt.ylabel("Probability")
plt.xlabel("Next Parse Step")
plt.title("Probability Distribution at Second Parse Action for Reduced Unambiguous")
x = np.arange(len(ALL_ACTIONS))
ax.set_xticks(x)
ax.set_xticklabels(ALL_ACTIONS)
ax.bar(x, means, yerr=stderrs)
plt.show()


