from datetime import date
import re

def validate_email(email_str):
    errors = []
    if not email_str:
        errors.append("Email cannot be empty.")
        return errors 

    if len(email_str) > 50:
        errors.append("Email cannot exceed 50 characters.")
    
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_str):
        errors.append("Invalid email format.")

    return errors

def validate_password(password_str):
    errors = []
    if not password_str:
        errors.append("Password cannot be empty.")
        return errors

    if len(password_str) > 100:
        errors.append("Password cannot exceed 100 characters.")
        
    return errors

def validate_address(address_str):
    errors = []
    if not address_str:
        errors.append("Address cannot be empty.")
    return errors

def validate_phone(phone_str):
    errors = []
    if not phone_str:
        errors.append("Phone number cannot be empty.")
        return errors

    if len(phone_str) > 15:
        errors.append("Phone number cannot exceed 15 characters.")
    
    if not re.match(r"^\+?[0-9\s-]{7,15}$", phone_str):
        errors.append("Invalid phone number format. Use digits, spaces, or hyphens.")
        
    return errors

def validate_start_date(date_str):
    errors = []
    if not date_str:
        errors.append("Start date cannot be empty.")
        return errors

    return errors

def validate_end_date(start_date_str, end_date_str):
    errors = []
    if not end_date_str: 
        return errors 
    try:
        tanggal_akhir_obj = date.fromisoformat(end_date_str)
        
        if start_date_str:
            tanggal_mulai_obj = date.fromisoformat(start_date_str)
            print(tanggal_akhir_obj)
            print(tanggal_mulai_obj)
            if tanggal_akhir_obj > tanggal_mulai_obj:
                errors.append("Tanggal akhir kerja tidak boleh sebelum tanggal mulai kerja.")
        
    except ValueError:
        errors.append("Format tanggal akhir kerja tidak valid. Harap gunakan format YYYY-MM-DD.")
    
    return errors


def validate_password_update(user_email, old_password_input, new_password1, new_password2, query_func):
    errors = {}

    if not old_password_input:
        errors.setdefault('old_password', []).append("Old password is required.")

    if not new_password1:
        errors.setdefault('new_password1', []).append("New password is required.")
    else:
        strength_errors = validate_password(new_password1)
        if strength_errors:
            errors.setdefault('new_password1', []).extend(strength_errors)
        
        if new_password1 == old_password_input and old_password_input:
             errors.setdefault('new_password1', []).append("New password must be different from the old password.")

    if not new_password2:
        errors.setdefault('new_password2', []).append("Confirm new password is required.")
    elif new_password1 and new_password1 != new_password2:
        errors.setdefault('new_password2', []).append("New passwords do not match.")

    if not errors.get('old_password') and old_password_input and user_email:
        query_str_fetch_old_pass = f"SELECT password FROM \"USER\" WHERE email = '{user_email}'" 
        
        try:
            result = query_func(query_str_fetch_old_pass)
            if not result or len(result) == 0:
                errors.setdefault('old_password', []).append("User not found or error fetching current password.")
            else:
                current_db_password = result[0]['password']
                if current_db_password != old_password_input:
                    errors.setdefault('old_password', []).append("Incorrect old password.")
        except Exception as e:
            errors.setdefault('old_password', []).append("Error verifying old password.")
            
    return errors