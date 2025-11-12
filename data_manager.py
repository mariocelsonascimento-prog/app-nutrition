# data_manager.py
import os, json
from datetime import date

DATA_DIR = "data"
PLAN_FILE = os.path.join(DATA_DIR, "plan.json")  # sua dieta (Minha dieta)
LOGS_DIR = os.path.join(DATA_DIR, "logs")        # consumos por dia

def _ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

def save_plan(meals: dict):
    """Salva a dieta (todas as refeições) em data/plan.json"""
    _ensure_dirs()
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(meals, f, ensure_ascii=False, indent=2)

def load_plan() -> dict:
    """Carrega a dieta (refeições) do disco"""
    _ensure_dirs()
    if not os.path.exists(PLAN_FILE):
        return {}
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _log_path(day: str) -> str:
    return os.path.join(LOGS_DIR, f"{day}.json")

def today_str() -> str:
    return date.today().isoformat()

def save_log(day: str, entries: list):
    """Salva o consumo do dia em data/logs/YYYY-MM-DD.json"""
    _ensure_dirs()
    with open(_log_path(day), "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def load_log(day: str) -> list:
    """Carrega o consumo do dia"""
    _ensure_dirs()
    path = _log_path(day)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
