# A short walkthrough of SignalLab

Use this to learn the project, reproduce the calculations and prepare a discussion. Describe it as an AI-assisted portfolio prototype using synthetic data. Do not present its simulated lift as an Axtria result. The project is now published through Lovable; the existing tested app was imported unchanged into its React route.

## A two-minute demonstration

1. **Overview:** “The question is where a software product loses potential builders, and what we should test next.” Point to 26,747 signups, 42.5% activation and the signup-to-publish funnel. Switch to Referral and the last four signup weeks. Notice that week-4 retention becomes unavailable, rather than zero, because those users have not completed the observation window.
2. **Channel lab:** Reset the filters. Explain why this section has 43 channels: it draws on the scale of marketing optimisation work you supported at Axtria. Search for Google. Explain why lower observed cost per activation does not prove a channel causes more conversions. Change the budget cap and saturation assumption. The result is a planning hypothesis, not a measured improvement.
3. **Experiment lab:** Explain the independent randomized test. The variant activates 43.51% versus 40.15% in control. That is +3.36 percentage points, or +8.36% relative. The interval and guardrails inform the decision. Moving the sample planner does not retrospectively change the experiment's original plan.
4. **Cohorts:** Explain why the heatmap forms a triangle. Recent cohorts do not have enough follow-up. The aggregate curve weights users, not cohort percentages.
5. **Methods:** Show the raw data, executable SQL and Python generator. Distinguish your commercial context and project direction from the AI-assisted implementation.

## Questions you should be able to answer

### Why this project for a product data science role?

It connects acquisition, activation, retention and experimental decisions in one inspectable workflow. The project goes beyond showing a number: it asks what action the number might motivate, what evidence would support that action and what could invalidate the conclusion. Its commercial analytics component builds on your experience while the software funnel makes the application to product growth explicit.

### What is an activation rate?

The numerator is users completing a first successful build within 7 days. The denominator is all signups with a complete 7-day window. It is not successful builds divided by attempts; those answer different questions. The nested funnel prevents a publication from appearing without a preceding activation.

### What is the difference between percentage points and relative lift?

If control is 40.15% and treatment is 43.51%, the absolute difference is 43.51 − 40.15 = 3.36 percentage points. Relative lift divides the difference by control: 3.36 / 40.15 ≈ 8.36%. They should never be used interchangeably.

### What does the p-value mean?

Under the null of equal activation rates and the model's assumptions, it is the probability of obtaining a result at least as extreme as the observed difference. It is not the probability that the null is true, and it does not measure practical importance. Here, the data are deliberately simulated, so the result demonstrates a method rather than real-world efficacy.

### Why use confidence intervals as well?

They show the range of effect sizes compatible with the chosen procedure. The activation difference interval is approximately +1.13 to +5.59 points. A company should consider the plausible downside and the size of a useful effect, not just whether a p-value crosses 0.05. The app uses Wilson intervals for individual rates and Newcombe's method for their difference.

### How did you choose the sample size?

The demonstration fixes a 40% baseline, 10% relative minimum detectable lift, 5% two-sided significance level and 80% power. The resulting approximate requirement is 2,389 users in each arm. A 10% relative change from 40% means a target of 44%, or 4 percentage points. In real work, those assumptions need product and business justification before assignment begins.

### Why is a positive activation effect not sufficient?

Users might complete an initial project but have worse subsequent experiences. The example therefore checks week-4 retention and error-free first-session completion. Both retain all assigned users in their denominator. The retention lower confidence bound is close to the allowed −2-point margin; this is an important trade-off to discuss, not hide. A tighter acceptable loss would require more evidence before rollout.

### Does the budget model prove where money should go?

No. It assumes concave saturation curves anchored to synthetic baseline outcomes. It does not estimate a causal marketing-mix model, control for confounding, or account for cross-channel effects. It is useful for comparing assumptions and proposing a controlled test. It preserves the same total budget and enforces per-channel change limits.

### What are the most important engineering choices?

One deterministic user ledger feeds every view. Costs are aggregated before joining them to user metrics so spend is not multiplied by user counts. Data-quality checks test unique IDs, funnel nesting, valid channel references, observation boundaries, non-negative costs and experiment dates. The app handles absent eligible cohorts and validates custom experiment counts.

### What would you improve for production?

Start with event definitions, identity resolution, consent and reliable instrumentation. Add data freshness checks, bot exclusion, experiment assignment logs, sample-ratio monitoring and a formally pre-specified testing protocol. Use real outcome data to assess causal response rather than treating assumed saturation curves as learned models. Add persistence and access control only when real data and users require them.

## Before submitting

Run the app, change the inputs and reproduce the main calculations yourself. Read the generator and SQL so you can explain what they do. If a recruiter asks who implemented it, describe the AI assistance openly and explain the decisions and limitations you understand. The published application link is https://signallab-vikas-reddy.lovable.app/ and requires no password.
