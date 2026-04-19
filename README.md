# Behavioral Anomaly & Funnel Analysis

**Product funnel analytics with behavioral anomaly detection — identifies drop-offs, retention anomalies, and engagement drift.**

---

## Problem

Product teams need to know where users drop off in the journey and when engagement patterns suddenly change — but manual analysis is slow and inconsistent.

## Solution

A SQL + Python pipeline that models the full user funnel (visit → signup → activation → retention), computes conversion rates at each stage, and automatically flags anomalous behavior patterns.

---

## Features

- Full funnel modeling: visit → signup → activation → Day-7 retention
- Conversion rate computation at every stage
- Drop-off identification by stage and user segment
- Behavioral anomaly flags: users who activated but didn't retain, signed up but didn't activate
- Retention tier classification: HIGH DROP-OFF / MEDIUM / HEALTHY

---

## Fraud Analytics Connection

> This project focuses on behavioral anomaly detection — identifying when user behavior deviates from the expected journey pattern. This is directly analogous to how fraud detection systems flag when a customer's transaction behavior suddenly changes from their established baseline. The methodology is identical: define the normal journey, detect deviation, classify severity.

---

## Tech Stack

SQL · Python (Pandas) · Power BI · Excel

---

## Run It

```bash
pip install pandas
python analysis.py
```

---

*Author: Anoushka Rathore | [LinkedIn](https://linkedin.com/in/anoushka-rathore-452b22259) | [Blog](https://whereshadowsrest.wordpress.com)*