import numpy as np

GOLD_DEPTH = []
SENTENCES = []

for line in open("parses_tree_depth.txt", "r"):
    line = line.strip()
    max_depth = 0
    n_open = 0
    n_closed = 0
    for char in line:
        if char == "(":
            n_open += 1
        if char == ")":
            n_closed += 1
        if n_open - n_closed > max_depth:
            max_depth = n_open - n_closed
    GOLD_DEPTH.append(max_depth)
    SENTENCES.append(line)
print(len(SENTENCES), len(GOLD_DEPTH))

TEST_DEPTH = []
sent_num = -1
sentences = {}
for line in open("tree_depth_sentence_predictions_1.txt", "r"):
    line = line.split("\t")
    if len(line) < 2:
        sent_num += 1
        if sentences:
            line = [k for k, v in sorted(sentences.items(), key=lambda x : x[1])][-1]
            max_depth = 0
            n_open = 0
            n_closed = 0
            for char in line:
                if char == "(":
                    n_open += 1
                if char == ")":
                    n_closed += 1
                if n_open - n_closed > max_depth:
                    max_depth = n_open - n_closed
            TEST_DEPTH.append(max_depth)
        sentences = {}
    else:
        sentences[line[0]] = float(line[1])
        #print(sentences)
DIFFERENCES = np.asarray([GOLD_DEPTH[i]-TEST_DEPTH[i] for i in range(len(GOLD_DEPTH))])
print(np.mean(DIFFERENCES), np.std(DIFFERENCES)/np.sqrt(len(DIFFERENCES)))



# counter = 0
# sentences = []
# parses = []
# for line in open("testing_oracle.txt", "r"):
#     if counter == 0:
#         parses.append(line.strip())
#     if counter == 1:
#         sentences.append(line.strip())
#     counter += 1
#     if len(line.strip()) == 0:
#         counter = 0
#
# for i in range(1000):
#     with open("sentences_tree_depth.txt", "a") as f:
#         f.write(f"{sentences[i]}\n")
#     with open("parses_tree_depth.txt", "a") as f:
#         f.write(f"{parses[i]}\n")