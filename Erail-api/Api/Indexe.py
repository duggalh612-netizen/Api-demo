from fastapi import FastAPI, Request, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# 🔑 Secret code
SECRET_CODE = "harshduggal0090"

# ✅ Middleware: check API key in query
def check_secret(request: Request):
    code = request.query_params.get("code")
    if code != SECRET_CODE:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid secret code")


# 1. Trains Between Stations
@app.get("/trains-between")
def trains_between(from_station: str, to_station: str, request: Request = None):
    check_secret(request)
    url = f"https://erail.in/trains-between-stations/{from_station}/{to_station}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    trains = []
    for row in soup.select("#divTrainsList tr"):
        cols = [c.get_text(strip=True) for c in row.select("td")]
        if cols:
            trains.append(cols)
    return {"trains": trains}


# 2. Train Info
@app.get("/train-info")
def train_info(train_no: str, request: Request = None):
    check_secret(request)
    url = f"https://erail.in/train-enquiry/{train_no}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.select_one("span#spnTrainName").text if soup.select_one("span#spnTrainName") else "Not Found"
    return {"train_no": train_no, "train_name": name}


# 3. Live Train Status
@app.get("/live-status")
def live_status(train_no: str, date: str, request: Request = None):
    check_secret(request)
    url = f"https://erail.in/rail/live-train-status/{train_no}/{date}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return {"status": soup.get_text(strip=True)}


# 4. All Stations
@app.get("/stations")
def stations(request: Request = None):
    check_secret(request)
    url = "https://erail.in/stations-list"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    stations = [s.text for s in soup.select("table tr td a")]
    return {"stations": stations}
