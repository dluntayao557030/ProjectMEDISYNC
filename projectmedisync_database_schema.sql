CREATE DATABASE projectmedisync_luntayao;
USE projectmedisync_luntayao;

CREATE TABLE users (
    user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role ENUM('Doctor', 'Nurse', 'Pharmacist', 'Admin') NOT NULL,
    license_number VARCHAR(30) NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NULL,
    email_address VARCHAR(150) NULL,
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE patients (
    patient_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    patient_first_name VARCHAR(50) NOT NULL,
    patient_last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    sex ENUM('Male', 'Female') NOT NULL,
    emergency_contact_name VARCHAR(100) NULL,
    emergency_person_relationship VARCHAR(30) NOT NULL,
    emergency_contact_number VARCHAR(20) NULL,
    room_number VARCHAR(10) NULL,
    admission_date DATETIME NOT NULL,
    diagnosis VARCHAR(255) NULL,
    doctor_id INT UNSIGNED NULL,
    nurse_id INT UNSIGNED NULL,
    added_by INT UNSIGNED NULL,
    status ENUM('Active', 'Discharged', 'Deceased') DEFAULT 'Active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_patient_added_by
        FOREIGN KEY (added_by) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_patient_doctor
        FOREIGN KEY (doctor_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_patient_nurse
        FOREIGN KEY (nurse_id) REFERENCES users(user_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE medicines (
    medicine_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    generic_name VARCHAR(150) NOT NULL,
    brand_name VARCHAR(150) NULL,
    formulation VARCHAR(100) NOT NULL,
    strength VARCHAR(100) NOT NULL,
    description VARCHAR(255) NULL,
    is_controlled BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE prescriptions (
    prescription_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    patient_id INT UNSIGNED NOT NULL,
    doctor_id INT UNSIGNED NOT NULL,
    medicine_id INT UNSIGNED NOT NULL,
    dosage VARCHAR(50) NOT NULL,
    duration_start DATE NOT NULL,
    duration_end DATE NOT NULL,
    frequency VARCHAR(100) NOT NULL,
    special_instructions VARCHAR(255) NULL,
    status ENUM(
        'Pending Verification',
        'Active',
        'Completed',
        'Modification Requested',
        'Rejected'
    ) DEFAULT 'Pending Verification',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_prescription_patient
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_prescription_doctor
        FOREIGN KEY (doctor_id) REFERENCES users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_prescription_medicine
        FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE prescription_verification (
    verification_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prescription_id INT UNSIGNED NOT NULL UNIQUE,
    pharmacist_id INT UNSIGNED NOT NULL,
    medication_lot_number VARCHAR(100) NULL,
    quantity_dispensed INT UNSIGNED NULL,
    expiry_date DATE NULL,
    decision ENUM('Approve', 'Request Modification', 'Reject') NOT NULL,
    reason VARCHAR(255) NULL,
    verified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_verification_prescription
        FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_verification_pharmacist
        FOREIGN KEY (pharmacist_id) REFERENCES users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE medication_administration (
    administration_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prescription_id INT UNSIGNED NOT NULL,
    nurse_id INT UNSIGNED NOT NULL,
    administration_time DATETIME NOT NULL,
    patient_assessment VARCHAR (50) NOT NULL,
    adverse_reactions VARCHAR(255) NULL,
    remarks VARCHAR(255) NULL,
    status ENUM('Administered', 'Missed') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_med_admin_prescription
        FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_med_admin_nurse
        FOREIGN KEY (nurse_id) REFERENCES users(user_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE medicine_preparation (
    preparation_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prescription_id INT UNSIGNED NOT NULL,
    quantity_prepared INT UNSIGNED NOT NULL,
    lot_number VARCHAR(100) NULL,
    status ENUM('Prepared', 'To be Prepared') DEFAULT 'To be Prepared',
    CONSTRAINT fk_prep_prescription
        FOREIGN KEY (prescription_id) REFERENCES prescriptions(prescription_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE notifications (
    notification_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    related_table VARCHAR(50) NULL,
    related_id INT UNSIGNED NULL,
    title VARCHAR(150) NOT NULL,
    message VARCHAR(255) NOT NULL,
    type ENUM('Urgent','Attention','Info') DEFAULT 'Info',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notifications_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);