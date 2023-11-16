This dataset was gathered by researchers for the "Voter Autrement" experiment. It was conducted online on the website vote.imag.fr

Reference: "Voter Autrement 2017 - Online Experiment" (see cite.bib)

This dataset contains:

* voters.csv
	- official_vote: Vote of the voter at the election
	- gender: gender of the voter (F=woman, M=man)
	- age: Age range of the voter
	- work: Socio-Professional category of the voter
	- education: Education level of the voter
	- vote_is_a_right: Do you think voting is a right?
	- vote_is_a_duty: Do you think voting is a duty?
	- vote_is_a_chance: Do you think voting is a chance?
	- vote_is_useful: Do you think voting is useful?
	- position: On a scale from 0 (left) to 10 (right), where would you put yourself?
	- after_vote: was the experiments conducted after the vote took place?
	if previous question is True:
	- voted_sincerely: Did you voted sincerely at the election?
	- voted_strategically: Did you voted strategically at the election?
	- other_motivation: free text area
	- regret_evaluation: evaluated regret (-2 to 2, -2 is max regret)
	- should_have_voted: I should have voted for...
	- should_have_voted_sincerely: Do you think you should have voted sincerely?
	- should_have_voted_strategically: Do you think you should have voted strategically?
	- should_have_voted_otherwise: Free text area
	- second_round_vote: Vote in the second round (Marine Le Pen/Emmanuel Macron)
	- rule_tested_1 to rule_tested_3: Voting rules tested by the voter
* weights.csv: suggested weights for the voters, based on their official vote at the election
* weights_before.csv: weights only of voters who answered before the election
* weights_after.csv: weights only of voters who answered after the election
* opinions.csv: Evaluation (-2 to 2) of the alternative voting rules and of plurality with runoff (the official rule)

Votes datasets:
* votes/approval.csv: Approval
* votes/borda.csv: Borda (4 ranked candidates)
* votes/condorcet.csv: Pairwise comparisons
* votes/irv_1.csv: IRV (no constraints)
* votes/irv_2.csv: IRV (4 ranked candidates min)
* votes/notes.csv: Opinions on the candidates given with a slider with a sad face at 0 and happy face at 100
* votes/scores_1.csv: Score Voting (-1,0,1)
* votes/scores_2.csv: Score Voting (-1,0,1,2)
* votes/scores_3.csv: Score Voting (0,1,2)
* votes/scores_4.csv: Score Voting (0,1,2,3)


