# NBA observations

Jupyter notebooks exploring aspects of the NBA.

The notebook FreeThrows looks at a suggestion of Jeff Van Gundy's to replace all free throws with a single free throw. The results are presented on [r/nba](https://www.reddit.com/r/nba/comments/5858ys/quantifying_records_with_jeff_van_gundys/).

The notebook BonusTime quantifies how long teams spend in the bonus. The results are on r/nba as [well](https://www.reddit.com/r/nba/comments/5bnc6i/time_spent_in_the_bonus_oc/).

NBA Isolation Forests looks at applying isolation forests to different ways of calculating rate stats and is presented here [/rnba](https://www.reddit.com/r/nba/comments/5la7es/nba_isolation_forests/).

The notebook And1 Heatmap plots a distribution of where and one opportunities occur. The interesting distributions are towards the middle of the notebook.

The notebook ArbitraryScoring looks at building a way to reevaluate the previous season based on different scoring systems, like adding a 4 point line. ArbitraryScoringApp is the beginning a flask app integrating these results. Some current difficulties:
- What other stats do we want to see
- How to go from one shot distribution to another
