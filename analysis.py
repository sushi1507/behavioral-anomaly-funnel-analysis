"""
Behavioral Anomaly & Funnel Analysis
Author: Anoushka Rathore | github.com/sushi1507
"""

import pandas as pd

df = pd.read_csv("data/user_events.csv")

# Build funnel
funnel = df.groupby("user_id")["event"].apply(list).reset_index()
funnel.columns = ["user_id", "events"]

funnel["visited"]    = funnel["events"].apply(lambda x: int("visit" in x))
funnel["signed_up"]  = funnel["events"].apply(lambda x: int("signup" in x))
funnel["activated"]  = funnel["events"].apply(lambda x: int("activation" in x))
funnel["retained"]   = funnel["events"].apply(lambda x: int("retention_day7" in x))

# KPIs
total = len(funnel)
signups     = funnel["signed_up"].sum()
activations = funnel["activated"].sum()
retained    = funnel["retained"].sum()

print("=" * 50)
print("  BEHAVIORAL FUNNEL ANALYSIS REPORT")
print("=" * 50)
print(f"\nTotal Users:         {total}")
print(f"Visited:             {total}  (100%)")
print(f"Signed Up:           {signups}  ({signups/total*100:.0f}%)")
print(f"Activated:           {activations}  ({activations/total*100:.0f}%)")
print(f"Retained (Day 7):    {retained}  ({retained/total*100:.0f}%)")

print(f"\nDrop-off at signup:      {total - signups} users")
print(f"Drop-off at activation:  {signups - activations} users")
print(f"Drop-off at retention:   {activations - retained} users")

# Anomaly flags
funnel["anomaly_flag"] = funnel.apply(lambda r:
    "DROP-OFF: Activated not retained" if r["activated"] and not r["retained"]
    else ("DROP-OFF: Signed up not activated" if r["signed_up"] and not r["activated"]
    else "Normal"), axis=1)

print("\n--- ANOMALY FLAGS ---")
print(funnel["anomaly_flag"].value_counts().to_string())

funnel.to_csv("funnel_analysis_output.csv", index=False)
print("\n✓ Saved to funnel_analysis_output.csv")