# SupportBot
WOMBO Support Bot

## Installation:
1. `git clone https://github.com/Skylarr12227/SupportBot`
2. `cd SupportBot`
3. `python3.9 -m pip install -r requirements.txt`
- sometimes there is a conflict the supabase vs supabase-py librarys (working this out)
4. `touch .env`
5. `nano .env` - add the following key:values with the proper keys for the environment.
  - `TOKEN=<BOT TOKEN>`
  - `SUPABASE_URL=<URL OF SUPABASE BEING USED>`
  - `SUPABASE_API_KEY=<API KEY OF SUPABASE USED>`
  - `OPENAI_KEY=<API KEY FOR OPENAI>`
  - `API_LINK=<WOMBO Specific API LINK>` - Anyone reusing this code would leave this out
  - `API_PASS=<ONLY USED BY WOMBO SPECIFICALLY>` - Anyone reusing this code would leave this out
  - `BITLY=<BITLY API KEY>` 

## Standard Run 
1. `cd SupportBot`
2. `python3.9 -m supportbot`

## Running with TMUX 
1. `cd SupportBot`
2. `tmux`
3. `python3.9 -m supportbot` (can be closed now)
4. `tmux attach -t <number of session>` to log into the session
   
# credit for help with code
- Flame442 <3
- Skylarr
