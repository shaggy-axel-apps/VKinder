# Vkinder
 - [Technical Requirements](https://github.com/shaggy-axel/VKinder/blob/master/TECH_REQUIREMENTS.md)

## Installation
```bash
# clone repo and go to the folder VKinder
git clone https://github.com/shaggy-axel/VKinder.git && cd VKinder

# setup virtualenvironment, activate and install dependencies from requirements.txt
python3.9 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

> in the env_sample I save all secret keys, in terminal run command:
> `cat env_sample > .env`, than add required keys in `.env` file

## Setup Bot-Group in VK
### Get Token
1. create community in VK
2. Go to Manage -> API Usage. Create token
![image](https://user-images.githubusercontent.com/12861849/114929451-7c907380-9e3c-11eb-8a1a-44597b634a5c.png)
3. Turn on sending messages in group. Manage -> Messages -> Community messages: Enabled.
4. Bot Settings. Bot abilities: Enabled.
- [x] Add Start button 
- [x] Ability to add this community to chats
![image](https://user-images.githubusercontent.com/12861849/114929568-a0ec5000-9e3c-11eb-8ea4-cafa0dc56b59.png)

## Usage
```bash
. .venv/bin/activate

# migrate database tables
python src/manage.py migrate

# start vk-bot longpoll
python src/manage.py start
```