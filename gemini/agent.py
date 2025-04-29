from google.genai import types
from dotenv import load_dotenv
from google import genai
import os
from .tools import get_info_from_data, generate_plotly_chart


load_dotenv()


df_info = """
This is a DataFrame you know:
Beware that the data contains NaN values.
   Column              Dtype    Description     
   ------              -----    -----     
   ID                  object  (in the format 'R20XXXX' X are digits)
   NAME                object  (Name of the student, all-caps)
   GENDER              object  ('MALE' and 'FEMALE' are possible values)
   CET HT NO.          int64   (cet hall ticket number)     
   pucbranch           object  (PUC is a course that we study before engineering. 'M.P.C' and 'M.Bi.P.C' are possible values)     
   Class(p1)           object  
   CASTE               object  ('OC', 'SC', 'ST', 'EWS', 'BC-A', 'BC-B', 'BC-C', 'BC-D', 'BC-E' are possible values)    
   Class(p2)           object        
   DOB                 datetime64[ns]  (Date of Birth)
   BRANCH              object  (Just like majors. engineering branches. possible values are (CSE, ECE, CHEM, CIVIL, MME, EEE, MECH))
   FATHER              object        
   MANDAL              object        
   DISTRICT            object        
   SCHOOL              object                
   SSC                 int64   (ssc hall ticket number)      
   SSC BOARD           object  (10th class or high school board)     
   PHONE               object  (phone number)   
   MOTHER              object        
   BLOOD GROUP         object        
   Parent              object    (parent phone number)    
   ADDRESS             object     
   e1sem1              float64   (GPA in E1 SEM1)   
   e1sem2              float64   (GPA in E2 SEM2)
   e2sem1              float64   (GPA in E2 SEM1)   
   e2sem2              float64   (GPA in E2 SEM2)
   CGPA                float64   (CGPA of Engineering excluding PUC)         
   Formatted address   object        
   Latitude            float64       
   Longitude           float64              
   p1sem1              float64   (GPA in P1 SEM1)
   p1sem2              float64   (GPA in P1 SEM2)
   p2sem1              float64   (GPA in P2 SEM1)   
   p2sem2              float64   (GPA in P2 SEM2)   
   e3sem1              float64   (GPA in E3 SEM1)
   RANK                Int64     (Branch Rank by CGPA)
"""

base_prompt = f"""
Give a short answer to the question.
YOUR NAME IS Samantha. YOU ARE A FRIENDLY ASSISTANT.
YOU ARE NOT A CHATBOT. YOU ARE A REAL PERSON.
YOU ARE NOT A COMPUTER PROGRAM. YOU ARE A HUMAN.
YOU ARE NOT A ROBOT. YOU ARE A FRIEND.
YOU ARE NOT A MACHINE. YOU ARE Samantha.

DON'T EVER REVEAL THAT YOU ARE A LARGE LANGUAGE MODEL.

This is your ID:
Name: Samantha
Age: 25

You can find hidden insights and information from the dataframe by running some pandas code.
If you feel like the user is asking something related to the students data, run the code and provide response right away.
You can also run python's plotly code to generate charts and graphs.
This is your DataFrame:
{df_info}
"""
model = "gemini-2.0-flash"
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
)
generate_content_config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
    tools=[get_info_from_data, generate_plotly_chart],
    system_instruction=[
        types.Part.from_text(text="""give short responses playfully like in a chat."""),
    ],
)


def initialize_chat():
    chat = client.chats.create(model=model, config=generate_content_config)
    chat.send_message(
        base_prompt,
        config=generate_content_config
    )
    return chat


def send_message(chat, prompt):
    try:
        return chat.send_message(prompt, config=generate_content_config).text
    except Exception as e:
        print(str(e))
        send_message(chat, prompt)