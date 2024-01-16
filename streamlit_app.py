# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========

# Import necessary libraries and modules
import os

import streamlit as st
from camel.configs import ChatGPTConfig
from camel.functions.data_io_functions import read_file
from camel.models.openai_model import OpenAIModel
from camel.types import ModelType

# Import functions and data related to the Streamlit user interface
from apps.streamlit_ui.multi_agent_communication_ui import main

# Set the title for the Streamlit app
st.title("🐫 CAMEL Multi-Agent")

# Create a sidebar with form elements
with st.sidebar:
    with st.form(key='form1'):
        # Input field for API Keys
        openai_api_key = st.text_input("OpenAI API Key", key="api_key_openai",
                                       type="password")
        duckduckgo_api_key = st.text_input("Duckduckgo API Key",
                                           key="api_key_duckduckgo",
                                           type="password")
        search_engine_id = st.text_input("Search Engine ID",
                                         key="search_engine_id",
                                         type="password")

        # Set the environment variables for the API Key
        os.environ["OPENAI_API_KEY"] = openai_api_key
        os.environ["DUCKDUCKGO_API_KEY"] = duckduckgo_api_key
        os.environ["SEARCH_ENGINE_ID"] = search_engine_id

        # File uploader for users to upload a document
        uploaded_file = st.file_uploader(
            "Upload a file", type=("txt", "docx", "pdf", "json", "html"))

        # If a file is uploaded, extract content from it
        if uploaded_file:
            article = read_file(uploaded_file)
            normal_string = article.docs[0]['page_content']

            # Create an instance of the OpenAI model
            my_openai_model = OpenAIModel(
                model_type=ModelType.GPT_3_5_TURBO,
                model_config_dict=ChatGPTConfig().__dict__)

            # Create a task prompt based on the uploaded content
            messages_task_prompt = [
                {
                    "role":
                    "system",
                    "content":
                    '''You are a helpful assistant to extract and
                     re-organize information from provided information.
                     below is the content for you:''' + '\n' + normal_string,
                },
                {
                    "role":
                    "user",
                    "content":
                    '''Please create a prompt for the task to be
                     performed described in the given information.''',
                },
            ]

            # Get a response for the task prompt
            response_task_prompt = my_openai_model.run(
                messages=messages_task_prompt)['choices'][0]
            content_task_prompt = response_task_prompt['message']['content']

            # Create a context content based on the uploaded content
            messages_context_content = [
                {
                    "role":
                    "system",
                    "content":
                    '''You are a helpful assistant to extract and
                     re-organize information from provided information.
                     below is the content for you:''' + '\n' + normal_string,
                },
                {
                    "role":
                    "user",
                    "content":
                    '''Please extract the context content for the task to
                     be performed described in the given information.''',
                },
            ]

            # Get a response for the context content
            response_context_content = my_openai_model.run(
                messages=messages_context_content)['choices'][0]
            content_context_content = response_context_content['message'][
                'content']

            # Set task prompt and context content as inputs in the form
            task_prompt = st.text_area(
                "Your task prompt extracted from the file",
                value=content_task_prompt)
            context_content = st.text_area(
                "Your context content extracted from the file",
                value=content_context_content)
        else:
            # Set default values for task prompt and context content
            with open('apps/streamlit_ui/task_prompt_GPT_prediction.txt',
                      'r') as file:
                task_prompt_business_novel = file.read()
            with open('apps/streamlit_ui/context_content_GPT_prediction.txt',
                      'r') as file:
                context_content_business_novel = file.read()
            task_prompt = st.text_area("Insert the task here",
                                       value=task_prompt_business_novel)
            context_text = st.text_area("Insert the context here",
                                        value=context_content_business_novel)

        # Create a submit button in the form
        submit_button = st.form_submit_button(label='Submit')

# Check if all required inputs are provided and the submit button is clicked
if (openai_api_key and duckduckgo_api_key and search_engine_id and task_prompt
        and context_text and submit_button):
    # Call the 'main' function with the task prompt and context content
    main(task_prompt=task_prompt, context_text=context_text)
