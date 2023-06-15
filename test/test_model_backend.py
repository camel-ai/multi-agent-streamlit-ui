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
import pytest

from camel.configs import ChatGPTConfig
from camel.model_backend import ModelFactory
from camel.typing import ModelType

parametrize = pytest.mark.parametrize('model', [
    ModelType.STUB,
    pytest.param(None, marks=pytest.mark.model_backend),
    pytest.param(ModelType.GPT_3_5_TURBO, marks=pytest.mark.model_backend),
    pytest.param(ModelType.GPT_4, marks=pytest.mark.model_backend),
])


@parametrize
def test_openai_model(model):
    model_config_dict = ChatGPTConfig().__dict__
    model_inst = ModelFactory.create(model, model_config_dict)
    messages = [
        {
            'role': 'system',
            'content': 'You can make a task more specific.'
        },
        {
            'role':
            'user',
            'content': ('Here is a task that Python Programmer will help '
                        'Stock Trader to complete: Develop a trading bot '
                        'for the stock market.\nPlease make it more specific.'
                        ' Be creative and imaginative.\nPlease reply with '
                        'the specified task in 50 words or less. '
                        'Do not add anything else.')
        },
    ]
    response = model_inst.run(messages=messages)
    assert isinstance(response, dict)
    assert 'id' in response
    assert isinstance(response['id'], str)
    assert 'usage' in response
    assert isinstance(response['usage'], dict)
    assert 'choices' in response
    assert isinstance(response['choices'], list)
    assert len(response['choices']) == 1
    choice = response['choices'][0]
    assert 'finish_reason' in choice
    assert isinstance(choice['finish_reason'], str)
    assert 'message' in choice
    message = choice['message']
    assert isinstance(message, dict)
    assert 'content' in message
    assert isinstance(message['content'], str)
    assert 'role' in message
    assert isinstance(message['role'], str)
    assert message['role'] == 'assistant'