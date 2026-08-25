# Market Research Report

## Executive Summary

UK/EU consumers hold **£15–20 avg/month in "silent" subscription leakage** (industry estimates), compounded by static ledger balances that misrepresent true spending power. This creates a systemic trust gap: users see a number that says "safe," then get declined or overdrawn. The **Safe-to-Spend Engine** targets this gap directly — converting raw ledger balance into a forward-looking, liability-adjusted figure. For the Bank, this is a **retention and engagement lever**, not a cosmetic feature: it reduces the #1 driver of reactive support contacts and increases the reason to open the app daily (DAU).

## User Pain Points

| Pain Point | Root Cause | Business Impact |
| --- | --- | --- |
| Accidental overdraft/decline | Static balance ≠ available balance | Support tickets, churn, negative reviews |
| "Where did my money go?" anxiety | No visibility into upcoming fixed liabilities | Reduced trust, lower app engagement |
| Subscription fatigue | Recurring bills (Netflix, gym, rent) blend into noise of daily spend | Users forget commitments, over-leverage themselves |
| Reactive, not proactive, budgeting | Bank apps show history, not forecast | Missed opportunity for proactive financial guidance |

**Core insight:** the pain isn't a lack of data — it's a lack of *interpretation*. Users already have the transaction history; they lack a system that turns it into a forward-looking signal.

## Competitor Benchmarking — Traditional vs. Neobanks

| Capability | Traditional Banks (Barclays, HSBC) | Other Neobanks (Monzo, Starling) | NeoBank (Current) |
| --- | --- | --- | --- |
| Ledger balance display | ✅ Static only | ✅ Static, real-time | ✅ Static, real-time |
| Recurring bill detection | ❌ None | ⚠️ Manual "Bills Pots" (user-configured) | ⚠️ Limited, not predictive |
| Forward-looking safe balance | ❌ None | ❌ None (Monzo requires manual pot funding) | ❌ Gap identified |
| Automated liability forecasting | ❌ None | ❌ None | **Opportunity: Safe-to-Spend Engine** |

**Key finding:** Even leading neobanks rely on **user-configured** pots/rules rather than **deterministic auto-detection**. No major player in this benchmark set offers an automated, zero-setup forward liability forecast — this is a genuine white space, not an incremental feature.

## The Bank Business Case

**Why this matters to Bank's KPIs:**

1. **Support cost reduction** — "Balance confusion" and overdraft-related queries are a recurring high-volume support category industry-wide. A proactive Safe-to-Spend indicator intercepts the query before it's asked.
2. **DAU / engagement** — A daily-relevant number (vs. a static balance checked reactively) gives users a reason to open the app each morning, reinforcing habit loops that competitor "Bills Pots" already prove has demand.
3. **Interchange revenue** — Users confident in their *true* spending power spend with more (not less) frequency on their card, rather than hoarding cash out of uncertainty.
4. **Premium tier differentiation** — Predictive financial certainty is a natural upsell for the Bank's premium tier, positioning it ahead of Monzo/Starling's manual-pot model.

**MVP scope alignment:** This business case is served entirely by deterministic rule-based detection (fixed-interval, fixed-amount recurring transactions) — no ML required to prove the value hypothesis, consistent with the defined PoC constraints.

---

*Prepared as part of the Safe-to-Spend Engine portfolio project — Fintech Product Owner workstream.*