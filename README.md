## Web Arcade: A Platform for Instant Access to Casual Games

<div align="justify">A full-stack Flask-powered arcade platform that provides instant access to a collection of casual games including Angry Birds, Mario, and Mini Golf all running locally through Pygame.

The system includes user authentication, an admin dashboard, payment info management, player performance tracking, and a sleek arcade-themed UI.</div>

#### Project Structure

Online Game Arcade/

├── data/ # Data files or gameplay-related assets

├── resources/ # Game-related images, sounds, or fonts

├── static/ # Static files for the Flask app (CSS, JS, images)

├── templates/ # HTML templates for Flask rendering

├── angrybird.py # Angry Bird game script

├── mario.py # Mario game script

├── minigolf.py # Mini Golf game script

├── App.py # Flask main app file

├── arcadiadb.sql # SQL file to set up the MySQL database

├── player-stats.json # Sample JSON player stats

├── requirements.txt # Required Python packages

└── outcome screenshots/   # UI/Game screenshots


#### Features
👤 User Features

•	User registration & login

•	Player dashboard

•	Game selection

•	Payment info (dummy integration)

•	View & update profile

•	Player statistics tracking

•	Play history

•	Launch desktop games instantly from browser

🛠 Admin Features

•	Admin login

•	View all users

•	View payments

•	View player stats

•	Navigate throughout the system

#### Included Games

Game	Framework	Directory

Angry Birds	Pygame + Pymunk physics	/angrybird

Mario	Pygame	/mario

Mini Golf	Pygame (state machine engine)	/minigolf

#### Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/Praisingh-Codes/Online-Game-Arcade.git

cd Online-Game-Arcade

2️⃣ Create Virtual Environment

python -m venv venv

venv\Scripts\activate   # Windows

3️⃣ Install Required Packages

pip install -r requirements.txt

4️⃣ Import Database

•	Open phpMyAdmin / MySQL Workbench / XAMPP

•	Create DB:

CREATE DATABASE arcadiadb;
•	Import file:

arcadiadb.sql

5️⃣ Start the Flask Server

python App.py

6️⃣ Open the Web App

Visit:

http://127.0.0.1:5000

#### Game Launching System
Flask uses subprocess to launch each game:

subprocess.Popen(["python", "angrybird/main.py"])

This opens a standalone Pygame window without blocking Flask, giving a smooth seamless arcade experience.

#### Player Statistics
Player performance—scores, time played, gameplay history—is stored automatically in:

player-stats.json

Admin can view aggregated data from the dashboard.

#### Screenshots
![Home Page](outcome%20screenshots/1.home_page.png)

![User Welcome Page](outcome%20screenshots/6.user_welcome_page.png)

![Angrybird Game](outcome%20screenshots/angrybird_game.png)

#### Technologies Used

Web Backend

•	Flask
•	Python

•	MySQL
•	Jinja2

•	Subprocess

Games

•	Pygame
•	Pymunk Physics

•	Custom State Engines

Frontend

•	HTML5
•	CSS3

•	Bootstrap
•	JavaScript

#### Roadmap / Future Enhancements
•	Add multiplayer support
•	Add leaderboard system

•	Add cloud save system
•	Convert games to browser-playable WASM versions

•	Add sound/music toggles
•	Add new games to the arcade platform
