# Nebulark RPG
## What Is Nebulark RPG?
Nebulark RPG is an idle rpg discord bot that allows users to go on adventures, gamble, and more.

## Usage
#### Cloning Down The Code
1. Run ```gh repo clone Galacticica/nebulark-rpg```
2. Run ```uv sync```
3. Run ```uv run manage.py migrate```

#### Run Locally
1. Create a ```.env``` file in the discord_bot directory and create a variable ```DISCORD_TOKEN``` with your test bot's token
2. In one terminal, run ```uv run manage.py runserver```
3. In another terminal, run ```uv run discord_bot/main.py```

#### Invite Bot To Server
1. Go to https://discord.com/oauth2/authorize?client_id=756192197967085767 and follow the directions.
2. Run /help in Discord and enjoy!

## Future Plans
- Add test coverage for all endpoints
- Success chance
- Add shops with gear that provides boosts (less time per adventure, more xp, more money, better success chance)
- Interactive adventures
- Stat points

## Contact
### Email : reaganzierke@gmail.com
### Discord : galacticica