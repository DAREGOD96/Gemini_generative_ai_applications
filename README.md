# Gemini_generative_ai_applications

## Getting Started

Instructions on how to clone and run the project on another machine.

### Installation

### STEPS:

Clone the repository

```bash
https://github.com/DAREGOD96/Gemini_generative_ai_applications.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n genai python=3.10 -y
```

```bash
conda activate genai
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


```bash
# Finally run the following command
streamlit run text.py
streamlit run vision.py
streamlit run gemini_chat.py
streamlit run health_app.py
streamlit run image_text_extractor.py

# For executing the text_to_sql_query.py file we need to first execute the sql.py file
python sql.py
streamlit run text_to_sql_query.py
```
