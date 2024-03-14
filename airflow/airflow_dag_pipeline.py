from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import random
from langdetect import detect
import re

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'retries': 1,
}

# Define the DAG object
dag = DAG(
        'language_detection_pipeline',
        default_args=default_args,
        description='A simple pipeline to detect the language of text',
        schedule_interval=None,
)

# Function to generate random text
def generate_text():
    languages = ['en', 'fr', 'de', 'es']  # Example languages
    return 'Random text in ' + random.choice(languages)

# Function to clean text (remove special characters)
def clean_text(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)

# Function to preprocess text (convert to lowercase)
def preprocess_text(text):
    return text.lower()

# Function to detect language
def detect_language(text):
    language = detect(text)
    return language

# Function for postprocessing (convert language to full name)
def postprocess_language(language):
    language_mapping = {
        'en': 'English',
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish'
    }
    return language_mapping.get(language, 'Unknown')

# Define tasks in the DAG
generate_text_task = PythonOperator(
        task_id='generate_text',
        python_callable=generate_text,
        dag=dag,
)

clean_text_task = PythonOperator(
        task_id='clean_text',
        python_callable=clean_text,
        op_args=[ "{{ task_instance.xcom_pull(task_ids='generate_text') }}" ],
        dag=dag,
)

preprocess_text_task = PythonOperator(
        task_id='preprocess_text',
        python_callable=preprocess_text,
        op_args=[ "{{ task_instance.xcom_pull(task_ids='clean_text') }}" ],
        dag=dag,
)

detect_language_task = PythonOperator(
        task_id='detect_language',
        python_callable=detect_language,
        op_args=[ "{{ task_instance.xcom_pull(task_ids='preprocess_text') }}" ],
        dag=dag,
)

postprocess_language_task = PythonOperator(
        task_id='postprocess_language',
        python_callable=postprocess_language,
        op_args=[ "{{ task_instance.xcom_pull(task_ids='detect_language') }}" ],
        dag=dag,
)

# Define task dependencies
generate_text_task >> clean_text_task >> preprocess_text_task >> detect_language_task >> postprocess_language_task