# NBA observations

Jupyter notebooks exploring aspects of the NBA.

The notebook FreeThrows looks at a suggestion of Jeff Van Gundy's to replace all free throws with a single free throw. The results are presented on [r/nba](https://www.reddit.com/r/nba/comments/5858ys/quantifying_records_with_jeff_van_gundys/).

The notebook BonusTime quantifies how long teams spend in the bonus. The results are on r/nba as [well](https://www.reddit.com/r/nba/comments/5bnc6i/time_spent_in_the_bonus_oc/).

The notebook And1 Heatmap plots a distribution of where and one opportunities occur. The interesting distributions are towards the middle of the notebook.

The notebook ArbitraryScoring looks at building a way to reevaluate the previous season based on different scoring systems, like adding a 4 point line. ArbitraryScoringApp is the beginning a flask app integrating these results. Some current difficulties:
- How do a let a user input a function safely? Using python's eval is unsafe.
- Make reevaluating seasons faster
- Add a plot of expected points per shot with a given scoring system.

