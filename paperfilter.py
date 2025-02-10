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
          model="gpt-4o-mini",
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
  You will be provided with a series of references, including their title, the year published, and abstract. The format will look like this:

  Title: Vaccine safety, vaccine effectiveness and other determinants for successful immunization programmes.
  Year: 2022
  Abstract: The studies in this thesis examined several key determinants for successful uptake of vaccinations in the Nordic countries, with focus on vaccine safety and vaccine effectiveness.In study I, we investigated whether disease history is a risk factor for narcolepsy after vaccination with the pandemic influenza vaccine, Pandemrix, which was circulated between 2009 and 2010. The results showed that there was no association between disease history and narcolepsy. We also found evidence for confounding by indication, with a larger number of prescriptions/diagnoses for nervous system disorders and mental and behavioural disorders when we did not adjust for the timing of vaccination or vaccination status. This could suggest that early cases of narcolepsy were initially misdiagnosed prior to narcolepsy diagnosis.In study II, we investigated the effect of the quadrivalent human papillomavirus (qHPV) vaccine on genital condyloma by the number of doses and time between doses. This cohort study followed young Swedish girls ages 10-27 for HPV vaccination and condyloma. The results showed that the greatest protection against condyloma was seen after two doses of qHPV vaccine with 4-7 months between dose one and two. We also found that girls, who initiated vaccination at a younger age, had a greater protection against condyloma.The results from these studies show just how complex the improvement of vaccination programmes can be. On one hand, we see the difficulties in assessing what went wrong following the introduction of a vaccine into a population- it is not always possible to predict a rare outcome from a mass vaccination campaign, so vaccine safety becomes a paramount concern from a societal perspective. We also see what happens when a vaccine proves its effectiveness in a population-based setting to the point where the number of doses can be reduced without compromising its effectiveness. Improving the vaccination programmes is, therefore, a complex multifactorial problem with many key determinants that can change depending on the vaccine in question e.g. mass vaccination versus routine vaccination. (PsycInfo Database Record (c) 2022 APA, all rights reserved)

  Evaluate the appropriateness of each entry for inclusion in a study based on the following criteria: 
  1. Should be in English; 
  2. Should be published 2020 or later; 
  3. Should test an intervention; 
  4. Should evaluate vaccine uptake, knowledge, attitudes and beliefs, or intent to vaccinate. 
  Give your answer as "YES", "MAYBE", or "NO"; Your answer should consist of nothing but one of these words.
"""}

yes = []
no = []
maybe = []
contextLimit = 10
context = []

SEMAPHORE_LIMIT = 15
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

fpath = "testing500.ris"

asyncio.run(main())