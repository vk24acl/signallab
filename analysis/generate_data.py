"""SignalLab reproducible synthetic cohort generator. Python 3, standard library.

This is a portfolio simulation, not Axtria, Lovable, or client data.
Run from the project root: python3 analysis/generate_data.py
"""
from __future__ import annotations
import csv
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = 43121
CHANNELS = [
    ("Google · Brand", "Paid search"), ("Google · Non-brand", "Paid search"),
    ("Google · Competitor", "Paid search"), ("Bing · Brand", "Paid search"),
    ("Bing · Non-brand", "Paid search"), ("Google · Retargeting", "Paid search"),
    ("Meta · Founders", "Paid social"), ("Meta · Small business", "Paid social"),
    ("LinkedIn · Product", "Paid social"), ("LinkedIn · Operations", "Paid social"),
    ("Reddit · Developers", "Paid social"), ("Reddit · Entrepreneurs", "Paid social"),
    ("YouTube · Tutorials", "Paid social"), ("YouTube · Creators", "Paid social"),
    ("TikTok · Builders", "Paid social"), ("X · Makers", "Paid social"),
    ("SEO · How-to guides", "Organic content"), ("SEO · Templates", "Organic content"),
    ("SEO · Comparisons", "Organic content"), ("SEO · Use cases", "Organic content"),
    ("Blog · Product", "Organic content"), ("Blog · Customer stories", "Organic content"),
    ("Newsletter · Weekly", "Email"), ("Email · Re-engagement", "Email"),
    ("Email · Product launch", "Email"), ("Email · Lifecycle", "Email"),
    ("Partner · Agencies", "Partners"), ("Partner · Accelerators", "Partners"),
    ("Partner · Universities", "Partners"), ("Partner · Integrations", "Partners"),
    ("Partner · Affiliates", "Partners"), ("Community · Discord", "Community"),
    ("Community · Reddit", "Community"), ("Community · Meetups", "Community"),
    ("Community · Hackathons", "Community"), ("Community · Product Hunt", "Community"),
    ("Referral · Customers", "Referral"), ("Referral · Creators", "Referral"),
    ("Referral · Teams", "Referral"), ("Direct · Website", "Direct"),
    ("Direct · Bookmarks", "Direct"), ("Direct · Word of mouth", "Direct"),
    ("Direct · Unattributed", "Direct"),
]

def generate():
    rng = random.Random(SEED)
    channels = []
    for i, (name, group) in enumerate(CHANNELS):
        paid = group in ("Paid search", "Paid social")
        weight = rng.uniform(.45, 1.8) * (1.4 if group == "Direct" else 1)
        activation = rng.uniform(.27, .53) + (.04 if group in ("Referral", "Email") else 0)
        channels.append(dict(id=i, name=name, group=group, paid=paid,
            weight=round(weight, 5), activation=round(activation, 5),
            unitCost=round(rng.uniform(9, 31) if paid else rng.uniform(1.5, 7.5), 2)))
    users, costs = [], []
    for week in range(12):
        counts = [0] * 43
        weekly_size = int(1750 + 83 * week + rng.uniform(-110, 110))
        for _ in range(weekly_size):
            channel = rng.choices(channels, weights=[c["weight"] for c in channels])[0]
            counts[channel["id"]] += 1
            arm = (1 if rng.random() < .5 else 2) if week < 4 else 0
            started = rng.random() < .82
            p = channel["activation"] + .004 * week + (.035 if arm == 2 else 0)
            activated = started and rng.random() < p / .82
            published = activated and rng.random() < .60 + .006 * week
            mask = 1
            # Activity in week k is point retention, not survival; users may return.
            for k in range(1, 12 - week):
                q = (.65 if activated else .12) * .90 ** (k - 1)
                if rng.random() < q:
                    mask |= 1 << k
            good_session = started and rng.random() < (.945 if arm == 2 else .94)
            users.append([len(users) + 1, week, channel["id"], int(started),
                int(activated), int(published), mask, arm, int(good_session)])
        for channel in channels:
            # Recorded acquisition cost includes allocated content/labour for non-paid.
            spend = round(counts[channel["id"]] * channel["unitCost"] * rng.uniform(.90, 1.10), 2)
            costs.append([week, channel["id"], spend])
    return dict(seed=SEED, asOf="2026-10-19", startDate="2026-07-20",
        rows=users, channels=channels, costs=costs,
        fields=["user_id", "signup_week", "channel_id", "started", "activated_7d",
                "published_7d", "active_week_mask", "experiment_arm", "error_free_session"],
        experiment=dict(name="Guided first project", start="2026-07-20", end="2026-08-16",
            baseline=.40, relativeMDE=.10, alpha=.05, power=.80,
            guardrailMargin=.02, randomisation="User-level 50:50; first four signup cohorts"))

def experiment(data):
    arms = [[r for r in data["rows"] if r[7] == a] for a in (1, 2)]
    n1, n2 = map(len, arms)
    x1, x2 = [sum(r[4] for r in a) for a in arms]
    p1, p2 = x1/n1, x2/n2
    pooled = (x1+x2)/(n1+n2)
    z = (p2-p1)/math.sqrt(pooled*(1-pooled)*(1/n1+1/n2))
    return dict(n_control=n1, n_variant=n2, activated_control=x1, activated_variant=x2,
                p_control=p1, p_variant=p2, absolute_lift=p2-p1,
                relative_lift=p2/p1-1, two_sided_p=math.erfc(abs(z)/math.sqrt(2)))

def main():
    data=generate()
    assert len(data["channels"]) == 43
    assert len({r[0] for r in data["rows"]}) == len(data["rows"])
    assert all(r[5] <= r[4] <= r[3] for r in data["rows"])
    assert all(r[6] < (1 << (12-r[1])) for r in data["rows"])
    (ROOT/"dist").mkdir(exist_ok=True)
    (ROOT/"dist"/"data.json").write_text(json.dumps(data,separators=(",",":")))
    with (ROOT/"analysis"/"users.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(data["fields"]);w.writerows(data["rows"])
    with (ROOT/"analysis"/"channel_costs.csv").open("w",newline="") as f:
        w=csv.writer(f);w.writerow(["signup_week","channel_id","acquisition_cost_gbp"]);w.writerows(data["costs"])
    summary=dict(users=len(data["rows"]),channels=43,activation=sum(r[4] for r in data["rows"])/len(data["rows"]),experiment=experiment(data))
    (ROOT/"analysis"/"expected_results.json").write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__ == "__main__": main()
