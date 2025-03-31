# ChatGPTPaperFilter
Filters a list of papers in RIS format with the OpenAI API.


Setup:
```console
pip install -r requirements.txt
```

Create a file called .env, containing the following:
```
API_KEY = "<api key goes here>"
```
To obtain an API key, visit https://openai.com/ to create an account and purchase API credits.


Configuration: (All options can be found at the top of paperfilter.py)

SEMAPHORE_LIMIT: How many consecutive threads are running. If you're getting rate limited too much, drop this! 
Default: 7

GPTMODEL: Which model of ChatGPT to be used. Tested with gpt-4o and gpt-4o-mini. 
Default: "gpt-4o"

BACKUPDELAY: Time, in seconds, between backups. Backup files are saved as "INPUT_FILENAME.sav", and are deleted once the script completes without error.
Default: 900


Usage:
```console
python paperfilter.py <FILENAME>
```


Outputs three files: output/YES.ris, output/MAYBE.ris, and output/NO.ris