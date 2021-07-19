import pandas as pd
import argparse

def main():
    """Execute the main portion of the code """
    # parse the arguments from the user
    parser = argparse.ArgumentParser(description="Process the files into a compatible format")
    parser.add_argument("dir", type=str, help="the directory containing the files to process")
    parser.add_argument("out", type=str, help="the name of the output file")
    parser.add_argument("-n", type=int, help="number of runs to consider (default=10)", default=10)
    args = parser.parse_args()
    DIR = args.dir
    OUTPUT = args.out
    N = args.n
    print(f"Processing the {N} results in {DIR}...")
    # load in the full text of the sentences so we can use that to match on
    SENTS = []
    for line in open("sents.txt"):
        line = line.strip()
        if line:
            SENTS.append(line)
    # the three types of decoding we're considering for each trained model
    TYPES = ["beam", "particle_m100", "regular_particle"]
    # the dataframe in which the averaged results will be stored
    OVERALL_DF = None
    # iterate through each of the types
    for type in TYPES:
        print(f"\tProcessing {type}...")
        # merge each of the 10 files into the overall dataframe to average later
        for i in range(10):
            curr_file = f"{DIR}/{type}-{i + 1}.txt"
            df = pd.read_csv(curr_file, sep="\t")
            # get the full text of the sentence in case of ambiguity in sentence number
            df["sentence"] = [SENTS[i - 1] for i in list(df["sentence_id"])]
            # rename the surprisal column to reflect the file we're considering
            df = df.rename(columns={"surprisal": f"{type}-{i + 1}",
                                    "token_id": "word_number"})
            # if this is the first file we've considered, then it becomes the dataframe we're working with
            if OVERALL_DF is None:
                OVERALL_DF = df
            # otherwise, merge the column of the file we're currently considering into the overall dataframe
            else:
                OVERALL_DF = pd.merge(OVERALL_DF, df, on=["sentence", "word_number",
                                                    "sentence_id", "token"])
        # average the columns that have been added for this decoding pattern
        col = OVERALL_DF.loc[:, f"{type}-{1}":f"{type}-{10}"]
        OVERALL_DF[f"{type}"] = col.mean(axis=1)
        # delete the columns that were used in calculating the average since we don't need them anymore
        for i in range(10):
            del OVERALL_DF[f"{type}-{i + 1}"]
    # write out the results
    print(f"Writing results to {OUTPUT}...")
    OVERALL_DF.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()