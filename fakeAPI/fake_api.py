from fastapi import FastAPI

app = FastAPI()

# Hardcoded menu data
menu_data = {
    "date": "03.09.2025",
    "day": "Wednesday",
    "total_calories": 1472,
    "items": [
        {"name": "Lentil soup", "calories": 125},
        {"name": "Chicken", "calories": 277},
        {"name": "Eggplant", "calories": 235},
        {"name": "Rice", "calories": 328},
        {"name": "Dessert", "calories": 511},
        {"name": "Fruits", "calories": None},
        {"name": "Salads", "calories": None}
    ]
}

# API endpoint to get the menu
@app.get("/api/menu")
async def get_menu():
    return menu_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)