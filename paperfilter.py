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

ex1 = """
  Title: A mindful path to the COVID-19 pandemic: an approach to promote physical distancing behavior
  Year: 2020
  Abstract: Purpose: The present situation is marked by the threat of COVID-19 pandemic on entire humankind and researchers across the globe are looking forward to vaccines or medicines to tackle COVID-19. However, according to the scholars and health-care agencies, vaccines alone would not be of much help and in the longer run adhering to the physical distancing policy along with sanitation could be the only solution. Moreover, extant studies across different areas have noted a positive association between various human psychological factors and prosocial behaviours. Additionally, an empirical study undertaken in the western context has tried exploring the association between human psychological factors and physical distancing behaviour (a kind of prosocial behaviour) in the COVID-19 context. The results of the extant study seem intriguing and encouraging enough to undertake a more robust exploratory study in this developing area. Against this background, this study aims to explore the relationship between individuals’ mindfulness and physical distancing behaviour, along with the mediating role of empathy during the COVID-19 pandemic. Design/methodology/approach: To achieve the study objectives, this study has used an online survey method and has collected responses from the general adult population in India spread across all six regions. The survey was conducted during May 2020 when India was under a nationwide lockdown to mitigate the risk of COVID-19 pandemic. The respondents were identified based on convenience and snowball sampling techniques. Using social media platforms, the prospective respondents were contacted through WhatsApp, LinkedIn and Facebook or e-mails. Post data cleaning, a total of 315 responses were found to be suitable for analysis. For analysis, confirmatory factor analysis was conducted to establish the validity and reliability of the conceptual model, whereas Pearson correlation was undertaken to study the relationship between variables and mediation was examined using the PROCESS macro of Hayes. Findings: The findings were encouraging and could become the foundation stone for further research and a practical guide for policymakers, agencies working in the health-care areas and even corporate leaders. As expected, an individual’s mindfulness was noted to be positively-related and influencing physical distancing behaviour. The mediation analysis indicated the intervening role of empathy in the association between an individual’s mindfulness and physical distancing behaviour. Practical implications: The findings of the present could be a game-changer in restricting the spread of the COVID-19 pandemic. As espoused by various scholars, as well as health-care organizations about the use of physical distancing in mitigating the risk of COVID-19, policymakers, health-care authorities and even corporate leaders could look forward to strategizing and execute the dissemination of various mindfulness-based programs among the individuals. These mindfulness-based programs, which could be disseminated offline and online through smartphones, could, in turn, help in positively influence physical distancing behaviour among the individuals leading to the success of physical distancing policy. Social implications: This study relates and extends the mechanism of mindfulness in influencing individuals’ physical distancing behaviour in the pandemic situation, notably the COVID-19 pandemic. Moreover, based on the “empathy-altruism hypothesis”, as well as Schwartz’s theory of fundamental values, the intervening role of empathy has been explored and the findings further helped in extended these two theories in the domain of pandemic. Originality/value: This study could be the first to conceptualize and examine the human psychological factors, particularly the relationship and role of an individual’s mindfulness with physical distancing behaviour among the general public during the COVID-19 pandemic. Additionally, this could also be the first study to conceptualize and explore the intervening role of empathy in the relationship between an individual’s mindfulness and physical distancing behaviour. Moreover, in conceptualizing and exploring the relationship between an individual’s mindfulness and physical distancing behaviour, this study explored and extended the “reperceiving” mechanism of mindfulness and the “empathy-altruism hypothesis” along with Schwartz’s theory of fundamental values in the domain of pandemic. © 2020, Emerald Publishing Limited.
"""
msgs.append({"role": "user", "content": ex1})
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=msgs
)
msgs.append({"role": "assistant", "content": completion.choices[0].message.content})
print(completion.choices[0].message.content)

ex2 = """
  Title: [Societal impact of vaccination : beyond individual protection. Renewed interest following COVID-19 pandemic ?].
  Year: 2020
  Abstract: Vaccine hesitancy is growing worldwide and hampering efforts to control vaccine-preventable diseases. Healthcare professionals have a critical role in the acceptance of vaccination by patients. Increased awareness about the benefits of vaccination is one of the recommended strategy to counter vaccine hesitancy. Beyond protection of individuals against specific pathogens, vaccination have broad benefits at multiple levels of society, partly mediated by community protection. These benefits include improved access to education, increased productivity and positive fiscal impact, limitation of gender inequalities, control and prevention of antibiotic resistant pathogens. In this narrative review, those benefits are summarized and relevant studies reviewed. The broad benefits of immunization should contribute to better communication about the impact of immunization and could be part of educational programs of future health-care workers. The COVID-19 pandemic has a tremendous socio-economic impact and is the illustration of a world without vaccine. Nevertheless, recent surveys indicate that the acceptance of a future SARS-CoV-2 vaccine will not be universal, illustrating the importance of communication centered on safety and tolerability of future vaccines.
"""
msgs.append({"role": "user", "content": ex2})
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=msgs
)
msgs.append({"role": "assistant", "content": completion.choices[0].message.content})
print(completion.choices[0].message.content)

ex3 = """
  Title: Healthcare professionals' perspectives on the challenges in the vaccination of Ukrainian child migrants and war refugees: findings from a qualitative study in Poland.
  Year: 2024
  Abstract: <ovid:b>OBJECTIVES</ovid:b>: The aim of this qualitative research study was to explore the barriers encountered by Ukrainian war migrants and refugees in accessing vaccinations in Poland and the challenges related to delivering vaccinations observed by healthcare professionals (HCPs)., <ovid:b>MATERIAL AND METHODS</ovid:b>: The study was based on an analysis of data from 18 in-depth interviews with HCPs working with Ukrainian refugees conducted in Poland in July and August 2023. The authors analyzed the data using the UNICEF Journey to Health and Immunization (JHI) framework in order to identify bottlenecks and possible interventions that could solve existing problems in preventive healthcare for migrants., <ovid:b>RESULTS</ovid:b>: This qualitative study revealed that at each stage of the JHI, there were challenges related to vaccinating Ukrainian children in Poland, which were similar to those experienced in other countries - gaps in routine immunizations and the need to fill these gaps by ensuring refugee populations are fully included in routine immunization in the host country. The work environment, training, and communication with the Ukrainian mothers contribute to HCPs' engagement in increasing vaccine uptake among their patients. The HCPs' attitudes, skills, and experiences impacted their interactions with patients and participation in the immunization process. Healthcare professionals observed that the mother's journey was influenced by vaccine literacy level, competing priorities, individual barriers of access (e.g., language barrier, costs), as well as feelings associated with the decision to vaccinate a child, including worries about vaccine safety. The surrounding cultural norms, social support, and past experiences with the Ukrainian health system also influenced decisions on vaccinations., <ovid:b>CONCLUSIONS</ovid:b>: Overcoming barriers related to vaccinations requires a comprehensive approach, starting with expanding HCPs' knowledge about migrants' rights to health services, including vaccinations, improving communication between patients and HCPs, building vaccine literacy/trust in vaccinations, and achieving vaccination coverage through tailored and flexible systemic solutions. Int J Occup Med Environ Health. 2024;37(6):602-16.<ovid:br/><ovid:br/> Copyright This work is available in Open Access model and licensed under a CC BY-NC 3.0 PL license.
"""
msgs.append({"role": "user", "content": ex3})
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=msgs
)
msgs.append({"role": "assistant", "content": completion.choices[0].message.content})
print(completion.choices[0].message.content)