# Late Show API - Flask Backend

A RESTful API for managing late show episodes, guests, and appearances built with Flask and SQLAlchemy.

## Features

- CRUD operations for episodes, guests, and appearances
- Database relationships between models
- Seeding script for sample data
- Flask-Migrate for database migrations

## Models

### Episode
- id: Integer (primary key)
- date: String
- number: Integer
- appearances: Relationship to Appearance

### Guest
- id: Integer (primary key)
- name: String
- occupation: String
- appearances: Relationship to Appearance

### Appearance
- id: Integer (primary key)
- rating: Integer (1-5)
- episode_id: ForeignKey to Episode
- guest_id: ForeignKey to Guest

## API Endpoints

### Episodes
- `GET /episodes` - List all episodes
- `GET /episodes/<id>` - Get episode details

### Guests
- `GET /guests` - List all guests

### Appearances
- `POST /appearances` - Create new appearance
