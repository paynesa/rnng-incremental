import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


meta_data = []
REGION_NUMBER = 6
PARTICLE_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40]
REGION_DATA = {
        1 : "Start",
        2 : "Noun",
        3 : "Ambiguous verb",
        4 : "RC contents",
        5 : "Disambiguator",
        6 : "End"
    }

i = 0
mvrr_f = open("mvrr.json")
mvrr_json = json.load(mvrr_f)
for item in mvrr_json["items"]:
    for sub_item in item["conditions"]:
        meta_data.append(sub_item)
reduced_ambig_mean = []
reduced_unambig_mean = []
unreduced_ambig_mean = []
unreduced_unambig_mean = []
reduced_ambig_std = []
reduced_unambig_std = []
unreduced_ambig_std = []
unreduced_unambig_std = []
for num_particles in PARTICLE_NUMBERS:
    reduced_ambig = []
    reduced_unambig = []
    unreduced_ambig = []
    unreduced_unambig = []
    for i in range(10):
        print(f"processing mvrr_{num_particles}_{i+1}.txt...")
        file = pd.read_csv(f"mvrr_{num_particles}_{i+1}.txt", sep="\t")
        for i in range(len(meta_data)):
            sentence = file[file["sentence_id"] == i+1]
            counter = 0
            condition_name = meta_data[i]["condition_name"]
            for region in meta_data[i]["regions"]:
                counter += len(region["content"].split())
                if region["region_number"] == REGION_NUMBER:
                    surprisal = np.asarray(sentence["surprisal"])[counter-1]
                    if condition_name == "reduced_ambig":
                        reduced_ambig.append(surprisal)
                    elif condition_name == "reduced_unambig":
                        reduced_unambig.append(surprisal)
                    elif condition_name == "unreduced_unambig":
                        unreduced_unambig.append(surprisal)
                    else:
                        unreduced_ambig.append(surprisal)
    reduced_ambig = np.asarray(reduced_ambig)
    reduced_ambig_mean.append(np.mean(reduced_ambig))
    reduced_ambig_std.append(np.std(reduced_ambig)/np.sqrt(len(reduced_ambig)))

    reduced_unambig = np.asarray(reduced_unambig)
    reduced_unambig_mean.append(np.mean(reduced_unambig))
    reduced_unambig_std.append(np.std(reduced_ambig)/np.sqrt(len(reduced_unambig)))

    unreduced_ambig = np.asarray(unreduced_ambig)
    unreduced_ambig_mean.append(np.mean(unreduced_ambig))
    unreduced_ambig_std.append(np.std(unreduced_ambig)/np.sqrt(len(unreduced_ambig)))

    unreduced_unambig = np.asarray(unreduced_unambig)
    unreduced_unambig_mean.append(np.mean(unreduced_unambig))
    unreduced_unambig_std.append(np.std(unreduced_unambig)/np.sqrt(len(unreduced_unambig)))

fig, ax = plt.subplots()
plt.title(f"Surprisals for MVRR at {REGION_DATA[REGION_NUMBER]}")
plt.xlabel
ax.errorbar(PARTICLE_NUMBERS, unreduced_ambig_mean, yerr=unreduced_ambig_std, label="unreduced_ambig")
ax.errorbar(PARTICLE_NUMBERS, unreduced_unambig_mean, yerr=unreduced_unambig_std, label="unreduced_unambig")
ax.errorbar(PARTICLE_NUMBERS, reduced_ambig_mean, yerr=reduced_ambig_std, label="reduced_ambig")
ax.errorbar(PARTICLE_NUMBERS, reduced_unambig_mean, yerr=reduced_unambig_std, label="reduced_unambig")
plt.legend()
plt.show()






