import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, RateLimitError
import rispy


async def apiCall(index, entry):
  paperPrompt = f"""
    Title: {entry['title']}
    Year: {entry['year']}
    Abstract: {entry['notes_abstract']}
  """
  if (index in backupDict):
    return ["Backup", entry, backupDict[index], index]
  async with semaphore:
    activeTasks += 1
    while True:
      try:
        response = await client.chat.completions.create(
          model="gpt-4o",
          messages=[sysPrompt, {"role": "user", "content": paperPrompt}]
        )
        return ["Valid", entry, response, index]
      except RateLimitError as e:
        print("Rate limited! Waiting 10s...")
        await asyncio.sleep(10)
        continue
      except Exception as e:

        return ["Error", entry, e, index]

async def backup():
  while (True):
    asyncio.sleep(10)
    

async def main():
  invalid = 0
  with open(fpath, 'r', encoding="utf-8-sig") as dataFile:
    data = rispy.load(dataFile)
    tasks = [apiCall(index,entry) for index, entry in enumerate(data)]
    backupTask = asyncio.create_task(backup())

    for completed_task in asyncio.as_completed(tasks):
      response = await completed_task
      if (response[0]=="Backup"):
        if (response[2]=="YES"):
          yes.append(response[1])
          print(str(response[3])+"/"+str(len(data))+": BACKUP, YES: "+response[1]['title'])
        elif (response[2]=="NO"):
          no.append(response[1])
          print(str(response[3])+"/"+str(len(data))+": BACKUP, NO: "+response[1]['title'])
        elif (response[2]=="MAYBE"):
          no.append(response[1])
          print(str(response[3])+"/"+str(len(data))+": BACKUP, MAYBE: "+response[1]['title'])
        else:
          print(str(response[3])+"/"+str(len(data))+": Backup Corrupted:"+response[1]['title']+": Please delete and rerun")
      elif (response[0]=="Error"):
        print(str(response[3])+"/"+str(len(data))+": LLM Error: "+str(response[1]))
        invalid += 1
      elif (response[2].choices[0].message.content == "YES"):
        yes.append(response[1])
        backupDict[response[3]] = "YES"
        print(str(response[3])+"/"+str(len(data))+": YES: "+response[1]['title'])
      elif (response[2].choices[0].message.content == "NO"):
        no.append(response[1])
        backupDict[response[3]] = "NO"
        print(str(response[3])+"/"+str(len(data))+": NO: "+response[1]['title'])
      elif (response[2].choices[0].message.content == "MAYBE"):
        maybe.append(response[1])
        backupDict[response[3]] = "MAYBE"
        print(str(response[3])+"/"+str(len(data))+": MAYBE: "+response[1]['title'])
      else:
        print(str(response[3])+"/"+str(len(data))+": Invalid answer: "+response[1]['title']+": "+response[1].choices[0].message.content)
        invalid += 1
      activeTasks -= 1
                        
    print("Filter Complete!")
    print(str(len(yes))+" "+"yes")
    print(str(len(no))+" "+"no")
    print(str(len(maybe))+" "+"maybe")
    print(str(invalid)+" "+"invalid")
    os.makedirs("output", exist_ok = True)
    with open("output/yes.ris", 'w', encoding="utf-8-sig") as dataFile:
            rispy.dump(yes, dataFile)
    with open("output/no.ris", 'w', encoding="utf-8-sig") as dataFile:
            rispy.dump(no, dataFile)
    with open("output/maybe.ris", 'w', encoding="utf-8-sig") as dataFile:
            rispy.dump(maybe, dataFile)


load_dotenv()

client = AsyncOpenAI(
  api_key=os.getenv('API_KEY')
)

sysPrompt = {"role": "system", "content": """
  Evaluate the appropriateness of each entry for inclusion in a study based on the following criteria: 
    1. In English 
    2. Published 2020 or later
    3. Tests an intervention, program, or policy intended to improve vaccine uptake, knowledge, attitudes and beliefs, or intent to vaccinate
    4. Reports change in vaccine uptake, knowledge, attitudes and beliefs, or intent to vaccinate as an outcome of the tested intervention
  Give your answer as "YES" if all criteria are met
  Give your answer as "MAYBE" if there is not enough information to determine whether all criteria are met
  Give your answer as "NO" if any criteria are clearly violated
"""}

yes = []
no = []
maybe = []
backupDict = {}

SEMAPHORE_LIMIT = 8
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)
backupLock = asyncio.Lock()
activeTasks = 0

fpath = "testing500.ris"

asyncio.run(main())