from fastapi import FastAPI, HTTPException, Request, Query
import io, csv
from expenses import sum_expenses_by_params

app = FastAPI()

@app.post("/aggregate")
async def aggregate(
    request: Request,
    department: str = Query(..., description="Department name e.g. 'Sales'."),
    year: int = Query(None, description="Year e.g. 2020."),
    quarter: int = Query(None, description="Quarter number (1-4)."),
    month: str = Query(None, description="Month name e.g. January. Numeric months not supported.")
):
    
    body = await request.body()
    content_type = request.headers.get("content-type", "")

    
    if not body and "text/csv" not in content_type.lower():
        raise HTTPException(status_code=400, detail="Missing CSV data in request body.")

    
    text = body.decode("utf-8-sig")
    csv_file = io.StringIO(text)
    reader = csv.DictReader(csv_file, delimiter=";")
    rows = list(reader)

    #empty CSV file header only, zero lines
    if not rows:
        raise HTTPException(status_code=400, detail="CSV contains no data.")

    #quarter or month
    if quarter is not None and month is not None:
        raise HTTPException(status_code=400, detail="Provide either quarter or month, not both.")

    #quarter must be 1–4
    if quarter is not None and not (1 <= quarter <= 4):
        raise HTTPException(status_code=400, detail="Invalid quarter: must be between 1 and 4.")

    #month must be alphabetic only
    if month is not None and not month.strip().isalpha():
        raise HTTPException(status_code=400, detail="Month must be a valid name, not numeric.")

    
    try:
        total = sum_expenses_by_params(
            rows,
            department=department,
            year=str(year) if year else None,
            quarter=quarter,
            month=month
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=str(ke))

    return {"total_expenses": total, "currency": "USD"}
