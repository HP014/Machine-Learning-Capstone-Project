# Datasheet

## Motivation

- **For what purpose was the dataset created?** It consists of evaluations of eight unknown "black-box" functions, used here to practise sample-efficient optimisation when each evaluation is limited. The course frames the task as solving a real-world optimisation challenge, where testing is expensive, time-consuming or resource-intensive (for example testing drug formulations with limited clinical trials, tuning manufacturing parameters with costly prototypes, or tuning a model that takes hours to train), and as building a portfolio piece that shows advanced optimisation techniques.
- **Who created the dataset, and who funded it?** The eight functions and the initial points were supplied by the course material of the Imperial College London Department of Computing and Imperial Executive Education, Professional Certificate in Machine Learning and Artificial Intelligence, Black-Box Optimisation Capstone Project. The course material does not say who built the functions or who funded the work. The outputs for my own queries were returned by the course's system, and I created the queries.

## Composition

- **What do the instances represent?** Each instance is one evaluation of one function: an input vector of 2 to 8 numbers between 0 and 1, and the scalar output it returned.
- **How many instances are there?** 279 in total, split across eight functions:

| Function | Inputs | Initial points | Points after Week 13 |
|---|---|---|---|
| F1 | 2 | 10 | 23 |
| F2 | 2 | 10 | 23 |
| F3 | 3 | 15 | 28 |
| F4 | 4 | 30 | 43 |
| F5 | 4 | 20 | 33 |
| F6 | 5 | 20 | 33 |
| F7 | 6 | 30 | 43 |
| F8 | 8 | 40 | 53 |

- **Is there any missing data?** No. Every query returned an output. Four rows are repeats of an earlier query (one in F1, one in F4, two in F5), and each returned the same output as the original, which suggests those functions are noise-free. The course describes F2's output as noisy, and no F2 query was repeated, so I could not check that.
- **Is there confidential data?** None that I know of. The data is purely numeric, with no personal information.

## Collection process

- **How was the data acquired?** The initial points for each function were supplied by the course at the start, as NumPy files (`initial_inputs.npy` and `initial_outputs.npy`). The course material does not say how they were generated, and their counts (10, 10, 15, 30, 20, 20, 30 and 40) match the course FAQ. After that, each week I submitted one new input per function and received its output.
- **Sampling strategy:** The initial points were supplied. Later points were chosen by me using Bayesian optimisation, so they concentrate in regions that looked promising and are not a uniform sample.
- **Time frame:** Thirteen weekly rounds, from about August to October 2026.

## Preprocessing/cleaning/labelling

- **Was any preprocessing done?** No cleaning or labelling was applied. The stored arrays contain the raw inputs and outputs exactly as received. Some models transform outputs internally (for example, F1 is modelled on the log of its absolute output), but the stored data is unchanged.
- **Was the raw data saved?** Yes. The stored arrays are the raw data, saved cumulatively, so each week's folder contains everything up to that week (`Data/Week_N/function_M/updated_inputs.npy` and `updated_outputs.npy`).

## Uses

- **What other tasks could the dataset be used for?** Benchmarking optimisation methods and surrogate models, or studying how models cope with extreme output scales (F1) and narrow peaks.
- **Is there anything that might affect future uses?** The points are not independent or evenly spread, because each one was chosen by an optimisation process, so they are unsuitable for statistics that assume random sampling. F1's outputs span hundreds of orders of magnitude. Four rows are repeated queries, caused by a missing duplicate check that was added in Week 6.
- **Tasks the dataset should not be used for:** Drawing conclusions about the true shape or maximum of any function beyond the regions sampled, or treating it as representative of real-world data.

## Distribution

- **How has the dataset already been distributed?** It is stored in this repository, which is public. The course's initial points are included with attribution to the course, and they remain the course's material. The rest is my own queries and the outputs returned for them.
- **Is it subject to any copyright, licence or terms of use?** The course material states no licence or terms of use for the data. The initial points remain the course's, and the data is shared here for educational, non-commercial purposes as part of a course portfolio. My code is released under the MIT licence (see `LICENSE`), which does not cover the course's initial points.

## Maintenance

- **Who maintains the dataset?** Hilton Patel (GitHub: HP014).
- **Will it be updated?** No. Week 13 was the final round, so the data is complete. Each `Data/Week_N` folder is an unchanged snapshot, and pipeline changes are recorded in `CHANGELOG.md`.
