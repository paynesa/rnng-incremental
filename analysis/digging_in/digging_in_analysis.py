"""Plots the differences in comma and no-comma surprisal across each of the three
lengths of intervening material (short, long, very long) as a function of
the number of particles"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# keep track of the values of k we're considering
PARTICLE_NUMBERS = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]

#keep track of the means and stderrs for each value of k for each of the 3 cases
SHORT_MEANS = []
SHORT_STDERRS = []
LONG_MEANS = []
LONG_STDERRS = []
VERY_LONG_MEANS = []
VERY_LONG_STDERRS = []

# calculate means and stderrs for each value of k
for particle_number in PARTICLE_NUMBERS:
    print(particle_number)
    DIFFERENCES = []
    # average over the 10 runs
    for i in range(10):
        df = pd.read_csv(f"results_bllip/{particle_number}-dig-{i+1}.txt", sep="\t")
        sentence_surprisals = []
        for sentence_id in set(df["sentence_id"]):
            sentence_surprisals.append(np.asarray(df[df["sentence_id"] == sentence_id]["surprisal"])[-2])
        no_commas = sentence_surprisals[:93]
        commas = sentence_surprisals[93:]
        DIFFERENCES.append([no_commas[i]-commas[i] for i in range(93)])
    # take the means of the differences betweeen the comma and no comma condition across the 10
    MEAN_DIFFERENCES = [np.mean(np.asarray([sen[i] for sen in DIFFERENCES])) for i in range(93)]
    # break it up by the three conditions
    SHORT_MEANS.append(np.mean(MEAN_DIFFERENCES[:31]))
    SHORT_STDERRS.append(np.std(MEAN_DIFFERENCES[:31])/np.sqrt(31))
    LONG_MEANS.append(np.mean(MEAN_DIFFERENCES[31:62]))
    LONG_STDERRS.append(np.std(MEAN_DIFFERENCES[31:62])/np.sqrt(31))
    VERY_LONG_MEANS.append(np.mean(MEAN_DIFFERENCES[62:]))
    VERY_LONG_STDERRS.append(np.std(MEAN_DIFFERENCES[62:])/np.sqrt(31))

# plot the results_bllip
fig, ax = plt.subplots()
plt.title(f"Particle Filter Surprisals for Digging In")
ax.errorbar(PARTICLE_NUMBERS, SHORT_MEANS, yerr=SHORT_STDERRS, label="short")
ax.errorbar(PARTICLE_NUMBERS, LONG_MEANS, yerr=LONG_STDERRS, label="long")
ax.errorbar(PARTICLE_NUMBERS, VERY_LONG_MEANS, yerr=VERY_LONG_STDERRS, label="very_long")
plt.ylabel("mean differences in surprisal")
plt.xlabel("number of particles")
plt.legend()
plt.show()











