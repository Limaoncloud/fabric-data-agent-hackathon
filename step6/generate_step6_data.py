"""
Generate Step 6 derived datasets for multi-source routing demos.
Creates additional data sources from Step 1 cleaned tables.
"""

import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STEP1_DIR = BASE_DIR.parent / "step1"


def parse_uk_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value.strip(), "%d/%m/%Y")
    except ValueError:
        return None


def load_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_engagement_summary(customers, interactions):
    grouped = defaultdict(list)
    for row in interactions:
        try:
            cid = int(row.get("customer_id", "0"))
        except ValueError:
            continue
        grouped[cid].append(row)

    rows = []
    for cust in customers:
        cid = int(cust["customer_id"])
        logs = grouped.get(cid, [])

        if logs:
            durations = [int(r.get("duration_minutes", "0") or 0) for r in logs]
            total_interactions = len(logs)
            avg_duration = round(sum(durations) / total_interactions, 2)
            typ_counter = Counter(r.get("interaction_type", "Other") or "Other" for r in logs)
            dominant_type = typ_counter.most_common(1)[0][0]
            dt_values = [parse_uk_date(r.get("interaction_date", "")) for r in logs]
            dt_values = [d for d in dt_values if d]
            last_date = max(dt_values).strftime("%d/%m/%Y") if dt_values else ""
        else:
            total_interactions = 0
            avg_duration = 0
            dominant_type = "None"
            last_date = ""

        if total_interactions >= 10:
            segment = "High Engagement"
        elif total_interactions >= 4:
            segment = "Medium Engagement"
        else:
            segment = "Low Engagement"

        rows.append(
            {
                "customer_id": cid,
                "customer_name": cust["customer_name"],
                "customer_type": cust["customer_type"],
                "customer_status": cust["status"],
                "total_interactions": total_interactions,
                "last_interaction_date": last_date,
                "avg_interaction_duration_minutes": avg_duration,
                "dominant_interaction_type": dominant_type,
                "engagement_segment": segment,
            }
        )

    rows.sort(key=lambda r: r["customer_id"])
    return rows


def create_case_finance_insights(cases, transactions):
    tx_by_case = defaultdict(list)
    for tx in transactions:
        case_id = tx.get("case_id", "")
        if case_id:
            tx_by_case[case_id].append(tx)

    rows = []
    for c in cases:
        case_id = c["case_id"]
        txs = tx_by_case.get(case_id, [])

        timesheet_amount = 0.0
        expense_amount = 0.0
        invoice_amount = 0.0
        payment_amount = 0.0
        total_hours = 0.0

        for tx in txs:
            ttype = (tx.get("transaction_type", "") or "").strip()
            amount = float(tx.get("amount_gbp", "0") or 0)
            hrs = float(tx.get("hours_worked", "0") or 0)

            if ttype == "Timesheet":
                timesheet_amount += amount
                total_hours += hrs
            elif ttype == "Expense":
                expense_amount += amount
            elif ttype == "Invoice":
                invoice_amount += amount
            elif ttype == "Payment":
                payment_amount += amount

        if invoice_amount <= 0:
            invoice_amount = timesheet_amount + expense_amount

        outstanding = round(max(0.0, invoice_amount - payment_amount), 2)

        if outstanding >= 100000:
            risk_band = "High"
        elif outstanding >= 25000:
            risk_band = "Medium"
        else:
            risk_band = "Low"

        rows.append(
            {
                "case_id": case_id,
                "customer_id": c["customer_id"],
                "solicitor_name": c["solicitor_name"],
                "case_type": c["case_type"],
                "case_status": c["case_status"],
                "case_value_gbp": float(c["case_value_gbp"]),
                "total_timesheet_amount_gbp": round(timesheet_amount, 2),
                "total_expense_amount_gbp": round(expense_amount, 2),
                "total_invoice_amount_gbp": round(invoice_amount, 2),
                "total_payment_amount_gbp": round(payment_amount, 2),
                "total_hours_billed": round(total_hours, 2),
                "outstanding_amount_gbp": outstanding,
                "payment_risk_band": risk_band,
            }
        )

    rows.sort(key=lambda r: r["case_id"])
    return rows


def create_solicitor_performance_mart(cases, transactions, interactions):
    case_by_sol = defaultdict(list)
    for c in cases:
        case_by_sol[c["solicitor_name"]].append(c)

    tx_by_sol = defaultdict(list)
    for tx in transactions:
        # transactions don't always include solicitor; infer from case when not present in source schema
        tx_by_sol[tx.get("case_id", "")].append(tx)

    # Build case -> solicitor map
    case_to_sol = {c["case_id"]: c["solicitor_name"] for c in cases}

    metrics = defaultdict(lambda: {
        "cases_handled": 0,
        "open_cases": 0,
        "total_case_value_gbp": 0.0,
        "total_hours_billed": 0.0,
        "total_invoice_amount_gbp": 0.0,
        "total_payment_amount_gbp": 0.0,
        "total_interactions": 0,
        "total_interaction_duration": 0.0,
    })

    for sol, sol_cases in case_by_sol.items():
        m = metrics[sol]
        m["cases_handled"] = len(sol_cases)
        m["open_cases"] = sum(1 for c in sol_cases if c.get("case_status") == "Open")
        m["total_case_value_gbp"] = sum(float(c.get("case_value_gbp", "0") or 0) for c in sol_cases)

    for tx in transactions:
        case_id = tx.get("case_id", "")
        sol = case_to_sol.get(case_id)
        if not sol:
            continue
        m = metrics[sol]
        ttype = (tx.get("transaction_type", "") or "").strip()
        amount = float(tx.get("amount_gbp", "0") or 0)
        hrs = float(tx.get("hours_worked", "0") or 0)

        if ttype == "Timesheet":
            m["total_hours_billed"] += hrs
        elif ttype == "Invoice":
            m["total_invoice_amount_gbp"] += amount
        elif ttype == "Payment":
            m["total_payment_amount_gbp"] += amount

    for inter in interactions:
        sol = inter.get("solicitor_name", "")
        if not sol:
            continue
        m = metrics[sol]
        m["total_interactions"] += 1
        m["total_interaction_duration"] += float(inter.get("duration_minutes", "0") or 0)

    rows = []
    for sol, m in metrics.items():
        cases_handled = m["cases_handled"]
        total_case_value = m["total_case_value_gbp"]

        if cases_handled >= 40 or total_case_value >= 8000000:
            tier = "Top"
        elif cases_handled >= 20 or total_case_value >= 3000000:
            tier = "Strong"
        else:
            tier = "Developing"

        avg_duration = round(
            m["total_interaction_duration"] / m["total_interactions"], 2
        ) if m["total_interactions"] else 0.0

        rows.append(
            {
                "solicitor_name": sol,
                "cases_handled": cases_handled,
                "open_cases": m["open_cases"],
                "total_case_value_gbp": round(total_case_value, 2),
                "total_hours_billed": round(m["total_hours_billed"], 2),
                "total_invoice_amount_gbp": round(m["total_invoice_amount_gbp"], 2),
                "total_payment_amount_gbp": round(m["total_payment_amount_gbp"], 2),
                "total_interactions": m["total_interactions"],
                "avg_interaction_duration_minutes": avg_duration,
                "performance_tier": tier,
            }
        )

    rows.sort(key=lambda r: r["solicitor_name"])
    return rows


def main():
    customers = load_csv(STEP1_DIR / "step1_cleaned_customers.csv")
    cases = load_csv(STEP1_DIR / "step1_cleaned_cases.csv")
    transactions = load_csv(STEP1_DIR / "step1_cleaned_transactions.csv")
    interactions = load_csv(STEP1_DIR / "step1_cleaned_interactions.csv")

    engagement_rows = create_engagement_summary(customers, interactions)
    case_finance_rows = create_case_finance_insights(cases, transactions)
    solicitor_perf_rows = create_solicitor_performance_mart(cases, transactions, interactions)

    write_csv(
        BASE_DIR / "step6_client_engagement_summary.csv",
        [
            "customer_id",
            "customer_name",
            "customer_type",
            "customer_status",
            "total_interactions",
            "last_interaction_date",
            "avg_interaction_duration_minutes",
            "dominant_interaction_type",
            "engagement_segment",
        ],
        engagement_rows,
    )

    write_csv(
        BASE_DIR / "step6_case_finance_insights.csv",
        [
            "case_id",
            "customer_id",
            "solicitor_name",
            "case_type",
            "case_status",
            "case_value_gbp",
            "total_timesheet_amount_gbp",
            "total_expense_amount_gbp",
            "total_invoice_amount_gbp",
            "total_payment_amount_gbp",
            "total_hours_billed",
            "outstanding_amount_gbp",
            "payment_risk_band",
        ],
        case_finance_rows,
    )

    write_csv(
        BASE_DIR / "step6_solicitor_performance_mart.csv",
        [
            "solicitor_name",
            "cases_handled",
            "open_cases",
            "total_case_value_gbp",
            "total_hours_billed",
            "total_invoice_amount_gbp",
            "total_payment_amount_gbp",
            "total_interactions",
            "avg_interaction_duration_minutes",
            "performance_tier",
        ],
        solicitor_perf_rows,
    )

    print("Generated Step 6 datasets:")
    print(f"- step6_client_engagement_summary.csv ({len(engagement_rows)} rows)")
    print(f"- step6_case_finance_insights.csv ({len(case_finance_rows)} rows)")
    print(f"- step6_solicitor_performance_mart.csv ({len(solicitor_perf_rows)} rows)")


if __name__ == "__main__":
    main()
