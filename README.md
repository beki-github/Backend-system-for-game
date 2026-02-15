# Backend System for Games

An API-driven backend platform designed to manage game data, user authentication, and persistent player progress tracking. This project serves as the Capstone Project for Part 3 of the development phase.

## 🚀 Overview
This system provides a centralized hub for gaming applications to store user data and progress metrics. Built with **Django** and **Django REST Framework**, it implements a robust relational database schema to handle many-to-many relationships between players and games.

## 🛠️ Tech Stack
* **Framework:** Django 5.x
* **API Toolkit:** Django REST Framework (DRF)
* **Database:** SQLite (Development) / PostgreSQL (Production ready)
* **Authentication:** Token-based Session Management

## 📊 Database Architecture
The project is built based on a custom Entity Relationship Diagram (ERD) featuring:
* **User:** Core authentication and profile data.
* **Game:** Catalog of available games with unique slugs and descriptions.
* **PlayerProgress:** A specialized join table tracking `level`, `playtime_minutes`, and `progress_percentage`.
* **UserSession:** Management of active authentication tokens and expiration.

## ⚙️ Initial Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/backend_system_for_games.git](https://github.com/YOUR_USERNAME/backend_system_for_games.git)
cd backend_system_for_games
