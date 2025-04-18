import sys
import csv

def parse_currency(value):
    
    #converts a monetary string into a float - negative values wrapped in parentheses become negative numbers
    
    value = value.strip().replace('$', '').replace(',', '')
    if value.startswith('(') and value.endswith(')'):
        value = '-' + value[1:-1]
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Cannot parse value: {value}")

def sum_expenses_by_params(rows, department=None, year=None, quarter=None, month=None):
    """
        Sums up expenses:
        - department
        - year
        - quarter
        - month - month name
    """
    quarter_mapping = {
        1: ['Jan', 'Feb', 'Mar'],
        2: ['Apr', 'May', 'Jun'],
        3: ['Jul', 'Aug', 'Sep'],
        4: ['Oct', 'Nov', 'Dec'],
    }
    month_mapping = {
        "jan": "Jan", "january": "Jan",
        "feb": "Feb", "february": "Feb",
        "mar": "Mar", "march": "Mar",
        "apr": "Apr", "april": "Apr",
        "may": "May",
        "jun": "Jun", "june": "Jun",
        "jul": "Jul", "july": "Jul",
        "aug": "Aug", "august": "Aug",
        "sep": "Sep", "september": "Sep",
        "oct": "Oct", "october": "Oct",
        "nov": "Nov", "november": "Nov",
        "dec": "Dec", "december": "Dec"
    }

    total = 0.0
    for row in rows:
        #remove whitespace
        row = {k.strip().lstrip('\ufeff'): v for k, v in row.items()}

        try:
            csv_dept = row['Department']
        except KeyError:
            raise KeyError("CSV header missing 'Department' column.")
        csv_year = row.get('Year')

        if department and department.lower() != csv_dept.lower():
            continue
        if year and str(year) != str(csv_year):
            continue

        if quarter is not None:
            months = quarter_mapping.get(quarter, [])
            for m in months:
                if m in row:
                    total += parse_currency(row[m])
            continue

        if month is not None:
            key = month.strip().lower()
            month_key = month_mapping.get(key)
            if not month_key:
                raise ValueError(f"Invalid month name: {month}")
            if month_key in row:
                total += parse_currency(row[month_key])
            continue

        #no quarter/month filter - sum all months
        for m in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']:
            if m in row:
                total += parse_currency(row[m])

    return total

def main():
    args = sys.argv[1:]
    reader = csv.DictReader(sys.stdin, delimiter=';')
    rows = list(reader)

    if len(args) == 1:
        dept = args[0]
        total = sum_expenses_by_params(rows, department=dept)
    elif len(args) == 2:
        dept, yr = args
        total = sum_expenses_by_params(rows, department=dept, year=yr)
    elif len(args) == 3:
        dept, yr, thr = args
        #numeric only for quarters
        try:
            q = int(thr)
        except ValueError:
            total = sum_expenses_by_params(rows, department=dept, year=yr, month=thr)
        else:
            if 1 <= q <= 4:
                total = sum_expenses_by_params(rows, department=dept, year=yr, quarter=q)
            else:
                print(f"Error: numeric argument '{thr}' invalid—only 1–4 allowed for quarters.")
                sys.exit(1)
    else:
        print("Usage:")
        print("  cat Expenses.csv | python3 expenses.py <department>")
        print("  cat Expenses.csv | python3 expenses.py <department> <year>")
        print("  cat Expenses.csv | python3 expenses.py <department> <year> <quarter>")
        print("  cat Expenses.csv | python3 expenses.py <department> <year> <month_name>")
        sys.exit(1)

    print(f"{total:.2f} USD")

if __name__ == "__main__":
    main()
