import os
from dotenv import load_dotenv
from openai import OpenAI
import rispy


load_dotenv()

client = OpenAI(
  api_key=os.getenv('API_KEY')
)

msgs = []

prompt = """
  You will be provided with a series of references, including their title, the year published, and abstract. The format will look like this:

  Title: Vaccine safety, vaccine effectiveness and other determinants for successful immunization programmes.
  Year: 2022
  Abstract: The studies in this thesis examined several key determinants for successful uptake of vaccinations in the Nordic countries, with focus on vaccine safety and vaccine effectiveness.In study I, we investigated whether disease history is a risk factor for narcolepsy after vaccination with the pandemic influenza vaccine, Pandemrix, which was circulated between 2009 and 2010. The results showed that there was no association between disease history and narcolepsy. We also found evidence for confounding by indication, with a larger number of prescriptions/diagnoses for nervous system disorders and mental and behavioural disorders when we did not adjust for the timing of vaccination or vaccination status. This could suggest that early cases of narcolepsy were initially misdiagnosed prior to narcolepsy diagnosis.In study II, we investigated the effect of the quadrivalent human papillomavirus (qHPV) vaccine on genital condyloma by the number of doses and time between doses. This cohort study followed young Swedish girls ages 10-27 for HPV vaccination and condyloma. The results showed that the greatest protection against condyloma was seen after two doses of qHPV vaccine with 4-7 months between dose one and two. We also found that girls, who initiated vaccination at a younger age, had a greater protection against condyloma.The results from these studies show just how complex the improvement of vaccination programmes can be. On one hand, we see the difficulties in assessing what went wrong following the introduction of a vaccine into a population- it is not always possible to predict a rare outcome from a mass vaccination campaign, so vaccine safety becomes a paramount concern from a societal perspective. We also see what happens when a vaccine proves its effectiveness in a population-based setting to the point where the number of doses can be reduced without compromising its effectiveness. Improving the vaccination programmes is, therefore, a complex multifactorial problem with many key determinants that can change depending on the vaccine in question e.g. mass vaccination versus routine vaccination. (PsycInfo Database Record (c) 2022 APA, all rights reserved)

  Evaluate the appropriateness of each entry for inclusion in a study based on the following criteria: 
  1. Should be in English; 
  2. Should be published 2020 or later; 
  3. Should test an intervention; 
  4. Should evaluate vaccine uptake, knowledge, attitudes and beliefs, or intent to vaccinate. 
  Give your answer as "YES", "MAYBE", or "NO".
"""
msgs.append({"role": "system", "content": prompt})

yes = []
no = []
maybe = []
invalid = 0
contextLimit = 10
context = []

fpath = "testing500.ris"
with open(fpath, 'r', encoding="utf-8-sig") as dataFile:
  data = rispy.load(dataFile)
  i = 1
  for entry in data:
    paperPrompt = f"""
      Title: {entry['title']}
      Year: {entry['year']}
      Abstract: {entry['notes_abstract']}
    """
    if (len(context) >= contextLimit*2):
      context.pop(0)
      context.pop(0)
    context.append({"role": "user", "content": paperPrompt})
    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "system", "content": prompt}]+context
    )
    context.append({"role": "assistant", "content": completion.choices[0].message.content})
    if (completion.choices[0].message.content == "YES"):
      yes.append(entry)
    elif (completion.choices[0].message.content == "NO"):
      no.append(entry)
    elif (completion.choices[0].message.content == "MAYBE"):
      maybe.append(entry)
    else:
      print("Invalid answer from LLM.")
      invalid += 1
    print(str(i)+"/"+str(len(data))+": "+entry['title'])
    i += 1


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