# Multi-User To-Do List with Email Notifications  

## Overview  
This is a **multi-user To-Do List application** built with **Python (Tkinter) and MySQL**, allowing multiple users to manage their tasks independently. The application provides task management features, user authentication, and email notifications for task updates.  

## Features  
- **User Authentication:** Each user has a separate task database.  
- **Task Management:** Add, delete, and clear tasks with a simple UI.  
- **Admin Controls:** Manage users with authentication checks.  
- **Email Notifications:** Sends task summaries via email.  
- **Security:** Admin login failure captures a webcam snapshot for security.  
- **Elegant UI:** Inspired by Monet's thematic style for a soft, aesthetic look.  

## Technologies Used  
- **Python** (Tkinter for GUI)  
- **MySQL** (Database for storing user tasks & credentials)  
- **SMTP (smtplib)** (For email notifications)  
- **OpenCV & PIL** (For security features)  

## Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/Vaibhavbhor404/projects.git
   cd projects
   ```
2. Install dependencies:  
   ```bash
   pip install mysql-connector-python opencv-python pillow smtplib
   ```

3. Database setup:
   ```sql
   CREATE DATABASE notes;
   USE notes;

   CREATE TABLE credentials (
       username VARCHAR(255) PRIMARY KEY,
       password VARCHAR(255),
       email VARCHAR(255)
   );

   ```

4. Running the application:  
   ```bash
   python main.py
   ```

## Usage  
- **Register/Login** to manage tasks individually.  
- **Add/Delete tasks** in the interactive UI.  
- **Receive email reminders** for pending tasks.  

## Contributing  
Feel free to fork this repository and contribute by submitting pull requests.  

## License  
This project is open-source and available under the MIT License.
