# Music School Management System (MSMS)

## Overview
MSMS is a Python application designed to support music school administration, including student and teacher management, scheduling, attendance, and finance-related activities.

## Technologies Used
- Python
- Streamlit for the graphical user interface
- Pytest for automated testing
- JSON for data storage
- CSV for report exports

## Project Structure
- `main.py`: Application entry point.
- `app/`: Core application logic and administrative utilities.
- `gui/`: User interface pages and dashboard.
- `tests/`: Automated tests.
- `data/`: Application data and backups.

## Running the Application
Install the required dependencies, then run:

```bash
streamlit run main.py
```

## Running Tests
Run the automated tests with:

```bash
python -m pytest
```

Check for Python syntax errors with:

```bash
python -m compileall -q app gui tests main.py
```

## Finance and Reporting
The application includes finance functionality and supports exporting finance and attendance reports to CSV files.

## Logging and Backups
Administrative utilities provide application logging and data backup functionality.

## Design Choices and Assumptions
The application separates core logic from the graphical interface to improve organisation and maintainability. JSON is used for data storage, CSV for report exports, and automated tests to check application functionality.

## Limitations
This is an academic project. Further testing, security improvements, and access controls would be required before production use.
