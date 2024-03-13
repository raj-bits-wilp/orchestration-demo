import packages.data_processor as dp
# import streamlit as st
import joblib
import json
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()

# Load the model
spam_clf = joblib.load(open('./models/spam_detector_model.pkl', 'rb'))

# Load vectorizer
vectorizer = joblib.load(open('./vectors/vectorizer.pickle', 'rb'))


class Data(BaseModel):
    text: str


@app.post('/spam_classification')
def diabetes_predd(input_parameters: Data):
    input_data = input_parameters.dict()
    prediction = spam_clf.predict(vectorizer.transform([input_data["text"]]))

    if (prediction[0] == 0):
        info = 'Ham'

    else:
        info = 'Spam'

    return {"out": info}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

#
# ### MAIN FUNCTION ###
# def main(title = "MLOps Demo Streamlit Text classification App".upper()):
#     st.markdown("<h1 style='text-align: center; font-size: 65px; color: #4682B4;'>{}</h1>".format(title),
#     unsafe_allow_html=True)
#     st.image("./images/message-image.jpeg")
#     info = ''
#
#     with st.expander("1. Ckeck if your text is a spam or ham 😀"):
#         text_message = st.text_input("Please enter your message")
#         if st.button("Predict"):
#             prediction = spam_clf.predict(vectorizer.transform([text_message]))
#
#             if(prediction[0] == 0):
#                 info = 'Ham'
#
#             else:
#                 info = 'Spam'
#             st.success('Prediction: {}'.format(info))
#
# if __name__ == "__main__":
#     main()
