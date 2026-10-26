# Datasheet

## Motivation

- **For what purpose was the dataset created?** It consists of evaluations of eight unknown "black-box" functions, used here to practise sample-efficient optimisation when each evaluation is limited. `[CONFIRM: the course's stated purpose for the functions]`
- **Who created the dataset, and who funded it?** The functions are provided through the course. `[CONFIRM: the team or institution that created them and who funded the work, if known]` The outputs for my own queries were returned by the course's system, and I created the queries.

## Composition

- **What do the instances represent?** Each instance is one evaluation of one function: an input vector of 2 to 8 numbers between 0 and 1, and the scalar output it returned.
- **How many instances are there?** 247 in total, split across eight functions:

| Function | Inputs | Initial points | Points after Week 9 |
|---|---|---|---|
| F1 | 2 | 10 | 19 |
| F2 | 2 | 10 | 19 |
| F3 | 3 | 15 | 24 |
| F4 | 4 | 30 | 39 |
| F5 | 4 | 20 | 29 |
| F6 | 5 | 20 | 29 |
| F7 | 6 | 30 | 39 |
| F8 | 8 | 40 | 49 |

- **Is there any missing data?** No. Every query returned an output. Four rows are repeats of an earlier query (one in F1, one in F4, two in F5).
- **Is there confidential data?** None that I know of. The data is purely numeric, with no personal information.

## Collection process

- **How was the data acquired?** The initial points for each function were provided at the start `[CONFIRM: how the initial points were generated and supplied]`. After that, each week I submitted one new input per function and received its output.
- **Sampling strategy:** The initial points were supplied. Later points were chosen by me using Bayesian optimisation, so they concentrate in regions that looked promising and are not a uniform sample.
- **Time frame:** Nine weekly rounds, from about August to October 2026.

## Preprocessing/cleaning/labelling

- **Was any preprocessing done?** No cleaning or labelling was applied. The stored arrays contain the raw inputs and outputs exactly as received. Some models transform outputs internally (for example, F1 is modelled on the log of its absolute output), but the stored data is unchanged.
- **Was the raw data saved?** Yes. The stored arrays are the raw data, saved cumulatively, so each week's folder contains everything up to that week (`Data/Week_N/function_M/updated_inputs.npy` and `updated_outputs.npy`).

## Uses

- **What other tasks could the dataset be used for?** Benchmarking optimisation methods and surrogate models, or studying how models cope with extreme output scales (F1) and narrow peaks.
- **Is there anything that might affect future uses?** The points are not independent or evenly spread, because each one was chosen by an optimisation process, so they are unsuitable for statistics that assume random sampling. F1's outputs span hundreds of orders of magnitude. Four rows are repeated queries.
- **Tasks the dataset should not be used for:** Drawing conclusions about the true shape or maximum of any function beyond the regions sampled, or treating it as representative of real-world data.

## Distribution

- **How has the dataset already been distributed?** It is stored in this repository. `[CONFIRM: whether the course allows the data to be shared publicly before making the repository public]`
- **Is it subject to any copyright, licence or terms of use?** `[CONFIRM: any licence or terms from the course]`

## Maintenance

- **Who maintains the dataset?** Hilton Patel (GitHub: HP014), who adds one new week of data after each round.
