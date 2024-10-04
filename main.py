import requests
import inquirer
from colorama import init, Fore, Style
import datetime
import time

wait_fight = 5 # 5 detik jeda fight

def read_tokens_from_file():
    with open('tokens.txt', 'r') as file:
        tokens = [line.strip() for line in file if line.strip()]
    return tokens

def create_headers(token):
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.8",
        "Authorization": f"tma {token}",
        "Content-Type": "application/json",
        "Origin": "https://staggering.tonkombat.com",
        "Referer": "https://staggering.tonkombat.com/",
        "Sec-CH-UA": '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }

def user_info(token):
    url = 'https://liyue.tonkombat.com/api/v1/users/me'
    headers = create_headers(token)  # Create headers for this token
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def user_kombat(token):
    url = 'https://liyue.tonkombat.com/api/v1/combats/me'
    headers = create_headers(token)  # Create headers for this token
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('data')
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def user_energy(token):
    url = 'https://liyue.tonkombat.com/api/v1/combats/energy'
    headers = create_headers(token)  # Create headers for this token
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result.get('data')
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def user_balance(token):
    url = 'https://liyue.tonkombat.com/api/v1/users/balance'
    headers = create_headers(token)  # Create headers for this token
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        balance_nano = result.get("data", 0)  # Get the balance in nanoTON
        balance_ton = balance_nano / 1_000_000_000  # Convert to TON
        return balance_ton
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

import requests

def user_task_list(token):
    url = 'https://liyue.tonkombat.com/api/v1/tasks/progresses'
    headers = create_headers(token)  # Create headers for this token
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        # Print the tasks
        if "data" in result:
            tasks = result["data"]  # Corrected the variable name here
            for task in tasks:
                if task.get('task_user') is None:  # Check if task_user is null
                    complete_task(token, task)  # Assuming complete_task is defined
                # else:
                #     print(f"Task {task['name']} is already completed by user.")
        else:
            print("No tasks found.")
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None


def complete_task(token, task):
    url = f"https://liyue.tonkombat.com/api/v1/tasks/{task['id']}"
    headers = create_headers(token)
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"================================")
        print(Fore.GREEN + f"Task Name : {task['name']}")
        print(Fore.GREEN + f"Reward : {task['reward_amount']}")
        print(Fore.GREEN + f"Status : completed! ")
        return result['data']
    else:
        print("Error:", response.status_code, response.text)
        return None

def user_claim(token):
    url = 'https://liyue.tonkombat.com/api/v1/users/claim'
    headers = create_headers(token)

    # You can define your payload here; adjust as necessary
    payload = {}  # Assuming no specific data is needed for the claim, modify as needed

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + f'Token claimed!')
        return result
    elif response.status_code == 400: 
        result = response.json()
        print(Fore.RED + f"{result['message']}")
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def user_last_claim(token):
    url = 'https://liyue.tonkombat.com/api/v1/users/last_claim'
    headers = create_headers(token)
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        last_claim_time = result.get("data")  # This should return the string directly
        print("Last Claim Time:", last_claim_time)
        return last_claim_time
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None
        
def onboard(token):
    url = 'https://liyue.tonkombat.com/api/v1/users/onboard'
    questions = [
        inquirer.List('house_id', message="Choose your house kombat", choices=[
            (Fore.YELLOW + f'[0] Hamster Kombat [ATK:⭐️⭐️⭐️⭐️⭐️⭐️   HP:⭐️⭐️⭐️   Luck:⭐️]',0),
            (Fore.YELLOW + f'[1] Tap Swap [ATK:⭐️⭐️⭐️⭐️⭐️⭐️   HP:⭐️⭐️   Luck:⭐️⭐️]',1),
            (Fore.YELLOW + f'[2] Notcoin [ATK:⭐️⭐️   HP:⭐️⭐️⭐️⭐️⭐️⭐️   Luck:⭐️⭐️]',2),
            (Fore.YELLOW + f'[3] Yescoin [ATK:⭐️⭐️   HP:⭐️⭐️⭐️   Luck:⭐️⭐️⭐️⭐️⭐️]',3),
            (Fore.YELLOW + f'[4] Blum [ATK:⭐️⭐️⭐️   HP:⭐️⭐️⭐️⭐️   Luck:⭐️⭐️⭐️]',4),
            (Fore.YELLOW + f'[5] Catizen [ATK:⭐️⭐️⭐️⭐️   HP:⭐️⭐️⭐️⭐️   Luck:⭐️⭐️]',5),
            (Fore.YELLOW + f'[6] Seed [ATK:⭐️⭐️⭐️   HP:⭐️⭐️⭐️⭐️⭐️⭐️   Luck:⭐️]',6),
            (Fore.YELLOW + f'[7] Dogs [ATK:⭐️⭐️⭐️   HP:⭐️⭐️   Luck:⭐️⭐️⭐️⭐️⭐️]',7)
        ], default=0),
    ]
    house_id = inquirer.prompt(questions)['house_id']
    payload = {"house_id": house_id}
    headers = create_headers(token)  # Create headers for this token
    response = requests.post(url, json=payload, headers=headers)  # Use json=payload for JSON body

    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + f"Welcome onboard {result['data']['username']}")
        return result
    else:
        print("Error:", response.status_code, response.text)
        return None

def countdown_to_next_claim(last_claim_time):
    if not isinstance(last_claim_time, str):
        print("Invalid last claim time. Expected a string but got:", type(last_claim_time))
        return
    
    # Check if the last_claim_time is in the correct format
    if last_claim_time.endswith("Z"):
        last_claim_dt = datetime.datetime.fromisoformat(last_claim_time[:-1])  # Remove the 'Z'
    else:
        print("Invalid last claim time format:", last_claim_time)
        return

    next_claim_dt = last_claim_dt + datetime.timedelta(hours=6, minutes=30)
    
    while True:
        now = datetime.datetime.utcnow()
        remaining_time = next_claim_dt - now
        
        if remaining_time.total_seconds() <= 0:
            print("It's time to claim!")
            break
        
        hours, remainder = divmod(remaining_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print(f"Time until next claim: {int(hours):02}:{int(minutes):02}:{int(seconds):02}", end='\r')
        time.sleep(1)

def find_combats(token):
    url = 'https://liyue.tonkombat.com/api/v1/combats/find'
    headers = create_headers(token)  # Create headers for this token
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result
    elif response.status_code == 404: 
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def fight_in_combat(token):
    url = 'https://liyue.tonkombat.com/api/v1/combats/fight'
    headers = create_headers(token)  # Create headers for this token
   
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        return result['data']
    elif response.status_code == 404: 
        print("Error 404: Resource not found. Message:", response.json())
        return None
    elif response.status_code == 400:
        error_message = response.json()
        message = error_message.get('message', 'No message provided')
        print(f"Error 400: {message}")
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def get_user_equipments(token):
    url = 'https://liyue.tonkombat.com/api/v1/equipments/me'
    headers = create_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        if "data" in result and result["data"]:
            # Return the equipment data
            return result["data"]
        else:
            print("No equipment found.")
            return None
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
        return None
    else:
        print("Error:", response.status_code, response.text)
        return None

def equip_item(token, equipment_id):
    url = f'https://liyue.tonkombat.com/api/v1/equipments/{equipment_id}/equip'
    headers = create_headers(token)
    
    response = requests.patch(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + f'Successfully equipped item: {result["data"]}')
        return result["data"]
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
    else:
        print("Error:", response.status_code, response.text)

def upgrade(token):
    # Define the upgrade types
    upgrade_types = ['mining-tok', 'pocket-size', 'honor']
    print(Fore.GREEN + "-------------------- [   Upgrades   ] --------------------")
    for upgrade_type in upgrade_types:
        while True:
            url = 'https://liyue.tonkombat.com/api/v1/upgrades'
            headers = create_headers(token)
            upgrade_data = {'type': upgrade_type}
            
            # Make the POST request with the upgrade data
            response = requests.post(url, json=upgrade_data, headers=headers)
            
            if response.status_code == 200:
                # Success, no additional data provided
                print(Fore.YELLOW + f"{upgrade_type} upgrade successful!")
            elif response.status_code == 400:
                # Handle the specific error for insufficient balance
                error_response = response.json()
                if error_response.get("code") == "invalid-request" and "not enough tok to upgrade" in error_response.get("message"):
                    print(Fore.RED + f"Error: Not enough tokens to upgrade {upgrade_type}.")
                    break  # Exit the while loop for this upgrade type
                else:
                    print(f"Error: {error_response}")
                    break  # Exit on other errors
            else:
                # Handle other errors
                print(f"Error: {response.status_code}, {response.text}")
                break  # Exit on other errors

def count_upgrade_types(data):
    upgrade_counts = {
        "pocket-size": 0,
        "honor": 0,
        "mining-tok": 0
    }
    upgrades = data.get("upgrades")
    if upgrades is None:
        print("No upgrades found.")
        return upgrade_counts
    
    if not isinstance(upgrades, list):
        print("Upgrades is not a list.")
        return upgrade_counts

    for upgrade in upgrades:
        upgrade_type = upgrade.get("upgrade_type")
        if upgrade_type in upgrade_counts:
            upgrade_counts[upgrade_type] += 1

    return upgrade_counts


def daily_reward(token):
    url = 'https://liyue.tonkombat.com/api/v1/daily'
    headers = create_headers(token)  # Assuming you have a function to create headers
    response = requests.post(url, headers=headers)
    print(f'result {response.status_code}')
    if response.status_code == 200:
        result = response.json()
        print(Fore.GREEN + "Daily reward claimed successfully!")
        return result
    elif response.status_code == 400:
        result = response.json()
        print(Fore.GREEN + f'{result['message']}')
        return None
    else:
        print(Fore.RED + f"Error: {response.status_code}, {response.text}")
        return None

def spend_stars(token):
    url = 'https://liyue.tonkombat.com/api/v1/users/stars/spend'
    headers = create_headers(token)  # Assuming you have a function to create headers
    payload = {"type": "upgrade-army-rank"}
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    if response.status_code == 200:
        print("Success Upgrade army rank")
    elif response.status_code == 404:
        print("Error 404: Resource not found. Message:", response.json())
    elif response.status_code == 400:
        print(result['message'])
    else:
        print("Error:", response.status_code, response.text)

def countdown_timer(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f'Time remaining: {timer}', end='\r')
        time.sleep(1)
        seconds -= 1
    print("Time's up!")

if __name__ == '__main__':
    banner = r"""███╗   ███╗ █████╗ ██╗  ██╗██╗██████╗  █████╗     ██████╗ ███████╗██╗   ██╗          
████╗ ████║██╔══██╗██║  ██║██║██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██║   ██║          
██╔████╔██║███████║███████║██║██████╔╝███████║    ██║  ██║█████╗  ██║   ██║          
██║╚██╔╝██║██╔══██║██╔══██║██║██╔══██╗██╔══██║    ██║  ██║██╔══╝  ╚██╗ ██╔╝          
██║ ╚═╝ ██║██║  ██║██║  ██║██║██║  ██║██║  ██║    ██████╔╝███████╗ ╚████╔╝           
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝  ╚═══╝            
████████╗ ██████╗ ███╗   ██╗    ██╗  ██╗ ██████╗ ███╗   ███╗██████╗  █████╗ ████████╗
╚══██╔══╝██╔═══██╗████╗  ██║    ██║ ██╔╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
   ██║   ██║   ██║██╔██╗ ██║    █████╔╝ ██║   ██║██╔████╔██║██████╔╝███████║   ██║   
   ██║   ██║   ██║██║╚██╗██║    ██╔═██╗ ██║   ██║██║╚██╔╝██║██╔══██╗██╔══██║   ██║   
   ██║   ╚██████╔╝██║ ╚████║    ██║  ██╗╚██████╔╝██║ ╚═╝ ██║██████╔╝██║  ██║   ██║   
   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   
                                                                                                                                                                     
    github: https://github.com/mahiradev1
    tg: t.me/airdropdigitalcuan
                                                                                     """

    print(banner)

    tokens = read_tokens_from_file()
    questions = [
        inquirer.List(
            'choose',
            message=Fore.GREEN+f"Choose you want",
            choices=[
                (Fore.YELLOW+f"[1] Daily, Upgrade & Fight", "1"),
                (Fore.YELLOW+f"[2] Change Equipment", "2"),
            ]
        )
    ]
    choose = inquirer.prompt(questions)['choose']

    for token in tokens:
        user_info_result = user_info(token)
        upgrades = count_upgrade_types(user_info_result['data'])
    
        if user_info_result is None:
            print(Fore.RED + "User info not found. Running onboard...")
            onboard(token)
            continue

        if choose == '1':
            balance = user_balance(token)
            user = user_kombat(token)
            energy = user_energy(token)
            print(Style.RESET_ALL + "===================== [   👻👻 " + Fore.YELLOW + user["username"] + Style.RESET_ALL + " 👻👻   ] =====================")
            print(Fore.YELLOW + f'Rank: {user["rank"]}')
            print(Fore.YELLOW + f'Balance: {balance} $TOK')
            print(Fore.YELLOW + f'Energy: {energy["current_energy"]}')
            print(Fore.YELLOW + f'Mining Tok Level: {upgrades["mining-tok"]}')
            print(Fore.YELLOW + f'Pocket Size Level: {upgrades["pocket-size"]}')
            print(Fore.YELLOW + f'Honor Level: {upgrades["honor"]}')
            print(Fore.YELLOW + f'Skill: {user["pet"]["active_skill"]}')
            daily_reward(token)
            user_claim(token)
            user_task_list(token)
            upgrade(token)
            spend_stars(token)
            while energy["current_energy"] > 0:
                combats = find_combats(token)
                print(Fore.CYAN + f'⚔️===========Fight===========⚔️')
                if combats and "data" in combats:
                    combats = fight_in_combat(token)  # Get the winner
                    winner = combats["winner"]  # Extract the winner status
                    enemy = combats["enemy"]["username"]
                    enemy_rank = combats["enemy"]["rank"]
                    print(Fore.GREEN + f"Enemy username : {enemy},")  
                    print(Fore.GREEN + f"Enemy Rank : {enemy_rank},")  
                    print(Fore.GREEN + f"Winner : {winner},")  
                    energy = user_energy(token)  # Refresh the energy after fighting
                    print(Fore.GREEN + f"Your current energy : {energy['current_energy']}")
                    if energy["current_energy"] <= 0:
                        print(Fore.RED + "No more energy left!")
                        break
                    time.sleep(wait_fight)  # Adjust as necessary
                else:
                    print(Fore.RED + "No available combats found.")
                    break
        elif choose == '2':
            equipment_data = get_user_equipments(token)
            if equipment_data:
                choices = [(f"{Fore.YELLOW}[{i+1}] {equipment['name']}", equipment['id']) for i, equipment in enumerate(equipment_data)]
                choices.append((Fore.YELLOW + "[0] Cancel", "0"))  # Option to cancel

                questions = [
                    inquirer.List(
                        'items',
                        message=Fore.GREEN + "Choose your item to equip:",
                        choices=choices
                    )
                ]
                user_choice = inquirer.prompt(questions)['items']

                if user_choice != "0":  # User selected an item
                    equip_item(token, user_choice)
                else:
                    print(Fore.RED + "Operation cancelled.")

    countdown_timer(600)