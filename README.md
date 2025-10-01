# 🐾 pawliday backend

The **pawliday backend** is a RESTful API built with **Flask (Python)** for the pawliday project — a web app and efficient digital organization tool for dog care services based on the individual characters and needs of the animals. As a dog sitter you can manage all important data about the dogs and the owners in one place.  
It provides endpoints for user authentication, sitter, owner, and dog management, and integrates with [imagekit.io](https://imagekit.io/) for dog image storage.

---

## 🚀 Features

- 🔑 **User Authentication:** Register, log in, log out, and manage sitter profiles
- 👩‍⚕️ **Owner Management:** CRUD operations for dog owners
- 🐶 **Dog Management:** CRUD operations for dogs linked to owners
- 📷 **Image Support:** Handles image uploads via frontend using imagekit.io
- 🌐 **RESTful API:** Communicates securely with the pawliday frontend

---

## 📚 Table of Contents

1. [About the Project](#-about-the-project)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Getting Started](#-getting-started)
5. [API Endpoints](#-api-endpoints)

---

## 💡 About the Project

The **pawliday backend** powers the pawliday app by:

- Managing sitter (user) accounts
- Handling authentication and secure sessions
- Storing and retrieving owner and dog data
- Providing an API consumed by the React frontend

---

## 🛠 Tech Stack

- **Framework:** [Flask](https://flask.palletsprojects.com/)
- **Language:** Python 3.x
- **Database:** SQLite (via `SQLiteHandler`)
- **Authentication:** JWT with cookies
- **CORS:** Enabled for local development and deployed frontend
- **Image Storage:** [imagekit.io](https://imagekit.io/)

---

## ⚙ Getting Started

### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [Virtualenv](https://docs.python.org/3/library/venv.html) (recommended)

### Installation

### Clone the repo

git clone https://github.com/Lina0596/pawliday_backend.git
cd pawliday_backend

### Create and activate a virtual environment

python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

### Install dependencies

pip install -r requirements.txt

### 🔑 Environment Variables

JWT_SECRET_KEY=your_jwt_secret_key
IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
IMAGEKIT_URL_ENDPOINT=your_imagekit_url_endpoint

### ▶ Running the Server

flask run

## 🌐 API Endpoints

### 🟢 Health & Utility

| Method | Endpoint           | Description                        |
| ------ | ------------------ | ---------------------------------- |
| GET    | `/api/wakeup`      | Health check to keep server awake  |
| GET    | `/api/auth-params` | Get ImageKit authentication params |

---

### 🔐 Authentication & Sitter

| Method | Endpoint             | Description                       |
| ------ | -------------------- | --------------------------------- |
| POST   | `/api/login`         | Log in sitter and set JWT cookies |
| POST   | `/api/logout`        | Log out sitter and clear cookies  |
| POST   | `/api/registration`  | Register a new sitter             |
| GET    | `/api/sitter`        | Get the logged-in sitter profile  |
| PUT    | `/api/sitter/update` | Update sitter profile             |
| DELETE | `/api/sitter/delete` | Delete sitter profile             |

---

### 👩‍👩‍👦 Owner Management

| Method   | Endpoint                               | Description                                        |
| -------- | -------------------------------------- | -------------------------------------------------- |
| GET      | `/api/sitter/owners`                   | Get all owners for the logged-in sitter            |
| GET      | `/api/sitter/owners/<owner_id>`        | Get a specific owner’s details                     |
| GET/POST | `/api/sitters/owners/add`              | Retrieve all owners (GET) / Add a new owner (POST) |
| PUT      | `/api/sitter/owners/<owner_id>/update` | Update a specific owner                            |
| DELETE   | `/api/sitter/owners/<owner_id>/delete` | Delete a specific owner and all their dogs         |

---

### 🐶 Dog Management

| Method   | Endpoint                                 | Description                                      |
| -------- | ---------------------------------------- | ------------------------------------------------ |
| GET      | `/api/sitter/dogs`                       | Get all dogs for the logged-in sitter            |
| GET      | `/api/sitter/dogs/<dog_id>`              | Get details of a specific dog                    |
| GET/POST | `/api/sitter/owners/<owner_id>/dogs/add` | Retrieve owner’s dogs (GET) / Add new dog (POST) |
| PUT      | `/api/sitter/dogs/<dog_id>/update`       | Update a specific dog’s details                  |
| DELETE   | `/api/sitter/dogs/<dog_id>/delete`       | Delete a specific dog                            |
| GET      | `/api/sitter/owners/<owner_id>/dogs`     | Get all dogs for a specific owner                |
