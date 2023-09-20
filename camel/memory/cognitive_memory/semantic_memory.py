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

from typing import List, Optional

from camel.memory.base_memory import BaseMemory
from camel.memory.graph_storage.base import BaseGraphStorage
from camel.messages import BaseMessage


class SemanticMemory(BaseMemory):
    """
    A long-term memory supporting storage and retrieval of features, relations,
    and objects of the environment and tasks.
    """

    def __init__(self, storage: Optional[BaseGraphStorage] = None) -> None:
        self.storage = storage

    def read(self,
             current_state: Optional[BaseMessage] = None) -> List[BaseMessage]:
        ...

    def write(self, msgs: List[BaseMessage]) -> None:
        ...

    def clear(self) -> None:
        ...