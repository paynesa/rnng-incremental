## Main Verb/Reduced Relative

We consider a set of MVRR sentences, given in `mvrr.txt`, with their UNK-ified
versions given in `unkified_mvrr.txt`. The sentences correspond to four conditions: 
`reduced/unreduced` correspond to the status of the relative clause and `ambiguous/unambiguous` correspond
to the verb either being able to appear as both a past participle and main verb (`ambiguous`) or 
only one (`unambiguous`). The sentences are divided based on these conditions in 
`unkified_mvrr_reduced_ambig.txt`, `unkified_mvrr_reduced_unambig.txt`, `unkified_mvrr_unreduced_ambig.txt`, and 
`unkified_mvrr_unreduced_unambig.txt`. 

Metadata stored in `mvrr.json` divides each sentence into six portions corresponding to 
the beginning, end, noun, relative clause, ambiguous verb, and disambiguator. This meta-data
may be used with the output surprisals of the model in order to analyze performance, as is done in 
`mvrr_stderr.py`. This file analyzes one of the six possible sentence regions and considers 
surprisal as a function of `k` for each of the four conditions, where `k` is the number of particles 
or beam size. 

Results on the `mvrr` data for the ptb-trained model can be found in 
`beam_ptb_results` and `particle_ptb_results`, while results for the bllip-trained model
can be found in `particle_bllip_results`.