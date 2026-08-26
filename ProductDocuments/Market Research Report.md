# Market Research Report

## Executive Summary

UK/EU customers lose an estimated **£15–20 a month** to subscriptions and bills they've forgotten about. On top of that, the balance shown in most banking apps doesn't account for money that's about to go out — so it looks safe to spend when it isn't. People get declined or overdrawn, then stop trusting the number on their home screen.

The **Safe-to-Spend Engine** fixes this by turning the raw balance into a number that already accounts for upcoming bills. For the Bank, this isn't just a nice-to-have: it cuts down one of the biggest reasons people contact support, and gives them a reason to check the app every day (which helps DAU — daily active users).

## User Pain Points

| Pain Point | Why it happens | Impact on the business |
| --- | --- | --- |
| Accidental overdraft or declined payment | The balance shown isn't the same as what's actually available to spend | More support tickets, churn, bad reviews |
| "Where did my money go?" anxiety | No visibility into bills that are about to come out | Less trust, less app engagement |
| Subscription fatigue | Recurring bills (Netflix, gym, rent) get lost among everyday spending | People forget what they've signed up for and overcommit |
| Reactive, not proactive, budgeting | Banking apps show what already happened, not what's coming | A missed chance to actually help people plan ahead |

**The core problem:** it's not that people lack data — they already see every transaction. What's missing is something that turns that history into a heads-up about what's coming.

## Competitor Benchmarking — Traditional vs. Neobanks

| Capability | Traditional Banks (Barclays, HSBC) | Other Neobanks (Monzo, Starling) | NeoBank (Current) |
| --- | --- | --- | --- |
| Shows real-time balance | ✅ Static only | ✅ Static, real-time | ✅ Static, real-time |
| Detects recurring bills | ❌ None | ⚠️ Manual "Bills Pots" (user sets these up) | ⚠️ Limited, not predictive |
| Shows a forward-looking safe balance | ❌ None | ❌ None (Monzo needs users to fund pots manually) | ❌ Gap identified |
| Forecasts upcoming bills automatically | ❌ None | ❌ None | **Opportunity: Safe-to-Spend Engine** |

**Key finding:** even Monzo and Starling still make users set up and fund their own "pots" — nobody does this automatically. Nobody in this space offers a zero-setup, forward-looking safe balance. This is a real gap, not a minor improvement.

## The Bank Business Case

**Why this matters:**

1. **Fewer support costs** — confusion about balances and overdrafts is one of the most common reasons people contact support across the industry. A Safe-to-Spend number answers that question before it's even asked.
2. **More daily engagement (DAU)** — a number that changes daily gives people a reason to open the app each morning, the same habit Monzo's Bills Pots already shows people want.
3. **More card spending (interchange revenue)** — when people trust they know what they can actually spend, they use their card more instead of holding back out of uncertainty.
4. **A reason to upgrade to premium** — this kind of forecasting is a natural premium feature, and puts the Bank ahead of Monzo/Starling's manual-pot approach.

**MVP scope:** all of this can be delivered with simple rule-based detection (spotting fixed-amount, fixed-interval payments) — no machine learning needed to prove it works, in line with the PoC scope already agreed.

---
