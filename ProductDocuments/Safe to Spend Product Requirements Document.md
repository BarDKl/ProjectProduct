# Safe to Spend Product Requirements Document

| Title/Initiative | Safe-to-Spend Engine |
| --- | --- |
| Date & Version | 14.08.2026 v0.1 (Initial) |
| Point of Contact | Bartosz DK |
| Product Deadline | Start of Q4 2026 |

## 1. Why? (Objective)

Bank users frequently experience **"subscription fatigue"** — a state in which accumulated recurring payments (rent, streaming, gym, software) become untracked, leaving the user with an inaccurate mental model of how much money is actually theirs to spend. The static ledger balance shown by nearly every banking app today does not distinguish between funds that are genuinely free to spend and funds already earmarked for near-term liabilities.

**Why this matters to two audiences:**

1. **For the bank:** Uncertainty around upcoming liabilities drives defensive behaviour — users hoard cash "just in case," which suppresses card spend (and therefore interchange revenue), and drives a high volume of avoidable "Where did my money go?" support contacts when the model breaks down (overdrafts, declines).
2. **For the user:** A clear, forward-looking number reduces financial anxiety, restores a sense of control, and supports mindful, confident spending decisions — directly addressing the Jobs to Be Done in Section 4.

## 2. How Do We Measure Success?

**Associated OKR**

> **Objective:** Reduce financial anxiety and increase confidence in spending decisions.
> 

> **Key Results:**
> 

> 1. Achieve 30% adoption of Safe-to-Spend (StS) among active users.
> 

> 2. Reduce insufficient-funds (IF) errors by 25%.
> 

> 3. Increase daily card transaction volume by 15% among users actively using the feature.
> 

**Success Metrics**

| Metric | Definition |
| --- | --- |
| StS Adoption Rate | Users viewing the Safe-to-Spend card ÷ Active users |
| IF Error Reduction | (IF errors per user, Q4 2026) ÷ average of (IF errors per user, Q3 2026) and (IF errors per user, Q4 2025). Q4-over-Q4 comparison controls for seasonality (e.g. holiday spending); Q3 2026 is included for recency of app version and user base despite seasonal noise. |
| Spend Confidence Lift | Avg. daily transactions (Q4 2026, active StS users) ÷ Avg. daily transactions (Q4 2026, active users without StS) |

**Guardrail / "Do Not Disturb" Metrics**

| Guardrail | Threshold |
| --- | --- |
| System health — API uptime | ≥ 99.9% |
| Data accuracy — recurring-transaction false-positive rate | < 2% |
| Privacy — data leaks or regulatory violations | Zero tolerance |

## 3. Who Are the Users?

**Persona 1 — Agnieszka (Primary: high-anxiety, low financial literacy)**

| Age | 20 |
| --- | --- |
| Net income/month | 3,000 zł (parental support) |
| Location | Wrocław, Poland |
| Occupation | Student |
| Active subscriptions | 6 — Netflix, HBO Max, Disney+, Spotify Premium, Player, YouTube Premium |
| Spending pattern | Impulsive spender |
| Financial literacy | Low — no independent income, limited spending caution |
| Key behaviour | Checks balance ~3x/day; uses the app for travel, daily expenses, online shopping |
| Biggest anxiety | Not having enough money to make it to the end of the month |

> *"I don't have a lot of money to spend, but I love to watch movies and relax listening to some music — I don't want to sacrifice it, but I'm anxious that I might have to, given my spending habits."*
> 

**Persona 2 — Kuba (Secondary: early-career, moderate spender)**

| Age | 23 |
| --- | --- |
| Net income/month | 5,000 zł |
| Location | Kraków, Poland |
| Occupation | Junior UI Designer |
| Active subscriptions | Claude Code, Gemini Pro, Netflix, YouTube Premium |
| Spending pattern | Moderate spender |
| Financial literacy | Medium — early professional, first full-time job |
| Key behaviour | Checks balance ~once every 2 days |

**Broader Segment:** Young, financially inexperienced people in their first or second job — students and early-career adults — who share a common feeling of losing track of committed vs. free-to-spend funds, regardless of income level.

## 4. Problems We Are Solving (Jobs to Be Done)

1. **When** I check my balance before making a purchase, **I want to** know what's truly safe to spend after upcoming bills are accounted for, **so I can** spend with confidence instead of guessing.
2. **When** a subscription or fixed bill is about to be charged, **I want** the app to have already reserved that amount from my visible balance, **so I** don't get declined or overdrawn.
3. **When** I have low financial literacy or no time/inclination to budget manually, **I want** recurring liabilities detected automatically, **so I** don't have to configure pots, categories, or rules myself.
4. **When** I'm anxious about spending, **I want** a single trustworthy number, **so I** stop over-saving defensively and can spend mindfully instead.

## 5. How Do We Know These Problems Exist? (Research)

Findings are detailed in the companion [Market Research Report](https://app.notion.com/p/Market-Research-Report-3ba32be71aab80e2a209de22783f458c?pvs=21). Key evidence:

- UK/EU consumers carry an estimated **£15–20/month in "silent" subscription leakage** (industry estimates), compounded by static ledger balances that misrepresent true spending power.
- Competitor benchmarking (Barclays, HSBC, Monzo, Starling) shows **no major player offers automated, zero-setup, forward-looking liability forecasting** — existing solutions (e.g. Monzo/Starling "Bills Pots") rely on manual user configuration. This is a genuine white space, not an incremental feature.
- The core insight from research: the pain point isn't a lack of transaction data — it's a lack of **interpretation**. Users already generate the signal; no system currently converts it into a forward-looking number.
- "Balance confusion" and overdraft-related queries are established as a recurring, high-volume support category industry-wide, directly linking this problem to support cost (a Bank KPI).

## 6. Solution

**Solution Brief**

The Safe-to-Spend Engine is a backend predictive API microservice (Python 3.12 / FastAPI, containerized with Docker) that:

1. Ingests a user's transaction history (mocked via the `Faker` library for this PoC, structured to resemble real Open Banking transaction data).
2. Applies **deterministic rules** to detect recurring liabilities: transactions matching a fixed interval (e.g. every 28–31 days) within a tolerance window, and a fixed amount within a tolerance percentage.
3. Projects detected liabilities forward across a **rolling 14-day window**.
4. Returns a `safe_to_spend` figure = current ledger balance − sum of liabilities due within the window, via a single REST endpoint.

**Alternatives Considered**

| Alternative | Description | Why Not Selected for MVP |
| --- | --- | --- |
| ML-based forecasting (e.g. time-series models) | Learn spending/recurrence patterns statistically | Adds training-data and retraining infrastructure not justified to validate the core hypothesis; explicitly excluded by MVP scope constraints |
| Manual user-configured "Bills Pots" (Monzo/Starling model) | User manually tags and funds recurring bills | Proven demand, but requires setup effort and doesn't solve the "forgetting" problem — this is the status quo, not a differentiator |
| Third-party Open Banking aggregator categorization (e.g. Plaid, TrueLayer) | Rely on external providers' transaction categorization/tags | Dependent on external data quality; real Open Banking API integration is explicitly out of scope for this PoC |

**Selected approach:** deterministic rule-based detection — zero setup for the user, fully explainable/auditable output, and testable without ML infrastructure, in direct alignment with the defined MVP constraints.

## 7. Product Flow (Details of the Feature/Product)

**System Flow (Backend PoC)**

1. Client (mobile app / API consumer) requests `GET /safe-to-spend` for a user.
2. Service pulls the user's mock transaction history.
3. Recurring-liability detector scans history for fixed-interval, fixed-amount patterns.
4. Liabilities falling within the next 14 days are summed.
5. Service returns: current balance, safe-to-spend balance, and the list of upcoming liabilities driving the deduction (for transparency).

*Note: Front-end wireframes/mockups for surfacing this data in-app are owned by the Design team and are tracked as an open dependency (Section 8) — out of scope for this backend PoC.*

**User Stories & Acceptance Criteria**

| ID | User Story | Acceptance Criteria |
| --- | --- | --- |
| US-1 | As a user, I want to see a Safe-to-Spend balance instead of just my raw balance, so I know what I can actually spend. | Given a user with ≥1 detected recurring liability, when they request their balance, then the API returns a `safe_to_spend` value lower than the raw ledger balance by the sum of liabilities due in the next 14 days. |
| US-2 | As a user, I want recurring bills detected automatically, so I don't have to configure anything manually. | Given ≥2 historical transactions to the same payee at the exact same amount and at a consistent interval (each gap within ±4 days of the average gap), when the detector runs, then that payee is classified as a recurring liability. Amount is matched exactly — variable-amount bills (e.g. utilities) are not yet detected (see Edge Cases below). |
| US-3 | As a user, I want to understand why my Safe-to-Spend number is lower than my balance, so I trust the figure. | Given a non-zero deduction, when the API responds, then the response includes the itemized list of upcoming liabilities (payee, amount, expected date) that make up the deduction. |

**Edge Cases**

- New user with insufficient transaction history to establish a recurring pattern (< 2 occurrences).
- Recurring bill with a variable amount (e.g. utilities) — not yet handled; detection currently requires an exact amount match, so amount drift breaks grouping entirely (no tolerance band implemented). Backlog item.
- Subscription cancelled by the user but still appearing in historical data.
- Liability due exactly on day 14 (boundary condition of the rolling window).
- Payee name inconsistency across transactions (e.g. "[NETFLIX.COM](http://NETFLIX.COM)" vs "Netflix").
- False positive: a coincidentally regular one-off spending pattern misclassified as recurring.

**Event Tracking Sheet**

| Event | Trigger | Key Properties | Supports Metric |
| --- | --- | --- | --- |
| `sts_card_viewed` | User views the Safe-to-Spend card in-app | user_id, sts_value, raw_balance | StS Adoption Rate |
| `sts_breakdown_expanded` | User taps to see itemized liabilities | user_id, liability_count | Engagement / trust in feature |
| `if_error_occurred` | Insufficient-funds error on a transaction | user_id, had_sts_enabled, amount | IF Error Reduction |
| `card_transaction_completed` | Successful card transaction | user_id, had_sts_enabled, amount | Spend Confidence Lift |

## 8. Dependencies

- **Open Questions:** Should Safe-to-Spend be opt-in or default-on at launch? How are multi-currency wallets (a Bank-specific case) handled in the deduction logic?
- **Infrastructure requirements:** None beyond the containerized microservice itself for the PoC — no production data pipeline required at this stage.
- **Budget approvals:** N/A for PoC (portfolio project, no real infra spend); would require standard cloud-hosting approval if progressed toward pilot.
- **Partner support (APIs, partnerships):** None for MVP — real Open Banking integration is explicitly deferred beyond this PoC.
- **Internal dependencies:** Design team for front-end wireframes/UI surfacing; Data/Analytics for event tracking implementation; Legal/Compliance review before any real transaction data is used.

## 9. Related Documents

1. [Market Research Report](https://app.notion.com/p/Market-Research-Report-3ba32be71aab80e2a209de22783f458c?pvs=21) ✅ Complete
2. [MVP Scope](./MVP%20Scope.md) ✅ Complete