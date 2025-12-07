import os
import smtplib
import csv
import random
from dotenv import load_dotenv

#TESTING:
def evaluate_gifting_pairs(user_data, present_count):
    print()
    for name, data in user_data.items():
        if len(data['gifting_to']) != present_count:
            print(f"Incorrect gifting pairs found: Participant '{name}' is assigned to gift {len(data['gifting_to'])} participants instead of {present_count}.")
            return False
            
        if data['number_of_unassigned_gifters'] != 0:
            print(f"Incorrect gifting pairs found: Participant '{name}' has been only gifted {data['number_of_unassigned_gifters']} gifts instead of {present_count}.")
            return False
        prior_gifts = []
        for i in data['gifting_to']:
            if i in prior_gifts:
                print("Incorrect gifting pairs found: A participant has been assigned to gift the same person more than once.")
                return False
            prior_gifts.append(i)
    print("All gifting pairs have been correctly assigned.")
    return True


#HELPER FUNCTIONS
def emailing(from_address, password, to_address, message="", login_trial=False, debug=False, verbose=False):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        if verbose:
            smtp.set_debuglevel(True) 
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        subject = "Your Secret Santa Gift List"
        body = message

        msg = f'To:{to_address}\nSubject: {subject}\n\n{body}'

        try:
            smtp.login(from_address, password)
            if login_trial:
                return True
        except Exception as e:
            print(f"Login failed. Check your email and password.")
            if debug:
                print(f"Error: {e}")
            return False

        try:
            smtp.sendmail(from_address, to_address, msg.encode('utf-8'))
        except Exception as e:
            print(f"Failed to send email to {to_address} from {from_address}.")
            if debug:
                print(f"Error: {e}")
            return False
        return True

def display_user_data(user_data, present_count):
    internal_counter = 0
    removal_list = []
    print()
    print(f"Current participant data (Number of Gifts per participant: {present_count}):")
    for name, data in user_data.items():
        removal_list.append(name)
        internal_counter += 1
        print(f"{internal_counter}. Name: {name}, Email: {data['email']}, Address: {data['address']}, Gifting To: {data['gifting_to']}")
    return internal_counter, removal_list

def delete_user_data_entry(user_data, removal_list, internal_counter):
    inside_in_valid = False
    while not inside_in_valid:
        inside_in_valid = True
        print()
        delete_name = input("Please enter the line number of the participant you wish to delete or press enter to cancel: ")
        if delete_name == '':
            break
        try:
            delete_name = int(delete_name)
            if delete_name < 1 or delete_name > internal_counter:
                print(f"Invalid input: {delete_name}. Please enter an integer 1 to {internal_counter} corresponding to the participant number.")
                inside_in_valid = False
                continue
            else:
                deletion_result = input(f"Are you sure you want to delete participant {removal_list[delete_name - 1]}? Type 'y' to confirm, or any other key to cancel: ")
                if deletion_result.lower() != 'y':
                    inside_in_valid = False
                    continue
        except:
            print(f"Invalid input: '{delete_name}'. Please enter a valid integer corresponding to the participant number.")
            inside_in_valid = False
            continue
    if delete_name != '':
        del user_data[removal_list[delete_name - 1]]
    return user_data

def import_user_data_from_file(filename, present_count):
    user_data = {}
    valid = True
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            counter = 0
            for row in reader:
                counter += 1
                if (len(row) < 2):
                    print(f"Invalid row in CSV file, Row number {counter}: {row}. Each row must contain at least a name and an email.")
                    valid = False
                    break
                elif '@' not in row[1]:
                    print(f"Invalid email address in CSV file, Row number {counter}: '{row[1]}'. Please ensure the email address is valid and is located in the second column.")
                    valid = False
                    break
                elif row[0] in user_data.keys():
                    print(f"Duplicate name found in CSV file, Row number {counter}: {row[0]}. Each participant must have a unique name or nickname for clarity.")
                    valid = False
                    break
                elif row[1] in [data['email'] for data in user_data.values()]:
                    print(f"Duplicate email address found in CSV file, Row number {counter}: '{row[1]}'. Each participant must have a unique email address.")
                    valid = False
                    break
                    
                user_data[row[0]] = {'email': row[1], 'address': 'N/A', 'gifting_to': [], 'number_of_unassigned_gifters': present_count}
            
                if len(row) > 2:
                    user_data[row[0]]['address'] = row[2]
    except:
        print(f"Failed to read the file '{filename}'. Please ensure the file exists and is accessible as a csv.")
        valid = False

    return user_data, valid
    
def import_user_data_from_terminal(present_count, prior_count=1, prior_user_data={}):
    user_data = prior_user_data.copy()
    result = 1
    counter = prior_count

    while result != 4:        
        inside_valid = False
        while not inside_valid:
            inside_valid = True
            print()
            name = input(f"Please enter the name of participant #{counter}: ")
            if name in user_data.keys():
                print(f"The name '{name}' has already been entered. Each participant must have a unique name or nickname for clarity.")
                inside_valid = False
                continue

        inside_valid = False
        while not inside_valid:
            inside_valid = True
            print()
            email = input(f"Please enter the email of participant #{counter} ({name}): ")
            if '@' not in email:
                print(f"Invalid email address: '{email}'. Please ensure the email address is valid.")
                inside_valid = False
                continue
            elif email in [data['email'] for data in user_data.values()]:
                print(f"Duplicate email address found: '{email}'. Each participant must have a unique email address.")
                inside_valid = False
                continue
        
        print()
        address = input(f"Please enter the address of participant #{counter} ({name}), or simply press enter to skip: ")
        if address == '':
            address = 'N/A'

        user_data[name] = {'email': email, 'address': address, 'gifting_to': [], 'number_of_unassigned_gifters': present_count}
        print(f"Added participant: {name}.")

        inside_valid = False
        while not inside_valid:
            inside_valid = True
            print()
            result = input("Press (1) to add another participant, press (2) to view all participant data, press (3) to delete a participant, or press (4) to finish entering participants: ")
            try:
                result = int(result)
                if result < 1 or result > 4:
                    print(f"Invalid input: {result}. Please enter an integer between 1 and 4.")
                    inside_valid = False
                    continue
            except:
                print(f"Invalid input: '{result}'. Please enter a valid integer between 1 and 4.")
                inside_valid = False
                continue

            if result == 2 or result == 3:
                inside_valid = False
                internal_counter, removal_list = display_user_data(user_data, present_count)

                if result == 4:
                    continue_entering = input("Enter 'y' to confirm finishing entering participants, or any other key to continue entering participants: ")
                    if continue_entering.lower() != 'y':
                        inside_valid = False

                if result == 3:
                    user_data = delete_user_data_entry(user_data, removal_list, internal_counter)
        counter += 1

    return user_data


#MAIN FUNCTIONS
def get_present_count():
    inside_valid = False
    while not inside_valid:
        inside_valid = True
        print()
        present_count = input(f"Please enter the number of gifts each participant will buy and recieve or simply press enter to be autofilled: ")
        if present_count == '':
            present_count = 1
        try:
            present_count = int(present_count)

            if present_count < 0:
                print(f"Invalid gift count: {present_count}. The gift count must be at least 0.")
                inside_valid = False
                continue
        except:
            print(f"Invalid gift count: '{present_count}'. The gift count must be an integer.")
            inside_valid = False
            continue
    return present_count

def message_user_input(present_count, debug=False):
    message_source = 1
    if not debug:
        message_source = -1
        while message_source != 1 and message_source != 2:
            if (message_source != -1):
                print("Invalid input. Please enter only the number 1 or the number 2.")
            print()
            input_value = input("Please enter (1) to import the message from a text file, or (2) to type your own message: ")

            try:
                message_source = int(input_value)
            except:
                message_source = 100
    
        valid = False
        while not valid:
            valid = True
            print()
            print("Messages can use [reciever_name], [gifter_name], and [reciver_address] as placeholders in the message as needed.")
            if message_source == 1:
                input_file = input("Please enter the file name of the text file containing the message that will be used in the email: ")
                try:
                    with open(input_file, 'r') as file:
                        message = file.read()
                except:
                    print(f"Failed to read the file '{input_file}'. Please ensure the file exists and is accessible.")
                    valid = False
            else:
                message = input("Please enter the message you want to be used in the email: ")

            if "[gifter_name]" not in message:
                print("The message will not send the name of who the user needs to gift their present to. Please include [gifter_name] in the message.")
                valid = False
            else:
                temp_msg = message
                temp_msg = temp_msg.replace("[gifter_name]", "GIFTER_NAME").replace("[receiver_name]", "RECEIVER_NAME").replace("[receiver_address]", "RECEIVER_ADDRESS")
                print("Please confirm this is your intended message. Note that your parameters to be replaced should be replaced in this message without brackets and in caps:")
                print()
                print("\'" + temp_msg + "\'")
                print()
                confirmation = input("Type 'y' to confirm, or any other key to re-enter the message: ")
                if confirmation.lower() != 'y':
                    valid = False


        user_source = -1
        while user_source != 1 and user_source != 2:
            if (user_source != -1):
                print("Invalid input. Please enter only the number 1 or the number 2.")
            print()
            input_value = input("Please enter (1) to import the user data of the participants from a csv file, or (2) to enter in the information manually: ")

            try:
                user_source = int(input_value)
            except:
                user_source = 100

        valid = False
        while not valid:
            valid = True
            print()
            
            if user_source == 1:
                print("Each line should contain two or three elements seperated by commas.")
                print("the first being the name, second being the email,  and third (optionally) containing their address.")
                print("Ensure the csv file does not contain a header row.")
                print()
                input_file = input("Please enter the file name of the csv file containing the user data of the participants: ")
                user_data, valid = import_user_data_from_file(input_file, present_count)
            else:
                user_data = import_user_data_from_terminal(present_count)
    
    else:
        with open('message.txt', 'r') as file:
            message = file.read()
        user_data, valid = import_user_data_from_file('list.csv', present_count)
        
    return message, user_data

def determine_gifting_pairs(user_data, present_count):
    while present_count >= len(list(user_data.keys())):
        adjustment_choice = -1
        while adjustment_choice != 1 and adjustment_choice != 2:
            if (adjustment_choice != -1):
                print("Invalid input. Please enter only the number 1 or the number 2.")
            print()
            print("Not enough participants to assign gifting pairs based on the current gift count per participant. Please adjust the gift count or add more participants.")
            input_value = input("Enter (1) to adjust gift count or (2) to add more participants: ")
            
            try:
                adjustment_choice = int(input_value)
            except:
                adjustment_choice = 100

        if adjustment_choice == 1:
            present_count = get_present_count()
            for name in user_data.keys():
                user_data[name]['gifting_to'] = []
                user_data[name]['number_of_unassigned_gifters'] = present_count
        else:
            user_data = import_user_data_from_terminal(present_count, prior_count=len(user_data)+1, prior_user_data=user_data)

    round = 1
    while round != present_count + 1:
        gifting_dict = {}
        minimum_len = len(list(user_data.keys()))
        giver = None
        for name, data in user_data.items():
            if len(data['gifting_to']) == round - 1:
                gifting_dict[name] = []
                for other_name, other_data in user_data.items():
                    if other_name != name and other_name not in data['gifting_to'] and other_data['number_of_unassigned_gifters'] == present_count - round + 1:
                        gifting_dict[name].append(other_name)
                if len(gifting_dict[name]) < minimum_len:
                    minimum_len = len(gifting_dict[name])
                    giver = name
        if len(list(gifting_dict.keys())) == 0:
            round += 1
            continue
        reciever = random.choice(gifting_dict[giver])
        user_data[giver]['gifting_to'].append(reciever)
        user_data[reciever]['number_of_unassigned_gifters'] -= 1
        
    return user_data, present_count

def emailing_users(user_data, message, from_address, password, debug=False, verbose=False):
    invalid_emails = 0
    total_emails = len(list(user_data.keys()))
    print()
    for name, data in user_data.items():
        names = ""    
        addresses = ""
        for gifting_to in data['gifting_to']:
            names = names + gifting_to + ", "
            addresses = addresses + user_data[gifting_to]['address'] + ", "
        names = names[:-2]
        addresses = addresses[:-2]
        
        personalized_message = message.replace("[gifter_name]", name)
        personalized_message = personalized_message.replace("[receiver_name]", names)
        personalized_message = personalized_message.replace("[receiver_address]", addresses)
        email_success = emailing(from_address, password, data['email'], personalized_message, False, debug, verbose)
        if email_success:
            print(f"Email successfully sent to {name} ({data['email']}) for gifting.")
        else:
            print(f"Failed to send email to {name} ({data['email']}) for gifting.")
            invalid_emails += 1
    print()
    print(f"Emailing complete. {total_emails - invalid_emails} out of {total_emails} emails were sent successfully.")
    return invalid_emails

def save_pairs_to_file(user_data, debug=False):
    filename = "gifting_pairs.txt"
    if not debug:
        valid = False
        while not valid:
            valid = True
            print()
            filename = input("Please enter the file to store all gifting pairs for record keeping, press enter to automatically name the file, or press 'n' to skip saving: ")
            if filename == '':
                filename = "gifting_pairs.txt"
            elif filename.lower() == 'n':
                return '', True
            elif filename.lower().endswith('.txt') == False:
                print("Invalid file name. Please ensure the file name ends with .txt")
                valid = False
            else:
                saving = input(f"Are you sure you want to save the gifting pairs to the file '{filename}'? Type 'y' to confirm or press enter to cancel: ")
                if saving.lower() != 'y':
                    valid = False
    try:
        with open(filename, 'w') as file:
            file.write(f"Gifting Matches:\n")
            for name, data in user_data.items():
                list_len = len(data['gifting_to'])
                counter = 0
                names = f'Participant: {name}, Gifting To: '
                for gifting_to in data['gifting_to']:
                    counter += 1
                    if counter == list_len and list_len != 1:
                        names += 'and ' + gifting_to
                    elif list_len != 2 and list_len != 1:
                        names += gifting_to + ", "
                    elif list_len == 1:
                        names += gifting_to
                    else:
                        names += gifting_to + " "
             
                file.write(f"{names}\n")
        if not debug:
            print()
            print(f"Gifting pairs successfully saved to '{filename}'.")
            print()
            print(f"Please check if the file '{filename}' contains the correct gifting pairs for your records.")
            continue_or_exit = input("Press 'y' to continue, press any key to exit: ")
            if continue_or_exit.lower() != 'y':
                return filename, False
        return filename, True
    except:
        print(f"Failed to save gifting pairs to the file '{filename}'. Please ensure the file is accessible.")
        return filename, False
    

def main():
    load_dotenv()
    from_address = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("PASSWORD")

    debug = False
    verbose = False
    input_val = input("Welcome to the Secret Santa Emailer! Press enter to continue. ")
    
    if len(input_val) > 0 and input_val.lower()[0] == 'd':
        debug = True
    if len(input_val) > 0 and input_val.lower()[0] == 'v' or (len(input_val) > 1 and input_val.lower()[1] == 'v'):
        verbose = True
        debug = True
    if debug:
        print("Debug mode activated.")
        present_count = 1
    else:
        present_count = get_present_count()
        
    message, user_data = message_user_input(present_count, debug)
    print("User data prior to matching shown below:")
    display_user_data(user_data, present_count)
    user_data, present_count = determine_gifting_pairs(user_data, present_count)
    
    filename, valid = save_pairs_to_file(user_data, debug)

    if valid:
        emailing_users(user_data, message, from_address, password, debug, verbose)

        if debug:
            display_user_data(user_data, present_count)
            evaluate_gifting_pairs(user_data, present_count)
    
    print()
    print("Thank you for using the Secret Santa Emailer! Goodbye.")

if __name__ == "__main__":
    main()
