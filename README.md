# Credit Approval System

## Overview

This is a Django application designed for a credit approval system. The application utilizes Docker Compose for easy deployment and management of services such as PostgreSQL, Redis, Django, and Celery.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Accessing the Django Admin](#accessing-the-django-admin)
- [Docker Compose](#docker-compose)
- [Custom Django Commands](#custom-django-commands)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/dronacharya_27/Alemeno_Task
```
# Navigate to the project directory
cd credit-approval-system

# Running the Application
```bash

# Build the Docker containers
docker-compose build
# Start the Docker containers
docker-compose up
```
The application should be accessible at http://localhost:8000/.

# Usage
Accessing the Django Admin
Open your web browser and go to http://localhost:8000/admin/.
Log in using the admin credentials.

# Docker Compose
The docker-compose.yml file defines the services needed for the application:
1. db: PostgreSQL database
2. redis: Redis server
3. web: Django application, Gunicorn, Celery worker

```bash
# Stop the application and services
docker-compose down
```
