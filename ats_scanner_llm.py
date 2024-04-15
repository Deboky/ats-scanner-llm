from common.utils import *

# Read the yaml file
with open("config.yaml", "rt") as file:
    config = yaml.safe_load(file.read())



api_key = config["GOOGLE_API_KEY"]

# print(api_key)


genai.configure(api_key=api_key)


# PDF Text Extraction

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Content Generation with Gemini Model

def get_gemini_repsonse(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text



# Prompt Template

input_prompt = """
Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Job description and the missing keywords with high accuracy resume:{text} description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

## Streamlit Web App

st.title("Smart ATS Resume Analyzer")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader(
    "Upload Your Resume", type="pdf", help="Please uplaod the pdf"
)

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_repsonse(input_prompt)
        st.subheader(response)