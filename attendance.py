import csv
import os
import math

def create_csv_if_not_exists():
    """Create the Attendance.csv file if it doesn't exist."""
    if not os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Subject', 'Hours per Week', 'Attendance Percentage', 'Leaves Left'])

def floor(x):
    return int(x)

def clear_and_restart():
    """Clear all attendance records and restart the system."""
    # Confirm before clearing
    while True:
        confirm = input("WARNING: This will delete ALL attendance records. Are you sure? (yes/no): ").lower().strip()
        
        if confirm in ['yes', 'y']:
            try:
                # Delete existing file
                if os.path.exists('Attendance.csv'):
                    os.remove('Attendance.csv')
                
                # Recreate the file with headers
                create_csv_if_not_exists()
                
                print("\n--- System Reset ---")
                print("All attendance records have been cleared.")
                print("You can now start adding new subjects.")
                
                # Optional: Immediately prompt to add subjects after reset
                add_now = input("Would you like to add subjects now? (yes/no): ").lower().strip()
                if add_now in ['yes', 'y']:
                    get_multiple_subjects()
                
                break
            except Exception as e:
                print(f"An error occurred while resetting the system: {e}")
                break
        elif confirm in ['no', 'n']:
            print("Reset cancelled. Returning to main menu.")
            break
        else:
            print("Please enter 'yes' or 'no'.")

def remove_subject():
    """Remove a specific subject from the CSV file."""
    # Read existing data
    rows = []
    with open('Attendance.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = list(reader)
    
    # Check if there are any subjects
    if not rows:
        print("No subjects found to remove.")
        return
    
    # Display current subjects
    print("\nCurrent Subjects:")
    for i, row in enumerate(rows, 1):
        print(f"{i}. {row[0]}")
    
    # Select subject to remove
    while True:
        try:
            choice = input("\nEnter the number of the subject to remove (or 'cancel' to exit): ").strip()
            
            # Allow cancellation
            if choice.lower() in ['cancel', 'c']:
                print("Removal cancelled.")
                return
            
            # Convert to index
            index = int(choice) - 1
            
            # Validate index
            if index < 0 or index >= len(rows):
                print("Invalid subject number. Please try again.")
                continue
            
            # Confirm removal
            subject_to_remove = rows[index][0]
            confirm = input(f"Are you sure you want to remove '{subject_to_remove}'? (yes/no): ").lower().strip()
            
            if confirm in ['yes', 'y']:
                # Remove the subject
                removed_subject = rows.pop(index)
                print(f"Removed subject: {removed_subject[0]}")
                
                # Write updated data back to file
                with open('Attendance.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Subject', 'Hours per Week', 'Attendance Percentage', 'Leaves Left'])
                    writer.writerows(rows)
                
                break
            else:
                print("Removal cancelled.")
                break
        
        except ValueError:
            print("Please enter a valid number or 'cancel'.")

def get_multiple_subjects():
    """Add multiple subjects to the CSV file in one go."""
    # Read existing data
    rows = []
    with open('Attendance.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = list(reader)
    
    # Get number of subjects
    while True:
        try:
            num_subjects = int(input("How many subjects do you want to add? "))
            if num_subjects <= 0:
                print("Number of subjects must be a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Input subjects and their details
    for i in range(num_subjects):
        print(f"\nEntering details for Subject {i+1}:")
        
        # Subject name
        while True:
            subject = input("Enter subject name: ").strip()
            if not subject:
                print("Subject name cannot be empty.")
                continue
            
            # Check for duplicate subjects
            if any(row[0].lower() == subject.lower() for row in rows):
                print(f"Subject '{subject}' already exists. Please enter a different name.")
                continue
            
            break
        
        # Hours per week
        while True:
            try:
                hours = float(input("Enter hours per week: "))
                if hours <= 0:
                    print("Hours must be a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")
        
        # Add new subject
        rows.append([subject, str(hours), '0', '0'])
        print(f"Added subject: {subject}")
    
    # Write updated data back to file
    with open('Attendance.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'Hours per Week', 'Attendance Percentage', 'Leaves Left'])
        writer.writerows(rows)
    
    print(f"\nSuccessfully added {num_subjects} subjects.")

def get_subject_details():
    """Provide options to add or remove subjects."""
    while True:
        print("\nSubject Management Menu:")
        print("1. Add Subjects One by One")
        print("2. Add Multiple Subjects at Once")
        print("3. Remove a Subject")
        print("4. Return to Main Menu")
        
        # Get user choice
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            # Existing single subject addition method
            subject = input("Enter subject name: ").strip()
            
            # Read existing data
            rows = []
            subject_exists = False
            with open('Attendance.csv', 'r') as file:
                reader = csv.reader(file)
                headers = next(reader)
                rows = list(reader)
                
                # Check if subject already exists
                for row in rows:
                    if row[0].lower() == subject.lower():
                        subject_exists = True
                        break
            
            # Get hours per week
            while True:
                try:
                    hours = float(input("Enter hours per week: "))
                    if hours <= 0:
                        print("Hours must be a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")
            
            # Update or add subject
            if subject_exists:
                for row in rows:
                    if row[0].lower() == subject.lower():
                        row[1] = str(hours)
                        break
                print(f"Updated details for {subject}")
            else:
                # Default values for new subject
                rows.append([subject, str(hours), '0', '0'])
                print(f"Added new subject: {subject}")
            
            # Write updated data back to file
            with open('Attendance.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Subject', 'Hours per Week', 'Attendance Percentage', 'Leaves Left'])
                writer.writerows(rows)
        
        elif choice == '2':
            get_multiple_subjects()
        
        elif choice == '3':
            remove_subject()
        
        elif choice == '4':
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def update_attendance():
    """Update attendance for a subject."""
    subject = input("Enter subject name: ").strip()
    
    # Read existing data
    rows = []
    subject_found = False
    with open('Attendance.csv', 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = list(reader)
        
        # Find the subject
        for row in rows:
            if row[0].lower() == subject.lower():
                subject_found = True
                
                # Get total classes
                while True:
                    try:
                        total_classes = int(input("Enter total number of classes taken: "))
                        if total_classes < 0:
                            print("Total classes cannot be negative.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number.")
                
                # Get classes attended
                while True:
                    try:
                        classes_attended = int(input("Enter number of classes attended: "))
                        if classes_attended < 0 or classes_attended > total_classes:
                            print("Invalid number of classes attended.")
                            continue
                        break
                    except ValueError:
                        print("Please enter a valid number.")
                
                # Calculate attendance percentage
                attendance_percentage = (classes_attended / total_classes) * 100 if total_classes > 0 else 0
                row[2] = f"{attendance_percentage:.2f}"
                
                # Calculate leaves left (assuming 80% attendance is required)
                max_missed_classes = floor(float(row[1]) * 2.8)
                leaves_left = max_missed_classes - (total_classes - classes_attended)
                row[3] = f"{leaves_left:.0f}"
                
                print(f"Updated attendance for {subject}")
                break
        
        # Subject not found
        if not subject_found:
            print(f"Subject {subject} not found. Please add subject details first.")
            return
    
    # Write updated data back to file
    with open('Attendance.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Subject', 'Hours per Week', 'Attendance Percentage', 'Leaves Left'])
        writer.writerows(rows)

def print_attendance():
    """Print all details from the CSV file."""
    try:
        with open('Attendance.csv', 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)
            
            # Print headers
            print("\n" + " | ".join(headers))
            print("-" * 50)
            
            # Print rows
            for row in reader:
                print(" | ".join(row))
    except FileNotFoundError:
        print("No attendance records found. Please add subjects first.")

def main():
    # Ensure CSV file exists
    create_csv_if_not_exists()
    
    while True:
        # Display menu
        print("\n--- Attendance Management System ---")
        print("1. Add/Update Subject Details")
        print("2. Update Attendance")
        print("3. View Attendance Records")
        print("4. Clear and Restart System")
        print("5. Exit")
        
        # Get user choice
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                get_subject_details()
            elif choice == '2':
                update_attendance()
            elif choice == '3':
                print_attendance()
            elif choice == '4':
                clear_and_restart()
            elif choice == '5':
                # Confirm exit
                confirm = input("Are you sure you want to exit? (yes/no): ").lower().strip()
                if confirm in ['yes', 'y']:
                    print("Exiting Attendance Management System.")
                    break
                else:
                    continue
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
