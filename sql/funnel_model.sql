
FUNNEL MODEL: User journey from visit → signup → activation → retention


WITH funnel AS (
    SELECT
        user_id,
        COUNT(CASE WHEN event = 'visit'          THEN 1 END) AS visits,
        COUNT(CASE WHEN event = 'signup'         THEN 1 END) AS signups,
        COUNT(CASE WHEN event = 'activation'     THEN 1 END) AS activations,
        COUNT(CASE WHEN event = 'retention_day7' THEN 1 END) AS retained_day7,
        MIN(event_date)                                       AS first_seen,
        MAX(event_date)                                       AS last_seen
    FROM user_events
    GROUP BY user_id
)
SELECT
    *,
    CASE
        WHEN activations > 0 THEN 'Activated'
        WHEN signups > 0     THEN 'Signed Up Only'
        ELSE 'Visit Only'
    END AS user_stage
FROM funnel;