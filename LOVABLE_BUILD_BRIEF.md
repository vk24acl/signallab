# Continue SignalLab in Lovable

This is the original build brief for the now-published Lovable project. Live app: https://signallab-vikas-reddy.lovable.app/

The imported app preserves the tested calculations, dataset and provenance.

## Prompt for Lovable

Create **SignalLab — Growth decision studio**, an interactive portfolio project for **Vikas Reddy Konreddy**, applying for a product-oriented data science role. Use the attached SignalLab.html as the functional and visual reference, and the accompanying source package as the source of truth. It is a polished analytics application, not a landing page.

Visual direction: forest-green left navigation, soft off-white main canvas, white rounded panels, lime accents, generous spacing, Manrope-style headings and small restrained labels. Preserve the sidebar profile, synthetic-data badge and five views. Make the layout responsive and keyboard-accessible.

The fastest faithful import is to keep the self-contained implementation as `public/signallab.html` and render it in a full-viewport same-origin iframe from the root React route. Give the iframe an informative title. Do not sandbox it in a way that prevents its exports; all data are synthetic. This keeps the tested prototype intact while making it a real project created and deployed through Lovable. A later iteration can migrate views to typed React components using the same analytics functions and data.

If porting directly to React, copy the exact seeded dataset from `dist/data.json`, the numerical functions from `dist/analytics.js` and the logic in `dist/app.js`; do not replace working functionality with static placeholder values. Preserve the supplied Python and SQL as downloadable source. Do not add a database, API key, authentication wall or external AI calls. A recruiter should be able to open the published demo immediately.

Five views:

1. **Overview** — 12/8/4-week and acquisition-group filters; signups, activation, mature-cohort W4 retention and acquisition cost per activation; weekly activation chart; nested user funnel; calculated next-question notes.
2. **Channel lab** — all 43 searchable, sortable channels, pagination, CSV export; an illustrative budget allocation sandbox for 16 paid channels, fixed total spend, ±0–30% per-channel bounds, and three saturation assumptions. Clearly distinguish observed channel efficiency from causal effects.
3. **Experiment lab** — exact synthetic counts: control 1,498 / 3,731 and variant 1,642 / 3,774. Wilson intervals for individual rates; Newcombe difference interval; two-sided pooled two-proportion z-test. Original sample plan: 40% baseline, 10% relative MDE, α=.05, power=.80, 2,389 users/arm. Include an exploratory MDE slider that does not change the original plan. Two ITT guardrails: W4 retention and error-free first-session completion. Assignment-ratio check. Custom counts must be validated and do not imply a rollout decision; sparse expected counts must warn against the z-test approximation.
4. **Cohort retention** — actual weighted rates and a triangular maturity-aware heatmap. Cohort dates begin 20 Jul 2026; signup cohorts end 11 Oct 2026; snapshot is 19 Oct. W4 eligibility is limited to signup weeks 0–7. Missing follow-up is blank, not zero.
5. **Methods & source** — concise candidate context, six data checks, definitions, assumptions, statistical limitations, source downloads and full raw-data exports.

All 26,747 users are synthetic, reproducible from Python seed 43121. The app is inspired by the candidate's commercial marketing analytics experience, including a 43-channel optimisation project at Axtria. It must not claim the simulation is real client data, a real Lovable experiment, or a measured career achievement. Keep the “AI-assisted portfolio prototype” disclosure.

After building, verify every tab, the filters, zero-mature-cohort case, channel search/sorting/pagination, budget conservation and zero-change setting, sample planner, custom-input validation and all download controls. Publish the completed demo through Lovable and provide the exact live app URL and editable Lovable project URL returned by the platform. No password is needed for this entirely synthetic portfolio.

## Honest application description after actual Lovable publication

“SignalLab is an AI-assisted growth analytics project I created with Lovable. It connects my commercial analytics background with product data science through a 43-channel allocation sandbox, user funnel, cohort retention analysis and an experiment decision tool. It uses reproducible synthetic data, with SQL, Python, metric definitions and statistical assumptions available for inspection.”

The project is now published in Lovable. Describe your involvement accurately: it is an AI-assisted prototype imported into and published through Lovable.
