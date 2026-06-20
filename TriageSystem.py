## ============================================================
# Title: Emergency Room Triage System
# Name: Wilford E Kent III

# Description:
# This program simulates a hospital emergency room triage system.
# It allows staff to add patients, assign priorities, view the
# waiting list, treat patients, save records, and load records.
# ============================================================

# Imports
import os


# Constants / Global Values

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATIENT_FILE = os.path.join(BASE_DIR, "er_patients.txt")
TREATED_FILE = os.path.join(BASE_DIR, "treated_patients.txt")


# This list will store patient dictionaries

waiting_list=[]

# This list will store patients who have already been treated

treated_list=[]

# variable to track arrival order
# This helps break ties when two patients have the same priority

arrival_counter = 1


# This function prints the main menu options

def display_menu():
    print("\n" + "=" * 52)
    print("        Emergency Room Triage System")
    print("=" * 52)
    print("1. Add Patient")
    print("2. View All Waiting Patients")
    print("3. View Next Patient")
    print("4. Treate Next Patient")
    print("5. Search For Patient")
    print("6. Remove Patient")
    print("7. Show ER Statkstics")
    print("8. Save Waiting List")
    print("9. Load Waiting List")
    print("10. Save Treated Patients")
    print("11. Exit")
    print("=" * 52)



# Ask the user for a patient name

def get_valid_name():
    while True:
        name = input('Enter patient name ').strip()
        if name == "":
            print('Invalid name try again ')
        else:
            return name

# Ask the user for patient age
# Make sure age is a valid positive number
# Return the valid age

def get_valid_age():
    while True:
        age = input("Enter patient age ").strip()
        if not age.isdigit() or int(age) < 1:
            print("Patient age as to be greater then one or a real digit ")
        else:
            return int(age)
        

# Ask the user to enter symptoms
# Make sure the entry is not blank
# Return the symptom text

def get_valid_symptoms():
    while True:
        symptoms = input("Enter symptoms ").strip()
        if symptoms == "":
            print("Invalid try again ")
        else:
            return symptoms


# Ask the user for pain level from 1 to 10
# Use validation to make sure the number is in range
# Return the pain level as an integer

def get_valid_pain_level():
    while True:
        pain_level = input("Enter pain level 1 - 10 ").strip()
        if not pain_level.isdigit():
            print("Invalid try again ")
        elif int(pain_level) < 1 or int(pain_level) >10:
            print("Invalid pain level try again ")
        else:
            return int(pain_level)



# Use pain level to assign:
# Critical, High, Medium, or Low

def assign_priority(pain_level, symptoms):
    symptoms_lower = symptoms.lower()
    
    emergency_keywords = [
        "chest pain",
        "bleeding",
        "unconscious",
        "trouble breathing",
        "not breathing",
        "seizure",
        "stroke",
        "heart attack"
    ]

    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return "Critical"

    if pain_level >= 9:
        return "Critical"
    elif pain_level >= 6 and pain_level <= 8:
        return "High"
    elif pain_level >= 3 and pain_level <= 5:
        return "Medium"
    else:
        return "Low"



# Convert priority names into numbers for sorting
# Return the numeric rank

def priority_rank(priority):
    if priority == "Critical":
        return 4
    elif priority == "High":
        return 3
    elif priority == "Medium":
        return 2
    elif priority == "Low":
        return 1
    else:
        return 0  

# Sort patients so that:
# 1. Higher priority comes first
# 2. Earlier arrival number comes first if priorities are the same

def sort_waiting_list():
    waiting_list.sort(
        key=lambda patient:(-priority_rank(patient["priority"]),patient["arrival_number"])
    )



# Steps:
# 1. Get valid patient name
# 2. Get valid age
# 3. Get symptoms
# 4. Get pain level
# 5. Assign priority
# 6. Create a patient dictionary
# 7. Add patient to waiting list
# 8. Sort waiting list
# 9. Print confirmation

def add_patient():
    global arrival_counter
    name = get_valid_name()
    age = get_valid_age()
    symptoms = get_valid_symptoms()
    pain_level = get_valid_pain_level()
    priority = assign_priority(pain_level, symptoms)

    patient = {
        "name": name,
        "age": age,
        "symptoms": symptoms,
        "pain level": pain_level,
        "arrival_number": arrival_counter,
        "priority": priority
    }
    waiting_list.append(patient)
    
    arrival_counter += 1
    sort_waiting_list()
    
    print(f"\nPatient {name} added successfully. ")
    print(f"Assigned priority: {priority}" )


# Show every patient currently waiting
def view_all_patients():
    if len(waiting_list) == 0:
        print(f"No patients are currently waiting.")
        return
    
    print("\nCurrent waiting patients")
    print("-" * 80)

    for i, patient in enumerate(waiting_list, start=1):
        print(f"Patient # {i}")
        print(f"Name: {patient['name']}")
        print(f"Age: {patient['age']}")
        print(f"Pain Level: {patient['pain level']}")
        print(f"Priority: {patient['priority']}")
        print(f"Symptoms: {patient['symptoms']}")
        print(f"Arrival Number: {patient['arrival_number']}")
        print("-" * 80)


# Show the highest-priority patient without removing them
# If the waiting list is empty, prints a message
def view_next_patient():
    if len(waiting_list) == 0:
        print(f"No patients are currently waiting.")
        return

    patient = waiting_list[0]
    print("\nNext patient to be treated")   
    print("Patient #1")
    print(f"Name: {patient['name']}")
    print(f"Age: {patient['age']}")
    print(f"Pain level: {patient['pain level']}")
    print(f"Priority: {patient['priority']}")
    print(f"Symptoms: {patient['symptoms']}")
    print(f"Arrival Number: {patient['arrival_number']}")
    print("-" * 80)
    
    
# Remove the first patient from the waiting list
# Add them to the treated list
# Print which patient is being treated
# If no patients are waiting, prints a message

def treat_next_patient():
    if len(waiting_list) == 0:
        print(f"No patients are currently waiting.")
        return  
    
    patient = waiting_list.pop(0)
    treated_list.append(patient)

    print(f"Now treating patient:{patient['name']} ")
    print(f"Priority: {patient['priority']}")
    print(f"Symptoms: {patient['symptoms']}")



# Ask the user for a name to search
# Search the waiting list for matching names
# If found, display patient information
# If not found, prints a message

def search_patient():
    if len(waiting_list) == 0:
        print(f"No patients are currently waiting.")
        return
    search_name = input("Enter a patient name to search ").strip().lower()
    found = False

    for patient in waiting_list:
        if search_name in patient['name'].lower():
            print("\nPatient found")
            print(f"Name: {patient['name']}")
            print(f"Age: {patient['age']}")
            print(f"Pain_level: {patient['pain level']}")
            print(f"Priority: {patient['priority']}")
            print(f"Symptoms: {patient['symptoms']}")
            print(f"Arrival Number: {patient['arrival_number']}")
            print("*" * 50)
            found = True

    if not found:
        print(f"Patient not found in waiting list.")

# Ask the user for a patient name
# Search for that patient in the waiting list
# Remove them if found

def remove_patient():
    if len(waiting_list) == 0:
        print(f"No patients are currently waiting.")
        return

    name_to_remove = input("Enter a patient name to remove ").strip().lower()
    found = False

    for patient in waiting_list:
        if patient['name'].lower() == name_to_remove:
            confirm = input(f"Are you sure you want to remove {patient['arrival_number']}? (y/n): ").strip().lower()

            if confirm == 'y':
                waiting_list.remove(patient)
                print(f"Patient name {patient['name']} removed successfully")
                return
            else:
                print("\nRemoval cancelled ")
                return

    print("\nPatient not found.")



# Display useful ER statistics such as:
# total waiting patients
# total treated patients

def show_statistics():
    critical_count = 0
    high_count = 0
    medium_count = 0
    low_count = 0

    for patient in waiting_list:
        if patient["priority"] == "Critical":
            critical_count += 1
        elif patient["priority"] == "High":
            high_count += 1
        elif patient["priority"] == "Medium":
            medium_count += 1
        elif patient["priority"] == "Low":
            low_count += 1

    print("\nThese are the statistics")
    print("-" * 40)
    print(f"Total waiting patients: {len(waiting_list)}")
    print(f"Treated patients: {len(treated_list)}")
    print(f"Critical patients: {critical_count} ")
    print(f"High patients: {high_count}")
    print(f"Medium patients: {medium_count}")
    print(f"Low Patients: {low_count}")
    



# Save all waiting patients to a text file
def save_to_file():
    try:
        with open(PATIENT_FILE,"w") as file:
            for patient in waiting_list:
                line = (
                    f"{patient['name']}|"
                    f"{patient['age']}|"
                    f"{patient['symptoms']}|"
                    f"{patient['pain level']}|"
                    f"{patient['priority']}|"
                    f"{patient['arrival_number']}\n"  
                )
                file.write(line)

        print(f"\nWaiting list saved {PATIENT_FILE}")
    except Exception as e:
        print(f"\nError saving waiting list: {e}") 
    

# Load patient records from the file
# Read each line
# Split the line into parts
# Rebuild each patient dictionary
# Add patients back into the waiting list

def load_from_file():
    global arrival_counter
     
    if not os.path.exists(PATIENT_FILE):
        print(f"\nNo saved waiting list ({PATIENT_FILE}).")
        return
        
    try:
        waiting_list.clear()

        with open(PATIENT_FILE,"r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 6:
                    patients = {
                        "name": parts[0],
                        "age": int(parts[1]),
                        "symptoms": parts[2],
                        "pain level": int(parts[3]),
                        "priority": parts[4],
                        "arrival_number": int(parts[5])
                    }
                waiting_list.append(patients)

        if waiting_list:
            arrival_counter = max(patient["arrival_number"] for patient in waiting_list) + 1
        else:
            arrival_counter = 1

        sort_waiting_list()
        print(f"\nWaiting list loaded from {PATIENT_FILE}.")
    except Exception as e:
        print(f"\nError loading waiting list: {e}")




# Save treated patients to a separate file

def save_treated_to_file():
    try:
        with open(TREATED_FILE,"w") as file:
            for patient in treated_list:
                line = (
                    f"{patient['name']}|"
                    f"{patient['age']}|"
                    f"{patient['symptoms']}|"
                    f"{patient['pain level']}|"
                    f"{patient['priority']}|"
                    f"{patient['arrival_number']}\n"
                )
            file.write(line)
        print(f"\nTreated patients saved to {TREATED_FILE}")
    except Exception as e:
        print(f"\nError saving treated patients: {e}")

# Optional helper:
# Load saved data automatically when the program starts

def load_startup_data():
    if os.path.exists(PATIENT_FILE):
        try:
            load_from_file()
        except Exception:
            print("Could not load startup data")


# Let the user press Enter before returning to menu
# This improves user experience

def pause():
   input(("\nPress Enter to continue...")) 



# Main Program

def main():
    load_startup_data() 

    while True:
        try:
            display_menu()
            choice = int(input('Enter your choice 1 - 11 ').strip())
            print(f"Choice is equal to {choice}")
        
            if choice == 1:
                add_patient()
            
            elif choice == 2:
                view_all_patients()
            
            elif choice == 3:
                view_next_patient()

            elif choice == 4:
                treat_next_patient()

            elif choice == 5:
                search_patient()

            elif choice == 6:
                remove_patient()

            elif choice == 7:
                show_statistics()

            elif choice == 8:
                save_to_file()

            elif choice == 9:
                load_from_file()

            elif choice == 10:
                save_treated_to_file()

            elif choice == 11:
                save_to_file()
                save_treated_to_file()
                print("Exiting Triage System...")
                break

            else:
                print("\nYou need  pick between 1 - 11")
            
        except ValueError:
            print("\nInvalid input. Please enter a NUMBER (1 - 11).")

        except Exception as e:
            print(f"\nUnexpected error: {e}")
        
        pause()

# -------------------------
# Program Start
# -------------------------
# Call main() here
main()