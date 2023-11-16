This dataset was gathered during an online experiment on the website https://vote.imag.fr/0

Analysis of the results (in French): https://vote.imag.fr/results/online-2022

This dataset contains:

* voters.csv
	- time: day the voter did the experiments
	- country: Country code of the voter
	- studies: Level of studies of the voter
	- socpro: Socio-Professional category of the voter
	- age: Age range of the voter
	- gender: gender of the voter (f=woman, h=man)
	- official_vote: their official vote at the election
	- opinion_on_system: score between -2 and 2 on the current voting system
	- rule_1, rule_2, rule_3, rule_4: the 4 voting rules tested by the voter
* weights.csv: suggested weights for the voters, based on their official vote at the election
* opinions.csv: score between -2 and 2 on the different voting rules tested by the voter.

Votes datasets:
* votes/approval.csv: Approval voting
* votes/borda.csv: Borda voting (number = rank of the candidate) with 4 ranked candidates
* votes/condorcet.csv: Pairwise comparisons of candidates
* votes/irv_1.csv: IRV with at least 4 ranked candidates
* votes/irv_2.csv: IRV with no constraints
* votes/majority_judgement_5: Majority Judgement (5 labels: Insuffisant, Passable, Assez bien, Bien, Très bien)
* votes/majority_judgement_7: Majority Judgement (7 labels: + A rejeter and Excellent)
* votes/notes.csv: opinion on a 0-100 scale given through a slider with a sad face for 0 and happy face for 100.
* votes/scores_3_neg: Score Voting (-1,0,1)
* votes/scores_3_pos: Score Voting (0,1,2)
* votes/scores_4_neg: Score Voting (-1,0,1,2)
* votes/scores_4_pos: Score Voting (0,1,2,3)
