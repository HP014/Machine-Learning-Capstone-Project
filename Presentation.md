# BBO capstone project presentation

The text of my presentation, written into the course's presentation template after the final (Week 13) round. The same text, laid out in the template, is in `BBO capstone project presentation - Hilton.pdf`.

## 1. An overview of my BBO approach

### What I'm trying to achieve

Eight unknown "black-box" functions each take between 2 and 8 inputs (every input between 0 and 1) and return a score. I can't see how any of them work, and I got only one query per function per week, for thirteen weeks. The goal was to find the inputs that give each function its highest score while wasting as few queries as possible. In plain terms, it's a search for the best settings on eight mystery machines, where every try is precious.

### My overall strategy

I use Bayesian optimisation, which ran as a weekly loop:

1. Review: compare last week's results with what each model predicted, measured in standard deviations.
2. Learn: fit a Gaussian Process (GP) to all the data so far, with a Random Forest as a second opinion. Each gives a prediction and an uncertainty for any candidate point.
3. Predict: score candidate points with Upper Confidence Bound (UCB) or Expected Improvement (EI), which weigh a high prediction against high uncertainty.
4. Choose: for each function, use the method that has earned trust there. That's usually a GP search close to the best point, and a step-by-step pattern search for F1. Where the GP failed, I measured the function directly with small steps.
5. Test: submit one query per function and record the reasoning in a weekly changelog.

### How it fits together

The review step is what makes the loop improve over time. It tells me which model to rely on for each function, how far from the best point it's worth searching, and when to change method. After thirteen rounds, every function finished above its starting best. Week 8 was the first round in which all eight set a new best at once, and 31 of my 46 new bests came from Week 8 onwards. Five functions (F2, F4, F5, F7 and F8) were still improving on the very last query.

### Final best scores

F1 1.43e-4, F2 0.742, F3 -0.0054, F4 0.714, F5 4,246, F6 -0.0575, F7 2.754, F8 9.975.

## 2. How my strategy has evolved

### Key changes since the early rounds

- Where I search: early on I scored 10,000 random points across the whole input space. From Week 8 I searched a small box (+/-0.02) around each function's best point (+/-0.04 for F3 and F4 from Week 7).
- Models: I started with one GP per function and tuned the kernel and the exploration setting (kappa) by feel. I added a Random Forest in Week 6 but stopped choosing its picks from Week 7, because it can never predict above the best value it has seen, which is no use for small improving steps. For F1 I modelled the log of the output (Week 7), then switched to a pattern search.
- Safeguards: I added a check that blocks any point within 0.001 of one already sampled, a minimum length-scale so GP fits can't collapse into noise, and normalised outputs.
- Reviewing: I used to look only at whether the best had improved. Now I measure every miss against its prediction and log it.
- Direct measurement: where the GP's predictions failed, I used line searches, half steps and one-input-at-a-time probes (F1, F2, F4, F6).

### What influenced these changes

- Model performance: the GP was confidently wrong on F4, landing about 6 standard deviations below its prediction. In Week 6 all four Random Forest picks landed within about 1.1 standard deviations, yet none set a new best. Across all 39 logged GP predictions, only 49% landed within one standard deviation.
- Data trends: big jumps across the space gave my worst results, while small steps near the best point kept improving.
- Wasted queries: F5's best point was queried three times before I added the duplicate check.
- Intuition played a smaller part. Most changes followed a specific failure I could point to in the data.

### Heuristics that now guide my decisions

1. Trust whichever model has predicted well for that function, and keep checking it against outcomes.
2. Never spend a query on a point I've already sampled.
3. Once a good region is found, take small steps around it.
4. Change one setting at a time, starting with the search box size before kappa.
5. If a model has no usable signal, measure the function directly with a small step.
6. Check any fitted curve against real results before trusting it (a curve through F1's profile predicted +2.2e-4 and the query returned -2.14e-4).

## 3. Patterns, data and insights

### The most meaningful trends

- Gains came in bursts. Most functions stayed flat for several weeks during wide exploration and then jumped once I switched to small steps around the best point. Week 8 was the first round in which all eight functions set a new best, for example F4 rose from 0.37 to 0.61, F5 from 2,987 to 3,175 and F6 from -0.19 to -0.10.
- After Week 8 progress was steady: F5 rose in each of the last six rounds, to 4,246 (up 42%), F4 reached 0.71, F1 rose about eleven orders of magnitude to 1.43e-4, and F2 reached 0.742 on the final query. F3 (-0.0054 since Week 9) and F6 (-0.0575 since Week 12) levelled off, which fits narrow peaks that one query a week was too slow to find.
- The GP is overconfident. Only 49% of its 39 logged predictions landed within one standard deviation of the actual result (about 68% for a well-calibrated model) and 79% within two (about 95%).

### Variables that influence results the most

Measuring how closely each input moves with the output (Spearman rank correlation, all 279 observations), a few inputs explain most of the variation, much like the first principal components in PCA:

- F5: x4 (0.88), x3 (0.78) and x2 (0.75) dominate, and its best point has x3 = x4 = 1.0, the upper limit.
- F8: x3 (-0.73), x1 (-0.67) and x7 (-0.60) are strongest, with x2 and x4 (about -0.44) next, so it behaves like a lower-dimensional function.
- F6: x4 (0.59) and x5 (-0.53). F7: x1 (-0.73), with its best point at x1 = 0.047, close to 0.
- F3: no input correlates strongly (none above 0.17), which matches its flat landscape.
- F1: almost every output is effectively zero (as small as 1e-245), so models trained on raw values can't see any pattern.

The biggest single factor across all functions was distance from the best point: large jumps caused most of the spread in my results, and small local steps produced the steady gains.

### How this shaped my understanding

I now see the search as two phases: first locate a good region, then refine it carefully. In the higher-dimensional functions I can step mainly along the inputs that matter and hold the rest roughly fixed. F2 and F3 showed how sharp a peak can be: on F2, moves of just 0.003 in an input changed the output by 0.04 to 0.12. I've also learned not to take a model's uncertainty at face value, because the places it is most uncertain are often where it is least reliable.

## 4. Decision-making and iteration

### Balancing exploration and exploitation

In Weeks 1 to 6 I explored widely, with fairly high UCB settings, to find each function's good region. Once a region was clearly good, more exploration cost more than it gained. In Weeks 7 and 8 every query sat within about 0.02 to 0.04 of the best point, and all eight functions improved in Week 8. I tested whether kappa still mattered inside the small search box. Raising it from 0 to 2 moved most picks by less than 0.03, so I treated the box size as my main exploration setting. In Weeks 9 to 13 I kept exploiting, with some cheap exploration: probing the input boundary for F5 and F7, and a step at right angles on F4, which gained 0.058 on the final query.

### Strategic decisions: what worked and why

- Local search on F4 (worked): the global search picked a point the GP itself predicted at -13, because uncertainty is highest in empty regions. Searching near the best point instead took F4 from -2.83 to 0.27, and later to 0.71. A line search predicted 0.645 and returned 0.657.
- Pattern search on F1 (worked): F1's outputs look like zero almost everywhere, so neither model could find a direction. A single small step of +0.012 in x2 multiplied the output by 12, which gave me a direction to follow.
- One input at a time on F2 (worked): it stayed at 0.667 for five weeks. Probing x1 bracketed its peak, and a curve through three points on x2 put the peak near 0.908. The query at 0.9095 returned 0.742, beating both the prediction (about 0.72) and the old best.
- Far exploratory jumps (didn't work): F7's Week 7 pick scored 0.93 against a prediction of 1.70, a miss of 4.1 standard deviations. The Random Forest on F4 predicted -6.65, far outside anything observed. I dropped both.

### Handling uncertainty

Each week I measured every miss in standard deviations and adjusted:

- If a model is overconfident, I shrink the step or switch to a method that measures the function directly.
- If a model is too cautious (F6 beat its prediction by 5 standard deviations), I keep stepping in that direction.
- If a model has no usable signal (F4's GP was equally unsure everywhere nearby), I repeat the last step that worked.

With 279 observations across eight functions, I treat these as working conclusions rather than proof.

## 5. Next steps and reflection

### What I would do next

- Exploit sooner: F5 found its peak in Week 1 and F4 reached 0.37 by Week 3, yet both stalled for five to seven weeks while I kept exploring. Once I took small steps they improved every week.
- Build the safeguards on day one: a duplicate check and a prediction log from Week 1 would have saved four wasted queries.
- Study each function before modelling it: F1's output range (1e-245 to 1e-3) meant raw-value models could see nothing until I modelled its log in Week 7.
- Try a wider range of models, such as BoTorch, especially for the higher-dimensional functions where 10,000 random candidates search the space coarsely. A peer who raised kappa in UCB to 1000 reached 8,267 on F5 against my 4,246, so I'd pair an extreme kappa with local refinement once the peak is found.
- The repository now has relative paths, two notebooks, the working scripts, a requirements file and clone-and-run steps, so the results can be reproduced.

### Connection to the broader ML landscape

This project is a small version of hyperparameter tuning and experiment design, where each trial is expensive and you can't test everything. Bayesian optimisation is how many AutoML tools search for good model settings. The lesson that a model's confidence must be checked against real results applies to any ML system in production, such as tuning thresholds where every live test has a cost.

### Communicating to a non-technical audience

"Imagine eight mystery machines, each with a few dials. I got one try per machine each week, so I used the results so far to predict which settings were worth trying next, balancing careful tweaks to what already worked with occasional tests of something new. Over thirteen weeks, every machine's best score went up." I'd lead with that outcome and show a simple chart of the best score by week, rather than any model details.
