import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, RateLimitError
import rispy


async def apiCall(entry):
  paperPrompt = f"""
    Title: {entry['title']}
    Year: {entry['year']}
    Abstract: {entry['notes_abstract']}
  """
  async with semaphore:
    while True:
      try:
        response = await client.chat.completions.create(
          model="gpt-4o",
          messages=[sysPrompt, {"role": "user", "content": paperPrompt}]
        )
        return [entry, response]
      except RateLimitError as e:
        print("Rate limited! Waiting 10s...")
        await asyncio.sleep(10)
        continue
      except Exception as e:

        return ["Error", e]

async def main():
  invalid = 0
  with open(fpath, 'r', encoding="utf-8-sig") as dataFile:
    data = rispy.load(dataFile)
    tasks = [apiCall(entry) for entry in data]

    i = 0
    for completed_task in asyncio.as_completed(tasks):
      response = await completed_task
      i += 1
      if (response[0]=="Error"):
        print(str(i)+"/"+str(len(data))+": LLM Error: "+str(response[1]))
        invalid += 1
      elif (response[1].choices[0].message.content == "YES"):
        yes.append(response[0])
        print(str(i)+"/"+str(len(data))+": YES: "+response[0]['title'])
      elif (response[1].choices[0].message.content == "NO"):
        no.append(response[0])
        print(str(i)+"/"+str(len(data))+": NO: "+response[0]['title'])
      elif (response[1].choices[0].message.content == "MAYBE"):
        maybe.append(response[0])
        print(str(i)+"/"+str(len(data))+": MAYBE: "+response[0]['title'])
      else:
        print(str(i)+"/"+str(len(data))+": Invalid answer: "+response[1].choices[0].message.content)
        invalid += 1
        continue
        
         
        
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
contextLimit = 10
context = []

SEMAPHORE_LIMIT = 8
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

fpath = "testing500.ris"

asyncio.run(main())