# Tree Depth

This code can be used to compare the predicted tree depths on a set of sentences 
with the gold standard depths to see if the model systematically predicts shallower 
or deeper trees than the gold standard.

`gold_parses_tree_depth.txt` contains the gold standard parses for 1000 sentences in the testing set, 
and `unkified_tree_depth_sentences.txt` contains the corresponding sentences over which the model's predicted 
parses can be obtained -- an example of such an output is in `tree_depth_sentence_predictions.txt`. 

`tree_depth.py` takes in the output parses by a model and the gold standard of parses and calculates the 
average pairwise difference in depth across the two sets of trees. The format of the input file is expected to be 
the same as the format of `tree_depth_sentence_predictions.txt`, containing the partial parses and their 
probabilities for each particle only at the end of parsing, with partial parses excluded for this analysis. 

