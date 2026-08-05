"""
Generate realistic multi-table raw data with intentional quality issues for Step 1
Demonstrates real-world data problems at scale
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent

# UK-specific data
UK_CITIES = ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Liverpool", 
             "Edinburgh", "Bristol", "Cardiff", "Newcastle", "Belfast", "Sheffield",
             "Leicester", "Nottingham", "Southampton", "Brighton", "Oxford", "Cambridge"]

COMPANY_TYPES = ["Ltd", "LLP", "PLC", "Limited", "& Co", "Associates", "Group"]
COMPANY_NAMES = ["ACME", "Global", "Premier", "Royal", "United", "British", "National",
                 "Enterprise", "Capital", "Sterling", "Crown", "Imperial", "Phoenix"]

FIRST_NAMES = ["John", "Sarah", "Michael", "Emma", "David", "James", "Robert", "Mary",
               "William", "Jennifer", "Richard", "Lisa", "Thomas", "Karen", "Charles",
               "Patricia", "Daniel", "Linda", "Matthew", "Elizabeth", "Andrew", "Susan"]

SURNAMES = ["Smith", "Jones", "Williams", "Brown", "Taylor", "Davies", "Evans", "Wilson",
            "Thomas", "Johnson", "Roberts", "Robinson", "Thompson", "White", "Hughes",
            "Edwards", "Green", "Lewis", "Wood", "Walker", "Hall", "Clarke", "Patel"]

CASE_TYPES = ["Conveyancing", "Employment", "Family", "Commercial", "IP", "Litigation",
              "Corp", "Property", "Dispute", "Contract", "Wills", "Immigration"]

SOLICITOR_NAMES = [
    "Sarah Jones", "Robert Smith", "Michael Brown", "Emma Wilson", "David Taylor",
    "James Davies", "Jennifer Thomas", "Richard Evans", "Lisa Johnson", "Andrew Roberts",
    "Susan Robinson", "Charles Thompson", "Patricia White", "Daniel Hughes", "Karen Edwards"
]

INTERACTION_TYPES = ["Call", "Email", "Meeting", "Letter", "Video", "Chat"]

# Intentionally vague/poor column names for raw data
def generate_raw_customers(num_customers=200):
    """Generate customers with data quality issues"""
    customers = []
    
    # Add some duplicates intentionally
    duplicate_base = []
    
    for i in range(num_customers):
        customer_id = i + 1
        
        # 10% chance of duplicate
        if random.random() < 0.1 and duplicate_base:
            # Create near-duplicate
            base = random.choice(duplicate_base)
            cust_name = base["n"]
            cust_type = base["typ"]
            city = base["loc"]
        else:
            # Generate new customer
            if random.random() < 0.6:  # 60% corporate
                cust_name = f"{random.choice(COMPANY_NAMES)} {random.choice(COMPANY_TYPES)}"
                cust_type = random.choice(["Corp", "Business", "Company", "Org", "C"])
            else:  # 40% individual
                cust_name = f"{random.choice(FIRST_NAMES)} {random.choice(SURNAMES)}"
                cust_type = random.choice(["Person", "Individual", "P", "Indiv", "Priv"])
            
            city = random.choice(UK_CITIES)
            
            # Store for potential duplication
            if len(duplicate_base) < 20:
                duplicate_base.append({"n": cust_name, "typ": cust_type, "loc": city})
        
        # Inconsistent date formats
        signup_date = datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1400))
        date_formats = [
            signup_date.strftime("%d/%m/%Y"),  # UK format
            signup_date.strftime("%m/%d/%Y"),  # US format
            signup_date.strftime("%Y-%m-%d"),  # ISO format
            signup_date.strftime("%d-%m-%y"),  # Short UK
            signup_date.strftime("%d.%m.%Y"),  # Dot format
        ]
        signup_str = random.choice(date_formats)
        
        # Inconsistent phone formats
        phone = random.randint(1000000000, 9999999999)
        phone_formats = [
            f"+44{phone}",
            f"0{phone}",
            f"+44 {phone}",
            f"0{phone // 10000000} {phone % 10000000}",
            f"({phone // 10000000}) {phone % 10000000}",
            str(phone),
        ]
        phone_str = random.choice(phone_formats)
        
        # Inconsistent status
        status = random.choice(["Active", "active", "ACTIVE", "Act", "A", "1", 
                               "Inactive", "inactive", "I", "0", "Suspended", "N/A", ""])
        
        # Some missing emails
        if random.random() < 0.15:  # 15% missing
            email = ""
        else:
            email_name = cust_name.lower().replace(" ", ".").replace("&", "and")
            email = f"{email_name}@example.co.uk"
        
        customers.append({
            "id": customer_id if random.random() > 0.05 else "",  # 5% missing IDs
            "n": cust_name,  # vague column name
            "typ": cust_type,  # vague abbreviation
            "loc": city,
            "dt": signup_str,  # vague abbreviation
            "ph": phone_str,
            "em": email,
            "stat": status,
            "col9": random.choice(["X", "Y", "", "N/A", "Unknown"]),  # mystery column
        })
    
    return customers


def generate_raw_cases(num_cases=500, num_customers=200):
    """Generate cases with data quality issues"""
    cases = []
    
    for i in range(num_cases):
        case_id = f"C{i+1:05d}" if random.random() > 0.08 else f"CASE{i+1}"  # Inconsistent ID format
        
        customer_id = random.randint(1, num_customers)
        solicitor = random.choice(SOLICITOR_NAMES)
        
        # Inconsistent case type naming
        case_type_base = random.choice(CASE_TYPES)
        case_type = random.choice([
            case_type_base,
            case_type_base.lower(),
            case_type_base.upper(),
            case_type_base[:4],  # Abbreviated
        ])
        
        # Random case value
        case_value = random.randint(5000, 500000)
        
        # Inconsistent value formats
        value_str = random.choice([
            str(case_value),
            f"£{case_value}",
            f"{case_value}.00",
            f"GBP {case_value}",
            str(case_value / 1000) + "K",  # 50K format
        ])
        
        # Inconsistent date formats
        start_date = datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1095))
        date_formats = [
            start_date.strftime("%d/%m/%Y"),
            start_date.strftime("%m/%d/%Y"),
            start_date.strftime("%Y-%m-%d"),
            start_date.strftime("%d-%m-%y"),
        ]
        start_str = random.choice(date_formats)
        
        # Case status inconsistency
        case_status = random.choice([
            "Open", "open", "OPEN", "Active", "Ongoing", "In Progress", "IP",
            "Closed", "closed", "CLOSED", "Complete", "Done", "Finished", "C",
            "Pending", "pending", "P", "On Hold", "Paused",
        ])
        
        cases.append({
            "cid": case_id,  # vague abbreviation
            "custid": customer_id,
            "sol": solicitor,  # vague abbreviation
            "typ": case_type,
            "val": value_str,
            "dt_start": start_str,
            "st": case_status,  # vague abbreviation
            "col8": random.choice(["", "X", "Y", "N/A"]),  # mystery column
        })
    
    return cases


def generate_raw_solicitors(num_solicitors=15):
    """Generate solicitor data with quality issues"""
    solicitors = []
    
    for i, name in enumerate(SOLICITOR_NAMES[:num_solicitors]):
        # Inconsistent ID format
        sol_id = f"SOL{i+1:03d}" if random.random() > 0.2 else f"S{i+1}"
        
        # Inconsistent specialization naming
        specialization = random.choice(CASE_TYPES)
        spec_str = random.choice([specialization, specialization.lower(), 
                                  specialization[:4], specialization.upper()])
        
        # Inconsistent hire date formats
        hire_date = datetime(2010, 1, 1) + timedelta(days=random.randint(0, 5000))
        hire_str = random.choice([
            hire_date.strftime("%d/%m/%Y"),
            hire_date.strftime("%Y-%m-%d"),
            hire_date.strftime("%m/%d/%Y"),
        ])
        
        # Inconsistent hourly rate formats
        hourly_rate = random.randint(150, 450)
        rate_str = random.choice([
            str(hourly_rate),
            f"£{hourly_rate}",
            f"{hourly_rate}.00",
            f"GBP{hourly_rate}",
        ])
        
        solicitors.append({
            "sid": sol_id,
            "nm": name,  # vague abbreviation
            "spec": spec_str,
            "hiredt": hire_str,
            "rate": rate_str,
            "loc": random.choice(UK_CITIES),
            "stat": random.choice(["Active", "active", "A", "1", "Employment"]),
        })
    
    return solicitors


def generate_raw_transactions(num_transactions=1000, num_cases=500):
    """Generate financial transactions with quality issues"""
    transactions = []
    
    for i in range(num_transactions):
        trans_id = f"T{i+1:06d}" if random.random() > 0.1 else f"TXN{i+1}"
        
        case_id_num = random.randint(1, num_cases)
        case_id = f"C{case_id_num:05d}" if random.random() > 0.2 else f"CASE{case_id_num}"
        
        # Transaction types with inconsistency
        trans_type = random.choice([
            "Timesheet", "timesheet", "TIME", "Hours", "Time",
            "Expense", "expense", "EXP", "Expenses", "E",
            "Invoice", "invoice", "INV", "Bill", "I",
            "Payment", "payment", "PAY", "Receipt", "P",
        ])
        
        # Transaction date
        trans_date = datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1095))
        trans_str = random.choice([
            trans_date.strftime("%d/%m/%Y"),
            trans_date.strftime("%Y-%m-%d"),
            trans_date.strftime("%m/%d/%Y"),
            trans_date.strftime("%d-%m-%y"),
        ])
        
        # Amount with inconsistent formatting
        amount = random.randint(50, 50000)
        amount_str = random.choice([
            str(amount),
            f"£{amount}",
            f"{amount}.00",
            f"GBP {amount}",
            str(amount / 1000) + "K" if amount > 10000 else str(amount),
        ])
        
        # Hours (for timesheet entries)
        hours = random.uniform(0.5, 40.0) if "time" in trans_type.lower() else 0
        hours_str = f"{hours:.1f}" if hours > 0 else ""
        
        # Payment status
        payment_status = random.choice([
            "Paid", "paid", "P", "1", "Complete",
            "Unpaid", "unpaid", "U", "0", "Pending",
            "Overdue", "overdue", "Late", "O",
            "", "N/A", "Unknown",
        ])
        
        transactions.append({
            "tid": trans_id,
            "cid": case_id,
            "typ": trans_type,
            "dt": trans_str,
            "amt": amount_str,
            "hrs": hours_str,
            "paystat": payment_status,
            "col8": random.choice(["", "X", "Y"]),
        })
    
    return transactions


def generate_raw_interactions(num_interactions=800, num_customers=200):
    """Generate customer interactions with quality issues"""
    interactions = []
    
    for i in range(num_interactions):
        int_id = f"INT{i+1:06d}" if random.random() > 0.15 else f"I{i+1}"
        
        customer_id = random.randint(1, num_customers)
        solicitor = random.choice(SOLICITOR_NAMES)
        
        # Interaction type inconsistency
        int_type_base = random.choice(INTERACTION_TYPES)
        int_type = random.choice([
            int_type_base,
            int_type_base.lower(),
            int_type_base.upper(),
            int_type_base[:3],
        ])
        
        # Interaction date
        int_date = datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1095))
        int_str = random.choice([
            int_date.strftime("%d/%m/%Y"),
            int_date.strftime("%Y-%m-%d"),
            int_date.strftime("%m/%d/%Y %H:%M"),
            int_date.strftime("%d-%m-%y"),
        ])
        
        # Duration in minutes
        duration = random.randint(5, 120)
        duration_str = random.choice([
            str(duration),
            f"{duration}m",
            f"{duration} mins",
            f"{duration/60:.1f}h" if duration > 60 else str(duration),
        ])
        
        # Notes - some missing
        if random.random() < 0.3:  # 30% missing
            notes = ""
        else:
            notes = random.choice([
                "Follow up required",
                "Client satisfied",
                "Needs clarification",
                "Urgent matter",
                "Routine check-in",
                "N/A",
                ".",
                "TBC",
            ])
        
        interactions.append({
            "iid": int_id,
            "cust": customer_id,
            "sol": solicitor,
            "typ": int_type,
            "dt": int_str,
            "dur": duration_str,
            "notes": notes,
            "col8": random.choice(["", "X"]),
        })
    
    return interactions


def write_csv(filename, data, fieldnames):
    """Write data to CSV file"""
    output_path = OUTPUT_DIR / filename
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"✓ Generated {output_path.name} with {len(data)} rows")


if __name__ == "__main__":
    print("Generating Step 1 raw data with intentional quality issues...\n")
    
    # Generate data
    customers = generate_raw_customers(200)
    cases = generate_raw_cases(500, 200)
    solicitors = generate_raw_solicitors(15)
    transactions = generate_raw_transactions(1000, 500)
    interactions = generate_raw_interactions(800, 200)
    
    # Write to CSV files
    write_csv("step1_raw_customers.csv", customers, 
              ["id", "n", "typ", "loc", "dt", "ph", "em", "stat", "col9"])
    
    write_csv("step1_raw_cases.csv", cases,
              ["cid", "custid", "sol", "typ", "val", "dt_start", "st", "col8"])
    
    write_csv("step1_raw_solicitors.csv", solicitors,
              ["sid", "nm", "spec", "hiredt", "rate", "loc", "stat"])
    
    write_csv("step1_raw_transactions.csv", transactions,
              ["tid", "cid", "typ", "dt", "amt", "hrs", "paystat", "col8"])
    
    write_csv("step1_raw_interactions.csv", interactions,
              ["iid", "cust", "sol", "typ", "dt", "dur", "notes", "col8"])
    
    print(f"\n{'='*60}")
    print("SUMMARY:")
    print(f"{'='*60}")
    print(f"Total Customers:     {len(customers):4d} (with ~10% duplicates)")
    print(f"Total Cases:         {len(cases):4d}")
    print(f"Total Solicitors:    {len(solicitors):4d}")
    print(f"Total Transactions:  {len(transactions):4d}")
    print(f"Total Interactions:  {len(interactions):4d}")
    print(f"{'='*60}")
    print(f"TOTAL RECORDS:       {len(customers)+len(cases)+len(solicitors)+len(transactions)+len(interactions):4d}")
    print(f"{'='*60}\n")
    
    print("Data quality issues included:")
    print("  ✓ Vague column names (n, typ, sol, dt, etc.)")
    print("  ✓ Inconsistent date formats (DD/MM/YYYY, MM/DD/YYYY, ISO)")
    print("  ✓ Inconsistent phone formats")
    print("  ✓ Duplicate customer records (~10%)")
    print("  ✓ Inconsistent status values (Active/active/A/1)")
    print("  ✓ Inconsistent case type naming")
    print("  ✓ Mixed currency formats (£, GBP, plain numbers)")
    print("  ✓ Mystery columns (col8, col9)")
    print("  ✓ Missing data (15% missing emails, 30% missing notes)")
    print("  ✓ Inconsistent ID formats")
    print("  ✓ No proper foreign key relationships")
