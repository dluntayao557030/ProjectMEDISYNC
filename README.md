# MEDISYNC - Medicine Monitoring System

![MEDISYNC Logo](ImageResources/MEDISYNCLogoBGRemoved.png)  
*(A hospice-focused medication management system)*

## Overview

MEDISYNC is a desktop-based **Medicine Monitoring System** designed specifically for hospice and palliative care facilities. It streamlines the medication workflow by providing real-time monitoring, prescription-level expiry tracking, and strict role-based access control to ensure timely, safe, and accountable administration of medications for patients in end-of-life care.

The system supports collaboration among **Doctors**, **Pharmacists**, **Nurses**, and **Administrators**, reducing medication delays, preventing administration of expired drugs, and maintaining clear accountability throughout the process.

This project was developed as a final requirement for **IT5/L – IT Elective 2** at the University of Mindanao, submitted in December 2025.

## Key Features

- **Real-Time Monitoring & Notifications**  
  Automated alerts for upcoming, due, or missed medication schedules sent to nurses and doctors.
  
- **Prescription-Level Expiry Tracking**  
  Tracks batch numbers and expiry dates for each individual prescription (not just bulk inventory).

- **Role-Based Access Control (RBAC)**  
  Different permissions and dashboards for:
  - Doctors (prescribe & edit prescriptions)
  - Pharmacists (verify prescriptions, add lot/expiry details)
  - Nurses (record administration, patient assessments, adverse reactions)
  - Administrators (manage users, patients, generate reports)

- **Comprehensive Logging & Audit Trail**  
  Every action is time-stamped and linked to the responsible user.

- **User-Friendly PyQt6 Interface**  
  Clean dashboards, pop-up summaries for confirmation, and intuitive navigation.

## Technologies Used

- **Language**: Python
- **IDE**: PyCharm
- **GUI Framework**: PyQt6
- **Database**: MySQL (via XAMPP)
- **Database Management**: phpMyAdmin

## Database Structure

The system uses the following main tables:

- `users`
- `patients`
- `medicines`
- `prescriptions`
- `prescription_verification`
- `medicine_preparation`
- `medication_administration`
- `notifications`

## Installation & Setup

1. **Prerequisites**
   - Install [Python 3.x](https://www.python.org/downloads/)
   - Install [XAMPP](https://www.apachefriends.org/index.html) (for MySQL)
   - Start Apache and MySQL in XAMPP Control Panel

2. **Database Setup**
   - Open phpMyAdmin (`http://localhost/phpmyadmin`)
   - Create a new database (e.g., `medisync_db`)
   - Import the schema file (if provided as `projectmedisync_database_schema.sql`)

3. **Install Dependencies**
   ```bash
   pip install PyQt6 pymysql python-dotenv
