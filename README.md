# <p align="center">Loan Eligibility Prediction API</p>

<p align="center">
    <img src="images/project_logo.png" alt="Project Logo" >
</p>

## ➤ Menu

* [➤ Project Structure](#-project-structure)
* [➤ How to Run](#-how-to-run)
* [➤ Requirements](#-requirements)
* [➤ Outputs](#-outputs)
* [➤ Evaluation Criteria](#-evaluation-criteria)
* [➤ Performance Metrics](#-performance-metrics)
* [➤ License](#-license)
* [➤ Authors](#-authors)

---

## Project Structure

This project includes the following primary files and modules:

- **app/**
    - **main.py**: Entry point of the API. Initializes and runs the FastAPI application.
    - **routes/**:
        - **auth.py**: Defines authentication-related endpoints (login, activation).
        - **loans.py**: Endpoints for loan predictions and loan history.
        - **admin.py**: Admin-specific endpoints for user management.
    - **models/**:
        - **loan_model.pkl**: Serialized machine learning model file.
        - **user.py**: SQLModel class defining the structure of the User table.
        - **loan.py**: SQLModel class defining the structure of the LoanRequest table.
    - **core/**:
        - **security.py**: Utility functions for authentication, password hashing, and JWT.
        - **ml_model.py**: Contains the machine learning model for loan eligibility predictions.
        - **config.py**: Configuration settings for the application.
    - **database/**:
        - **database.py**: Database connection and session management using SQLModel.
    - **schemas/**:
        - **loans.py**: Pydantic models for loan data validation.
        - **users.py**: Pydantic models for user data validation.

---

## How to Run

Follow these steps to execute the project:

1. Ensure Python >= 3.9 is installed on your system.
2. Clone this repository to your local machine:

```bash
    git clone https://github.com/Khadaassi/Simplon_FastAPI.git
```
3. Navigate to the project directory:

```bash
    cd Simplon_FastAPI/App
```
4. Install the required dependencies:

```bash
    pip install -r requirements.txt
```
5. Apply database migrations using Alembic:

```bash
    alembic upgrade head
```
6. Run the FastAPI application:

```bash
    uvicorn app.main:app --reload
```

#### OR

Run the project using Docker:

1. Ensure Python 3.x is installed on your system.
2. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/Khadaassi/Simplon_App_bancaire_Django.git
    ```

3. Navigate to the project directory:

    ```bash
    cd Simplon_App_bancaire_Django/Bamk
    ```
4. Build and run your image.
    ```bash
    docker build -t fastapi-app .
    docker run -rm -p 8000:8000 fastapi-app
    ```

Deploy to Azure using Bash script:

    chmod +x script.sh
    ./script.sh

---

## Requirements

List of required software and libraries:

- Python >= 3.9
- FastAPI
- SQLModel (built on SQLAlchemy and Pydantic)
- Uvicorn
- Passlib (password hashing)
- Python-jose (JWT)
- pandas
- scikit-learn (for the ML model)

---

## Outputs

The API provides the following outputs:

- JSON responses indicating loan eligibility prediction.
- Historical records of loan requests.
- User management responses for admin operations.

### Example Output

**Loan Eligibility Prediction**

```json
{
    "eligible": true,
    "status": "approved",
    "loan_request_id": 1
}
```
---
<p align="center">Link ➔ <a href="http://bamkapp.francecentral.azurecontainer.io:8080">http://kaassi.francecentral.azurecontainer.io:8000 </a>
</p>

<p align="center"><i>Link only valid for internal use.</i></p>
---

## Evaluation Criteria

### Educational Modalities
- Group of 3 people
- Duration: 2 weeks

### Evaluation Modalities
- Oral presentation
- Peer code review

---

## Performance Metrics

- Applications and API meet the requirements of the specifications.
- No obvious security vulnerabilities.

---

## License

[MIT License](LICENSE)

---

## Authors

- **Khadija Aassi**
  <a href="https://github.com/khadijaaassi" target="_blank">
      <img loading="lazy" src="images/github-mark.png" width="30" height="30" style="vertical-align: middle; float: middle; margin-left: 30px;" alt="GitHub Logo">
  </a>

- **Ludivine Raby**
  <a href="https://github.com/ludivineRB" target="_blank">
      <img loading="lazy" src="images/github-mark.png" width="30" height="30" style="vertical-align: middle; float: middle; margin-left: 30px;" alt="GitHub Logo">
  </a>

- **Raouf Addeche**
  <a href="https://github.com/RaoufAddeche" target="_blank">
      <img loading="lazy" src="images/github-mark.png" width="30" height="30" style="vertical-align: middle; float: middle; margin-left: 30px;" alt="GitHub Logo">
  </a>

---

