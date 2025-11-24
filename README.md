# Event Scheduling System

## Overview
This is an Event Scheduling System built using Flask and MySQL. The app helps you manage events, resources (rooms, instructors, equipment), and allocate resources to events while preventing scheduling conflicts. Perfect for schools, training centers, or any organization that needs to coordinate events and resources.

## Features
* **Event Management**: Create, update, view, and delete events with start and end times.
* **Resource Management**: Add, update, view, and delete resources (rooms, instructors, equipment).
* **Smart Allocation**: Allocate resources to events with automatic conflict detection.
* **Utilization Reports**: Generate reports showing resource usage over custom date ranges.
* **Responsive Design**: Clean, modern interface with Bootstrap 5 and custom styling.

## Screenshots

### Events Page

Navigate to Events page
Fill in the event details:
Title (e.g., "Introduction to Python")
Start time
End time
Click Create Event
Edit or delete events using the action buttons
<img width="1919" height="863" alt="Screenshot 2025-11-24 065847" src="https://github.com/user-attachments/assets/bd0a531e-ff30-4ad2-950a-232b68017bac" />

### Resources Page
Navigate to Resources page
Add resources by providing:
Resource name
Resource type (room, instructor, or equipment)
Edit or delete resources as needed
<img width="1918" height="868" alt="Screenshot 2025-11-24 065910" src="https://github.com/user-attachments/assets/7c9e2ffc-682f-49d5-af7f-ac06fbabfbe1" />

### Allocate Page
Navigate to Allocate page
Select an event from the dropdown
Select a resource to allocate
Click Allocate
The system will prevent double-booking automatically
<img width="1919" height="873" alt="Screenshot 2025-11-24 065935" src="https://github.com/user-attachments/assets/01894c8a-ed0f-43de-883a-c4fa4a7254fb" />

### Report Page
Navigate to Report page
Select a date range (start and end dates)
Click Generate Report
View:
Total hours utilized per resource
List of bookings for each resource
Resource types and names
<img width="1919" height="863" alt="Screenshot 2025-11-24 070008" src="https://github.com/user-attachments/assets/40d51fe2-93e4-4d73-ba48-df96f490fd4c" />

## Tech Stack
* **Backend**: Flask (Python web framework)
* **Database**: MySQL
* **Frontend**: HTML, Bootstrap 5, Font Awesome
* **Template Engine**: Jinja2

## Prerequisites
Before running the app, make sure you have the following installed:
* Python 3.7+
* MySQL Server
* pip (for installing Python packages)

## Installation

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd event-scheduling-system
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Database

Edit `db_config.py` and update your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'event'
}
```

### Step 4: Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your browser to start using the app.

The database and tables will be created automatically on first run.

```

## How to Use

### Event Management
* **Add Event**: Fill in the event title, start time, and end time, then click "Create Event".
* **Update Event**: Click the "Edit" button next to any event to modify its details.
* **View Events**: All events are listed on the Events page with their schedules.
* **Delete Event**: Click the "Delete" button to remove an event.

### Resource Management
* **Add Resource**: Enter the resource name and select the type (room, instructor, or equipment).
* **Update Resource**: Click "Edit" to modify resource details.
* **View Resources**: All resources are displayed with color-coded type badges.
* **Delete Resource**: Remove resources using the "Delete" button.

### Resource Allocation
* **Allocate Resource**: Select an event and a resource from the dropdowns, then click "Allocate".
* **Conflict Detection**: The system automatically prevents double-booking of resources.
* **View Allocations**: See all current allocations in the table on the right.
* **Update Allocation**: Click "Edit" to change an allocation.
* **Remove Allocation**: Click "Remove" to deallocate a resource from an event.

### Utilization Reports
* **Generate Report**: Select a start date and end date, then click "Generate Report".
* **View Usage**: See total hours utilized for each resource.
* **Check Bookings**: View upcoming bookings for each resource in the selected period.

## Key Features

### Automatic Conflict Detection
The system checks for scheduling conflicts when allocating resources. If a resource is already booked during the requested time slot, you'll receive an error notification.

### Time Formatting
All times are displayed in an easy-to-read format: `MMM DD, HH:MM AM/PM`

Example: `Nov 24, 05:46 AM — Nov 24, 06:46 AM`

### Cascade Deletion
* Deleting an event automatically removes all its resource allocations
* Deleting a resource removes all its allocations from events

## Database Schema

### Event Table
* `event_id` (Primary Key, Auto Increment)
* `title` (Event name)
* `start_time` (Event start date and time)
* `end_time` (Event end date and time)
* `description` (Optional event description)

### Resource Table
* `resource_id` (Primary Key, Auto Increment)
* `resource_name` (Name of the resource)
* `resource_type` (Type: room, instructor, or equipment)

### EventResourceAllocation Table
* `allocation_id` (Primary Key, Auto Increment)
* `event_id` (Foreign Key → Event)
* `resource_id` (Foreign Key → Resource)

## Troubleshooting

### Database Connection Issues
If you see connection errors:
1. Verify MySQL is running: `sudo service mysql status`
2. Check credentials in `db_config.py`
3. Ensure the MySQL user has proper permissions



```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

## Future Enhancements
* User authentication and role-based access control
* Email notifications for upcoming events
* Calendar view for better visualization
* Export reports to PDF/Excel
* Multi-resource allocation in one action
* Support for recurring events
* Mobile app version

## LinkedIN LINK : 
https://www.linkedin.com/posts/sobika-m-36b536333_flask-python-webdevelopment-activity-7398611218497933312-4d07?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFPoCYMBEJnYBBgcw0644x_kiJMBwsKx_6M

