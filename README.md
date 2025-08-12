# Sales and Profit Prediction System

This project is a full-stack application that uses machine learning to predict future sales and profit based on previous data. It is built using:

- **FastAPI** for the backend API
- **Python** for machine learning
- **SQL Server** for data storage
- **ASP.NET Core MVC** for the frontend (not included in this repo)

## Features

- Upload sales datasets
- Clean and train ML model
- Predict future sales and profits
- Secure user and admin login with JWT
- Role-based access for Admin and Users
- View prediction history and results

## Project Structure

```
sales_prediction/
├── app/
│   ├── main.py               # FastAPI entry point
│   ├── models.py             # Pydantic request/response models
│   ├── database.py           # SQL Server connection
│   ├── crud.py               # DB operations
│   ├── ml_model.py           # Load and run predictions
│   ├── schemas.py            # SQLAlchemy models
│   ├── auth.py               # JWT-based auth
│   └── routers/
│       ├── users.py
│       ├── admin.py
│       └── predictions.py
├── data/
│   └── uploaded/             # Uploaded datasets
├── models/
│   └── model.pkl             # Trained ML model
├── requirements.txt
└── README.md
```

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI app:
```bash
uvicorn app.main:app --reload
```

3. Access the API docs:
```
http://localhost:8000/docs
```

## Note

You need to set up a working **SQL Server instance** and update the connection string in `database.py`.
