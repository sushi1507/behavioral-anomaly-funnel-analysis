-- ============================================================
-- BEHAVIORAL ANOMALY DETECTION
-- Flags sudden drops in retention/engagement per cohort
-- ============================================================

WITH user_funnel AS (
    SELECT
        user_id,
        COUNT(CASE WHEN event = 'visit'          THEN 1 END) AS visits,
        COUNT(CASE WHEN event = 'signup'         THEN 1 END) AS signups,
        COUNT(CASE WHEN event = 'activation'     THEN 1 END) AS activations,
        COUNT(CASE WHEN event = 'retention_day7' THEN 1 END) AS retained_day7
    FROM user_events
    GROUP BY user_id
),
metrics AS (
    SELECT
        user_id,
        CASE WHEN signups > 0
             THEN ROUND(activations * 1.0 / signups, 2)
             ELSE 0 END AS activation_rate,
        CASE WHEN activations > 0
             THEN ROUND(retained_day7 * 1.0 / activations, 2)
             ELSE 0 END AS retention_rate
    FROM user_funnel
)
SELECT
    user_id,
    activation_rate,
    retention_rate,

    -- Anomaly flags
    CASE
        WHEN retention_rate = 0 AND activation_rate = 1
            THEN 'DROP-OFF: Activated but never retained'
        WHEN activation_rate = 0 AND retention_rate = 0
            THEN 'DROP-OFF: Signed up but never activated'
        ELSE 'Normal Journey'
    END AS anomaly_flag,

    -- Risk tier
    CASE
        WHEN retention_rate < 0.3 THEN 'HIGH DROP-OFF RISK'
        WHEN retention_rate < 0.6 THEN 'MEDIUM RISK'
        ELSE 'HEALTHY'
    END AS retention_tier

FROM metrics
ORDER BY retention_rate ASC;