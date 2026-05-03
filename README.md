# Dating Platform (Web Application)

Full-stack web application developed as a team project for the course *Principles of Software Engineering*.  
The system enables users to connect, communicate, and discover other users based on shared interests and interaction history.

---

## Overview

The application addresses the problem of finding and connecting with new people in a fast-paced environment.  
It provides real-time communication, user evaluation, and a recommendation mechanism for improving interaction quality.

---

## System Roles

- Regular user: profile creation, messaging, rating other users, reporting inappropriate behavior  
- Premium user: access to additional information such as average user ratings  
- Administrator: moderation of reports and user suspension  
- Suspended user: temporarily restricted access to system functionalities  

---

## Core Features

- User registration and authentication  
- Real-time messaging between users  
- User rating system (1–10 scale)  
- Recommendation mechanism based on user preferences and interaction history  
- Reporting and moderation system  
- Role-based access control (regular, premium, admin)  
- Profile management (create, update, delete)  

---

## Recommendation Logic

The system uses a k-nearest neighbors (k-NN) approach to determine similarity between users based on:
- profile attributes (age, interests, etc.)
- previous ratings and interactions  

Users are presented in an order that reflects predicted compatibility.

---

## Architecture

- Backend: Django (Python)  
- Frontend: HTML, CSS, JavaScript  
- Database: MySQL  
- Communication: WebSocket (real-time messaging)  

---

## Functional Scope

The system supports:
- account management (registration, login, password change)  
- user interaction (chat, rating, reporting)  
- administrative control (user suspension)  
- personalized user listing  

---

## Limitations

- No support for video or audio communication  
- No user identity verification mechanism  
- No automated content moderation  
- Basic data protection mechanisms  

---

## Development Context

The project was developed in a team environment as part of a software engineering course, with focus on:
- requirements analysis  
- system design  
- role distribution and collaboration  
- implementation of a complete full-stack application  

---

## Author

Nina Bucalo  
University of Belgrade, School of Electrical Engineering  
GitHub: https://github.com/bucalonina  
