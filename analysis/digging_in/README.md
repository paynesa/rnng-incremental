## Digging in 

We consider a subset of the data in `unkigied_digging_in_sentences.txt` including
only the non-blocking sentences, following Futrell et al 2019. This data can be extracted
with `digging_data.py` and is in `relevant_digging_in_sentences.txt.`

The model is run 10 times on each value of `k` for the particles and results 
are averaged across these values: results for the model trained on `bllip` are in 
`results_bllip`. To create a graph comparing the no-comma vs. comma conditions for each 
of the `short, long` and `very_long` conditions, run `digging_in_analysis.py`.