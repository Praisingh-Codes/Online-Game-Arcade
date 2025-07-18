## Title - Web Arcade: A Platform for Instant Access to Casual Games

##  Introduction

<div align="justify">

Web Arcade: A Platform for Instant Access to Casual Games is a web-based entertainment system designed to deliver quick and engaging gameplay experiences directly through a browser. The platform provides users with instant access to a variety of casual and arcade-style games without the need for downloads or installations, making it accessible across desktops, laptops, tablets, and smartphones.
  
The primary objective of this project is to create a user-friendly, responsive, and lightweight gaming environment that emphasizes ease of use, fast loading times, and enjoyable gameplay. By focusing on casual games with simple controls and intuitive mechanics, the platform caters to players of all ages and skill levels.

This project reflects the growing demand for on-the-go digital entertainment and explores how web technologies can be used to replicate the charm of traditional arcade gaming in a modern, accessible format. Through this platform, users can enjoy nostalgic classics and quick-play games in a seamless and interactive environment, highlighting both technical implementation and user experience.
</div>

##  Structure 

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

## Setup Instructions

1. Clone the Repository

    Terminal - Command - Git Clone 

    https://github.com/Praisingh-Codes/Online-Game-Arcade.git

    cd Online-Game-Arcade


2. Create Virtual Environment

   Terminal - Command
   
   python -m venv venv
   
   source venv/bin/activate # On Windows: venv\Scripts\activate


3. Install Dependencies
   
   Terminal - Command
    
   pip install -r requirements.txt


4. Set Up the Database

   Import arcadiadb.sql into your MySQL server:

   SQl - Command
  
   CREATE DATABASE arcade;
   
   USE arcade;
   
   -- then run arcadiadb.sql content
   
   Update your MySQL credentials in app.py or a config file.


5. Run the Web Application
   
   Terminal - Command
   
   python App.py

   Then go to http://127.0.0.1:5000/ in your browser.

## Screenshots

####  Home
![Home Page](outcome%20screenshots/1.home_page.png)

####  Admin Login 
![Admin Login Page](outcome%20screenshots/2.admin_login_page.png)

####  User Login 
![User Login Page](outcome%20screenshots/3.user_login_page.png)

#### User Welcome
![User Welcome Page](outcome%20screenshots/6.user_welcome_page.png)

####  User Information 
![Personal Information Page](outcome%20screenshots/7.personal_info_page.png)

####  User Statistics 
![User Statistics Page](outcome%20screenshots/8.player_states_page.png)

####  Games 
![Game Page](outcome%20screenshots/9.game_page.png)

####  Angrybird 🎮
![Angrybird Game](outcome%20screenshots/angrybird_game.png)

####  Mario 🎮
![Mario Game](outcome%20screenshots/mario_game.png)

####  Mini Golf 🎮
![Mini Golf Game](outcome%20screenshots/minigolf_game.png)


## Future scope

<div align="justify">
The Web Arcade platform offers considerable potential for future development and expansion. As user expectations and digital entertainment technologies continue to evolve, the platform can be enhanced with a broader game library, user account features for saving progress and tracking achievements, and social functionalities such as leaderboards, multiplayer support, and community interaction. Cross-device synchronization can further improve accessibility by allowing seamless gameplay across desktops, tablets, and mobile phones. Incorporating artificial intelligence can introduce adaptive gameplay and smarter in-game opponents, while cloud gaming integration could enable high-performance experiences without reliance on local hardware. Additionally, the adoption of emerging technologies like Virtual and Augmented Reality could provide immersive and interactive gaming environments. In the long term, monetization strategies such as ad integration, premium content, or in-app purchases can help sustain platform growth. With these enhancements, Web Arcade is well-positioned to evolve into a dynamic, user-centric gaming ecosystem that redefines casual browser-based gaming.
</div>
