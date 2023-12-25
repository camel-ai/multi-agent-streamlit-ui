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
import json

import streamlit as st
from camel.agents.deductive_reasoner_agent import DeductiveReasonerAgent
from camel.agents.insight_agent import InsightAgent
from camel.agents.role_assignment_agent import RoleAssignmentAgent
from camel.configs import ChatGPTConfig, FunctionCallingConfig
from camel.functions import MATH_FUNCS, SEARCH_FUNCS
from camel.societies import RolePlaying
from camel.types import ModelType, TaskType
from colorama import Fore


def main(model_type=ModelType.GPT_3_5_TURBO_16K, task_prompt=None,
         context_text=None) -> None:
    # Model and agent initialization
    model_config_description = ChatGPTConfig()
    role_assignment_agent = RoleAssignmentAgent(
        model_type=model_type, model_config=model_config_description)
    insight_agent = InsightAgent(model_type=model_type,
                                 model_config=model_config_description)
    deductive_reasoner_agent = DeductiveReasonerAgent(
        model_type=model_type, model_config=model_config_description)

    # Generate role with descriptions
    role_descriptions_dict = \
        role_assignment_agent.run_role_with_description(
            task_prompt=task_prompt, num_roles=4, role_names=None,
            function_list=[*SEARCH_FUNCS])
    send_role_descriptions_to_ui(role_descriptions_dict=role_descriptions_dict)

    # Split the original task into subtasks
    subtasks_with_dependencies_dict = \
        role_assignment_agent.split_tasks(
            task_prompt=task_prompt,
            role_descriptions_dict=role_descriptions_dict,
            num_subtasks=None,
            context_text=context_text)

    oriented_graph = {}
    for subtask_idx, details in subtasks_with_dependencies_dict.items():
        deps = details["dependencies"]
        oriented_graph[subtask_idx] = deps
    role_assignment_agent.draw_subtasks_graph(
        oriented_graph=oriented_graph,
        graph_file_path="apps/streamlit_ui/task_dependency_graph.png")

    subtasks = [
        subtasks_with_dependencies_dict[key]["description"]
        for key in sorted(subtasks_with_dependencies_dict.keys())
    ]
    send_subtasks_to_ui(subtasks=subtasks)

    # Calculate the execution order of the subtasks, based on their
    # dependencies
    parallel_subtask_pipelines = \
        role_assignment_agent.get_task_execution_order(
            subtasks_with_dependencies_dict)

    # Initialize the environment record
    environment_record = {}  # The cache of the system
    if context_text is not None:
        insights = insight_agent.run(context_text=context_text)
        for insight in insights.values():
            if insight["entity_recognition"] is None:
                continue
            tags = tuple(insight["entity_recognition"])
            environment_record[tags] = insight

    # Resolve the subtasks in sequence of the pipelines
    for subtask_id in (subtask for pipeline in parallel_subtask_pipelines
                       for subtask in pipeline):
        # Get the description of the subtask
        one_subtask = \
            subtasks_with_dependencies_dict[subtask_id]["description"]
        one_subtask_labels = \
            subtasks_with_dependencies_dict[subtask_id]["input_tags"]
        # Get the insights from the environment for the subtask
        insights_for_subtask = get_insights_from_environment(
            subtask_id, one_subtask, one_subtask_labels, environment_record,
            deductive_reasoner_agent, role_assignment_agent, insight_agent,
            context_text)

        # Get the role with the highest compatibility score
        role_compatibility_scores_dict = (
            role_assignment_agent.evaluate_role_compatibility(
                one_subtask, role_descriptions_dict))

        # Get the top two roles with the highest compatibility scores
        ai_assistant_role = \
            max(role_compatibility_scores_dict,
                key=lambda role:
                role_compatibility_scores_dict[role]["score_assistant"])
        ai_user_role = \
            max(role_compatibility_scores_dict,
                key=lambda role:
                role_compatibility_scores_dict[role]["score_user"])

        ai_assistant_description = role_descriptions_dict[ai_assistant_role]
        ai_user_description = role_descriptions_dict[ai_user_role]

        with st.expander(f"{subtask_id}:\n{one_subtask}"):
            send_two_role_descriptions_to_ui(
                ai_assistant_role=ai_assistant_role, ai_user_role=ai_user_role,
                ai_assistant_description=ai_assistant_description,
                ai_user_description=ai_user_description)

            subtask_content = (
                "- Description of TASK:\n" +
                subtasks_with_dependencies_dict[subtask_id]["description"] +
                "\n- Input of TASK:\n" +
                subtasks_with_dependencies_dict[subtask_id]["input_content"] +
                "\n- Output Standard for the completion of TASK:\n" +
                subtasks_with_dependencies_dict[subtask_id]["output_standard"])

            # You can use the following code to play the role-playing game
            sys_msg_meta_dicts = [
                dict(
                    assistant_role=ai_assistant_role, user_role=ai_user_role,
                    assistant_description=ai_assistant_description +
                    insights_for_subtask, user_description=ai_user_description)
                for _ in range(2)
            ]  # System message meta data dicts
            function_list = [*MATH_FUNCS, *SEARCH_FUNCS]
            assistant_model_config = \
                FunctionCallingConfig.from_openai_function_list(
                    function_list=function_list,
                    kwargs=dict(temperature=0.7),
                )  # Assistant model config
            user_model_config = \
                FunctionCallingConfig.from_openai_function_list(
                    function_list=function_list,
                    kwargs=dict(temperature=0.7),
                )  # User model config

            role_play_session = RolePlaying(
                assistant_role_name=ai_assistant_role,
                user_role_name=ai_user_role,
                assistant_agent_kwargs=dict(
                    model_type=ModelType.GPT_4_TURBO,
                    model_config=assistant_model_config,
                    function_list=function_list,
                ),
                user_agent_kwargs=dict(
                    model_type=ModelType.GPT_4_TURBO,
                    model_config=user_model_config,
                    function_list=function_list,
                ),
                task_prompt=subtask_content,
                model_type=model_type,
                task_type=TaskType.
                ROLE_DESCRIPTION,  # Important for role description
                with_task_specify=False,
                extend_sys_msg_meta_dicts=sys_msg_meta_dicts,
            )

            actions_record = ("The TASK of the context text is:\n" +
                              f"{one_subtask}\n")
            chat_history_two_roles = ""

            # Start the role-playing to complete the subtask
            chat_turn_limit, n = 50, 0
            input_assistant_msg, _ = role_play_session.init_chat()
            while n < chat_turn_limit:
                n += 1
                assistant_response, user_response = role_play_session.step(
                    input_assistant_msg)

                send_message_to_ui(role="user", role_name=ai_user_role,
                                   message=user_response.msg.content)
                send_message_to_ui(role="assistant",
                                   role_name=ai_assistant_role,
                                   message=assistant_response.msg.content)

                # Generate the insights from the chat history
                actions_record += (f"--- [{n}] ---\n"
                                   f"{assistant_response.msg.content}\n")
                user_conversation = user_response.msg.content
                assistant_conversation = \
                    assistant_response.msg.content.replace(
                        "Solution&Action:\n", "").replace(
                            "Next request.", "").strip("\n")
                transformed_text_with_category = \
                    role_assignment_agent.transform_dialogue_into_text(
                        user=ai_user_role, assistant=ai_assistant_role,
                        task_prompt=one_subtask,
                        user_conversation=user_conversation,
                        assistant_conversation=assistant_conversation)
                if ("ASSISTANCE"
                        in transformed_text_with_category["categories"]
                        or "ANALYSIS"
                        in transformed_text_with_category["categories"]):
                    transformed_text = transformed_text_with_category["text"]
                    chat_history_two_roles += (transformed_text + "\n\n")

                if assistant_response.terminated:
                    print(Fore.GREEN + (
                        f"{ai_assistant_role} terminated. Reason: "
                        f"{assistant_response.info['termination_reasons']}."))
                    break
                if user_response.terminated:
                    print(Fore.GREEN + (
                        f"{ai_user_role} terminated. "
                        f"Reason: {user_response.info['termination_reasons']}."
                    ))
                    break

                if "CAMEL_TASK_DONE" in user_response.msg.content or \
                        "CAMEL_TASK_DONE" in assistant_response.msg.content:
                    break

                input_assistant_msg = assistant_response.msg

            send_message_to_ui(
                role="assistant", role_name=ai_assistant_role,
                message=f"Output of the {subtask_id}:\n" +
                chat_history_two_roles)

            insights_instruction = (
                "The CONTEXT TEXT is the steps to resolve " +
                "the TASK. The INSIGHTs should come solely" +
                "from the actions/steps.")
            insights = insight_agent.run(
                context_text=actions_record,
                insights_instruction=insights_instruction)
            for insight in insights.values():
                if insight["entity_recognition"] is None:
                    continue
                labels_key = tuple(insight["entity_recognition"])
                environment_record[labels_key] = insight


def get_insights_from_environment(subtask_id, one_subtask, one_subtask_labels,
                                  environment_record, deductive_reasoner_agent,
                                  role_assignment_agent, insight_agent,
                                  context_text):
    # React to the environment, and get the insights from it
    conditions_and_quality_json = \
        deductive_reasoner_agent.deduce_conditions_and_quality(
            starting_state="None",
            target_state=one_subtask)

    target_labels = list(
        set(conditions_and_quality_json["labels"]) | set(one_subtask_labels))
    # print(f"Target labels for {subtask_id}:\n{target_labels}")

    labels_sets = [
        list(labels_set) for labels_set in environment_record.keys()
    ]
    # print(f"Labels sets for {subtask_id}:\n{labels_sets}")

    _, _, _, labels_retrieved_sets = \
        role_assignment_agent.get_retrieval_index_from_environment(
            labels_sets=labels_sets,
            target_labels=target_labels)
    # print_and_write_md(
    #     "Retrieved labels from the environment:\n" +
    #     f"{labels_retrieved_sets}", color=Fore.CYAN,
    #     file_path=f"retrieved labels for {subtask_id}")

    # Retrive the necessaray insights from the environment
    retrieved_insights = [
        environment_record[tuple(label_set)]
        for label_set in labels_retrieved_sets
    ]
    # print("Retrieved insights from the environment for "
    #       f"{subtask_id}:\n"
    #       f"{json.dumps(retrieved_insights, indent=4)}")

    insights_none_pre_subtask = insight_agent.run(context_text=context_text)
    insights_for_subtask = (
        "\n====== CURRENT STATE =====\n"
        "The snapshot and the context of the TASK is presentd in "
        "the following insights which is close related to The "
        "\"Insctruction\" and the \"Input\":\n" +
        f"{json.dumps(insights_none_pre_subtask, indent=4)}\n")

    insights_for_subtask += "\n".join(
        [json.dumps(insight, indent=4) for insight in retrieved_insights])

    # print_and_write_md(
    #     f"Insights from the context text:\n{insights_for_subtask}",
    #     color=Fore.GREEN, file_path="insights of context text for "
    #     f"{subtask_id}")

    subtask_id = subtask_id.replace("_", " ")

    return insights_for_subtask


def send_role_descriptions_to_ui(role_descriptions_dict={}):
    num_roles = len(role_descriptions_dict)
    with st.expander(f"Build {num_roles} AI agents:"):
        for role, role_description in role_descriptions_dict.items():
            st.write(f"{role}:")
            st.write(role_description)


def send_two_role_descriptions_to_ui(ai_assistant_role="", ai_user_role="",
                                     ai_assistant_description="",
                                     ai_user_description=""):
    st.write(f"{ai_assistant_role}:")
    st.write(ai_assistant_description)
    st.write(f"{ai_user_role}:")
    st.write(ai_user_description)


def send_subtasks_to_ui(subtasks=[]):
    with st.expander("Subtasks:"):
        for i, subtask in enumerate(subtasks):
            st.write(f"Subtask {i + 1}:")
            st.write(subtask)


def send_message_to_ui(role="", role_name="", message=""):
    if role not in ["user", "assistant"]:
        raise ValueError("The role should be one of 'user' or 'assistant'.")

    with st.chat_message(role):
        st.write(f"AI {role}: {role_name}\n\n{message}\n")
