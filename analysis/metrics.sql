-- SignalLab / synthetic portfolio data. SQLite-compatible examples.
-- Import users.csv as users and channel_costs.csv as channel_costs.
-- Definitions: activated = first successful project within 7 days;
-- point retention W4 = activity in week 4 among users with 4 weeks of follow-up.
-- Acquisition cost includes allocated organic effort, not just media spend.

-- 1. Deduplicated user-level funnel: never join a many-row event table first.
SELECT signup_week,
       COUNT(*) AS signups,
       SUM(started) AS started,
       SUM(activated_7d) AS activated,
       SUM(published_7d) AS published,
       1.0 * SUM(activated_7d) / NULLIF(COUNT(*), 0) AS activation_rate
FROM users
GROUP BY signup_week
ORDER BY signup_week;

-- 2. Channel spend is aggregated before the user join to avoid cost fan-out.
WITH user_metrics AS (
    SELECT channel_id, COUNT(*) AS signups, SUM(activated_7d) AS activated,
           SUM(CASE WHEN signup_week <= 7 THEN 1 ELSE 0 END) AS eligible_w4,
           SUM(CASE WHEN signup_week <= 7 AND (active_week_mask & 16) != 0
                    THEN 1 ELSE 0 END) AS retained_w4
    FROM users GROUP BY channel_id
), spend AS (
    SELECT channel_id, SUM(acquisition_cost_gbp) AS cost
    FROM channel_costs GROUP BY channel_id
)
SELECT u.*, s.cost,
       1.0 * activated / NULLIF(signups,0) AS activation_rate,
       1.0 * retained_w4 / NULLIF(eligible_w4,0) AS retention_w4,
       s.cost / NULLIF(activated,0) AS cost_per_activated_user
FROM user_metrics u JOIN spend s USING(channel_id);

-- 3. Intention-to-treat A/B analysis. Every assigned user stays in denominator.
SELECT experiment_arm, COUNT(*) AS assigned,
       SUM(activated_7d) AS activated,
       SUM(CASE WHEN (active_week_mask & 16) != 0 THEN 1 ELSE 0 END) AS retained_w4,
       SUM(started) AS attempted_sessions,
       SUM(error_free_session) AS error_free_sessions
FROM users WHERE experiment_arm IN (1,2)
GROUP BY experiment_arm;

-- 4. Explicit maturity restriction prevents recent cohorts appearing to churn.
SELECT signup_week, COUNT(*) AS eligible,
       1.0 * SUM(CASE WHEN (active_week_mask & 16) != 0 THEN 1 ELSE 0 END)
           / COUNT(*) AS point_retention_w4
FROM users WHERE signup_week <= 7
GROUP BY signup_week;

-- 5. Data contract / quality checks. All should return zero failures.
SELECT 'duplicate_user_id' AS check_name, COUNT(*)-COUNT(DISTINCT user_id) AS failures FROM users
UNION ALL
SELECT 'invalid_funnel',COUNT(*) FROM users
 WHERE published_7d>activated_7d OR activated_7d>started
UNION ALL
SELECT 'unknown_channel',COUNT(*) FROM users WHERE channel_id NOT BETWEEN 0 AND 42
UNION ALL
SELECT 'invalid_week',COUNT(*) FROM users WHERE signup_week NOT BETWEEN 0 AND 11;
