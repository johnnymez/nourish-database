# Nourish Database System

## Overview

This Nourish Database System is a Food Pantry Distribution System that was made to help with operations at food distribution centers. The system provides a user friendly interface for managing household information, volunteer coordination, donation tracking, and inventory management.

### Key Features

- **Household Management**: Register and track household information, including demographics and TFAP certification status
- **Volunteer Tracking**: Maintain volunteer records with contact information and service hours
- **Donation Source Tracking**: Monitor and manage donation sources and distribution sources
- **Inventory Lot Management**: Track food inventory by lot with expiration dates and storage locations
- **Visit History Tracking**: Record household visits and distribution activities
- **Proxy Household Support**: Handle proxy household registrations and support
- **Distribution Item Tracking**: Log individual items distributed to households
- **Inventory Remaining Calculations**: Automatically calculate remaining inventory based on distributions

### Technology Stack

- **Language**: Python
- **Database**: SQLite
- **Interface**: Command-line and webpage

## Installation Instructions

### Prerequisites

- Python 3.7 or higher
- SQLite 3

### Setup Steps

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd "Final Project Database Design"
   ```

2. **Install Python** (if not already installed)
   - Visit [python.org](https://www.python.org/) and download Python 3.7 or higher

3. **Verify SQLite installation**
   ```bash
   sqlite3 --version
   ```

4. **Initialize the database**
   - The system automatically creates `final_project-1.db` on first run if it doesn't exist

## Usage Instructions

### Command-Line Interface

Run the command-line application:
```bash
python nourishapp.py
```

The menu-driven interface allows you to:
- Add and manage households
- Register and track volunteers
- Record donations and sources
- Manage inventory lots and items
- Log visits and distributions

### Web Interface

Run the web application:
```bash
python webapp.py
```

Then open your web browser and navigate to `http://localhost:8000` to access the web-based interface.