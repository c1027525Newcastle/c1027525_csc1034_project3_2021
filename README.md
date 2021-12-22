##Code Optimisation
###For the code optimisation i have changed the values of args.steps and args.repeats to 100 and 100_000 respectively to spend less time on waiting on the code to finish.

###stochastic_page_rank
Testing of the code that is present now for the stochastic_page_rank
function gives the following times: 15, 14.77, 14.11, 13.56,
15.20 seconds to an average of 14.53 seconds.

After changing the end of the function after and including the line:
hit_frequency = {},
to: hit_frequency = {node_list[i]: hit_count[i] for i in range(len(node_list))},
this now improves the code to a better time of an average of 14.12
seconds (after testing with times of: 14.3, 14.56, 14.06, 14.32,
13.38) due to the code being able to faster assign the keys and
values to the dictionary.