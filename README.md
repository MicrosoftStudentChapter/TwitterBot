# Tech News by MLSC

Tech News delivered to you weekly on Discord and Twitter

### Installation
Install [python and pip](https://www.python.org/downloads/) and add them in your environment Path.

### Usage
Let's install a virtual env in your PC

```bash
pip install venv
```

Now cd to the directory Cloned
### Virtual Python Environment
``` bash
python -m venv env
source env/bin/activate
```

A small (env) will be behind your hostname in your bash terminal which means a virtual python env. is created and hence the changes done over here won't affect your actual machine's python. You can exit from this env by Reopening your terminal or by sourcing your `.bashrc` or `.zshrc`

Alternatively, you can use poetry, if you change the environment using poetry, run make or make requirements to update the `requirements.txt`.

### Installing requirements

```bash
pip install -r requirements.txt
```

### env Variables

Create a `.env` file or rename `.env.example` to `.env` and supply the credentials as demanded.

### Running the Bot(s)

Congrats, Now there are a few Bots which can be used  following the successful installation of modules

```bash
python reddit/reddit-comp.py #Run the Reddit News Compilation ONLY
```

```bash
python discord_bot/discord_main.py #Run Discord bot (By default all COGs are active run `.help` to lookup commands
```
    
```bash
python twitter/twitter_main.py #Run Twitter bot
```
