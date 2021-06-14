import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("surprisals_digging_in.txt", sep="\t")

without_commas = df[df["sentence_id"] <= 186]
with_commas = df[df["sentence_id"] > 186]
CONDITIONS = ["", "no_blocker_short", "no_blocker_long", "no_blocker_very_long", "blocker_short", "blocker_long", "blocker_very_long"]
surprisal_means_with_commas = []
surprisal_means_without_commas = []
surprisal_stds_with_commas = []
surprisal_stds_without_commas = []

for i in range(6):
    group_without_commas = without_commas[(without_commas["sentence_id"] <= 31*(i+1)) & (without_commas["sentence_id"] > 31*(i))]
    group_with_commas = with_commas[(with_commas["sentence_id"] <= 186+(31*(i+1))) & (with_commas["sentence_id"] > 186+(31*i))]
    surprisals_without_commas = []
    surprisals_with_commas = []
    for sentence_id in set(group_with_commas["sentence_id"]):
        curr_sentence = group_with_commas[group_with_commas["sentence_id"] == sentence_id]
        surprisals_with_commas.append(np.asarray(curr_sentence["surprisal"])[-2])
    for sentence_id in set(group_without_commas["sentence_id"]):
        curr_sentence = group_without_commas[group_without_commas["sentence_id"] == sentence_id]
        surprisals_without_commas.append(np.asarray(curr_sentence["surprisal"])[-2])
    surprisals_without_commas = np.asarray(surprisals_without_commas)
    surprisals_with_commas = np.asarray(surprisals_with_commas)

    surprisal_means_without_commas.append(np.mean(surprisals_without_commas))
    surprisal_stds_without_commas.append(np.std(surprisals_without_commas)/np.sqrt(31))
    surprisal_means_with_commas.append(np.mean(surprisals_with_commas))
    surprisal_stds_with_commas.append(np.std(surprisals_with_commas)/np.sqrt(31))

# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
fig, ax = plt.subplots()
plt.ylabel("Mean surprisal")
plt.xlabel("Condition")
plt.title("Digging in Surprisals with Particle Filter, k=100")
x = np.arange(6)
ax.set_xticklabels(CONDITIONS)
ax.bar(x, surprisal_means_without_commas, width=0.25, label="No Comma", yerr=surprisal_stds_with_commas)
ax.bar(x+0.25, surprisal_means_with_commas, width=0.25, label="Comma", yerr=surprisal_stds_without_commas)
plt.legend()
plt.show()

