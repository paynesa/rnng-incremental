"""Gets the digging in sentences that are non-blocking, since the other ones were
not included in Futrell et al 2019"""
i =0
lines = []
for line in open("../unkified_digging_in_sentences.txt"):
    if i < 93:
        lines.append(line)
    if i >= 186 and i < 279:
        lines.append(line)
    i += 1
for line in lines:
    with open("../relevant_digging_in_sentences.txt", "a") as f:
        f.write(line)