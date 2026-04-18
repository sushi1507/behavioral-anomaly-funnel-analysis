CONVERSION RATES: Drop-off at each funnel stage

WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event = 'visit'          THEN user_id END) AS total_visitors,
        COUNT(DISTINCT CASE WHEN event = 'signup'         THEN user_id END) AS total_signups,
        COUNT(DISTINCT CASE WHEN event = 'activation'     THEN user_id END) AS total_activations,
        COUNT(DISTINCT CASE WHEN event = 'retention_day7' THEN user_id END) AS total_retained
    FROM user_events
)
SELECT
    total_visitors,
    total_signups,
    total_activations,
    total_retained,

    -- Conversion rates
    ROUND(total_signups    * 100.0 / NULLIF(total_visitors,   0), 1) AS visit_to_signup_pct,
    ROUND(total_activations * 100.0 / NULLIF(total_signups,   0), 1) AS signup_to_activation_pct,
    ROUND(total_retained   * 100.0 / NULLIF(total_activations,0), 1) AS activation_to_retention_pct,

    -- Drop-off
    (total_visitors   - total_signups)     AS dropped_at_signup,
    (total_signups    - total_activations) AS dropped_at_activation,
    (total_activations - total_retained)   AS dropped_at_retention

FROM funnel;