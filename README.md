<div style="left">
  <a href="https://colab.research.google.com/drive/1AzP33O8rnMW__7ocWJhVBXjKziJXPtim?usp=sharing" target="_blank">
    <img alt="Open In Colab" src="https://colab.research.google.com/assets/colab-badge.svg" />
  </a>
  <a href="https://huggingface.co/camel-ai" target="_blank">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-CAMEL--AI-ffc107?color=ffc107&logoColor=white" />
  </a>
  <a href="https://join.slack.com/t/camel-kwr1314/shared_invite/zt-1vy8u9lbo-ZQmhIAyWSEfSwLCl2r2eKA" target="_blank">
      <img alt="Slack" src="https://img.shields.io/badge/Slack-CAMEL--AI-blueviolet?logo=slack" />
  </a>
  <a href="https://discord.gg/CNcNpquyDc" target="_blank">
    <img alt="Discord" src="https://img.shields.io/badge/Discord-CAMEL--AI-7289da?logo=discord&logoColor=white&color=7289da" />
  </a>
  <a href="https://ghli.org/camel/wechat.png" target="_blank">
    <img alt="Discord" src="https://img.shields.io/badge/WeChat-CamelAIOrg-brightgreen?logo=wechat&logoColor=white" />
  </a>
  <a href="https://twitter.com/CamelAIOrg" target="_blank">
    <img alt="Twitter Follow" src="https://img.shields.io/twitter/follow/CamelAIOrg?style=social&color=brightgreen&logo=twitter" />
  </a>
</div>

# CAMEL Multi-Agent System Streamlit UI

<div align="center">

  <a>![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)</a>
  <a href="https://github.com/camel-ai/camel/actions/workflows/pytest_package.yml">![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/camel-ai/camel/pytest_package.yml?label=tests&logo=github)</a>
  <a href="https://camel-ai.github.io/camel/">
    ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/camel-ai/camel/documentation.yaml?label=docs&logo=github)
  </a>
  <a href="https://github.com/camel-ai/camel/stargazers" target="_blank">
  <img alt="GitHub Repo Stars" src="https://img.shields.io/github/stars/camel-ai/camel?label=stars&logo=github&color=brightgreen" />
  </a>
  <a href="https://github.com/camel-ai/camel/blob/master/licenses/LICENSE">![License](https://img.shields.io/github/license/camel-ai/camel?label=license&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0IiBmaWxsPSIjZmZmZmZmIj48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xMi43NSAyLjc1YS43NS43NSAwIDAwLTEuNSAwVjQuNUg5LjI3NmExLjc1IDEuNzUgMCAwMC0uOTg1LjMwM0w2LjU5NiA1Ljk1N0EuMjUuMjUgMCAwMTYuNDU1IDZIMi4zNTNhLjc1Ljc1IDAgMTAwIDEuNUgzLjkzTC41NjMgMTUuMThhLjc2Mi43NjIgMCAwMC4yMS44OGMuMDguMDY0LjE2MS4xMjUuMzA5LjIyMS4xODYuMTIxLjQ1Mi4yNzguNzkyLjQzMy42OC4zMTEgMS42NjIuNjIgMi44NzYuNjJhNi45MTkgNi45MTkgMCAwMDIuODc2LS42MmMuMzQtLjE1NS42MDYtLjMxMi43OTItLjQzMy4xNS0uMDk3LjIzLS4xNTguMzEtLjIyM2EuNzUuNzUgMCAwMC4yMDktLjg3OEw1LjU2OSA3LjVoLjg4NmMuMzUxIDAgLjY5NC0uMTA2Ljk4NC0uMzAzbDEuNjk2LTEuMTU0QS4yNS4yNSAwIDAxOS4yNzUgNmgxLjk3NXYxNC41SDYuNzYzYS43NS43NSAwIDAwMCAxLjVoMTAuNDc0YS43NS43NSAwIDAwMC0xLjVIMTIuNzVWNmgxLjk3NGMuMDUgMCAuMS4wMTUuMTQuMDQzbDEuNjk3IDEuMTU0Yy4yOS4xOTcuNjMzLjMwMy45ODQuMzAzaC44ODZsLTMuMzY4IDcuNjhhLjc1Ljc1IDAgMDAuMjMuODk2Yy4wMTIuMDA5IDAgMCAuMDAyIDBhMy4xNTQgMy4xNTQgMCAwMC4zMS4yMDZjLjE4NS4xMTIuNDUuMjU2Ljc5LjRhNy4zNDMgNy4zNDMgMCAwMDIuODU1LjU2OCA3LjM0MyA3LjM0MyAwIDAwMi44NTYtLjU2OWMuMzM4LS4xNDMuNjA0LS4yODcuNzktLjM5OWEzLjUgMy41IDAgMDAuMzEtLjIwNi43NS43NSAwIDAwLjIzLS44OTZMMjAuMDcgNy41aDEuNTc4YS43NS43NSAwIDAwMC0xLjVoLTQuMTAyYS4yNS4yNSAwIDAxLS4xNC0uMDQzbC0xLjY5Ny0xLjE1NGExLjc1IDEuNzUgMCAwMC0uOTg0LS4zMDNIMTIuNzVWMi43NXpNMi4xOTMgMTUuMTk4YTUuNDE4IDUuNDE4IDAgMDAyLjU1Ny42MzUgNS40MTggNS40MTggMCAwMDIuNTU3LS42MzVMNC43NSA5LjM2OGwtMi41NTcgNS44M3ptMTQuNTEtLjAyNGMuMDgyLjA0LjE3NC4wODMuMjc1LjEyNi41My4yMjMgMS4zMDUuNDUgMi4yNzIuNDVhNS44NDYgNS44NDYgMCAwMDIuNTQ3LS41NzZMMTkuMjUgOS4zNjdsLTIuNTQ3IDUuODA3eiI+PC9wYXRoPjwvc3ZnPgo=)</a>
</div>

<p align="center">
   <a href="https://github.com/camel-ai/camel#community">Community</a> |
  <a href="https://github.com/camel-ai/camel#installation">Installation</a> |
  <a href="https://camel-ai.github.io/camel/">Documentation</a> |
  <a href="https://github.com/camel-ai/camel/tree/HEAD/examples">Examples</a> |
  <a href="https://arxiv.org/abs/2303.17760">Paper</a> |
  <a href="https://github.com/camel-ai/camel#citation">Citation</a> |
  <a href="https://github.com/camel-ai/camel#contributing-to-camel-">Contributing</a> |
  <a href="https://www.camel-ai.org/">CAMEL-AI</a>
</p>

<p align="center">
  <img src='https://raw.githubusercontent.com/camel-ai/camel/master/misc/logo.png' width=800>
</p>

## Overview
This project, part of CAEML, implements a multi-agent system with a user interface developed in Streamlit. It showcases the integration of advanced agent-based modeling techniques with an accessible and interactive web interface.

<p align="center">
    <img src='misc\stramlit_ui.png' with=800>
</p>

### ⚠️ Development and Testing Warning

**Warning**: The multi-agent system is still under active development and testing, which means the UI may have several issues. If you encounter problems, please try refreshing the page and rerunning it. Additionally, we encourage you to report any issues you encounter by submitting an 'Issue' on the GitHub repository. Your feedback is valuable in improving the system's stability and functionality.

## Community
🐫 CAMEL is an open-source library designed for the study of autonomous and communicative agents. We believe that studying these agents on a large scale offers valuable insights into their behaviors, capabilities, and potential risks. To facilitate research in this field, we implement and support various types of agents, tasks, prompts, models, and simulated environments.

Join us ([*Slack*](https://join.slack.com/t/camel-kwr1314/shared_invite/zt-1vy8u9lbo-ZQmhIAyWSEfSwLCl2r2eKA), [*Discord*](https://discord.gg/CNcNpquyDc) or [*WeChat*](https://ghli.org/camel/wechat.png)) in pushing the boundaries of building AI Society.

## Introduction to Multi-Agent System of CAMEL

<p align="center">
    <img src='misc\framework_of_the_multi_agent_system.png' with=800>
</p>

In an era where digital interfaces are integral to our daily lives, the need for seamless and meaningful human-computer interactions has never been greater. This is where the groundbreaking the Multi-Agent System comes into play, introducing a game-changer in the realm of digital communication. 

The Multi-Agent System has risen as a critical solution to complex and dynamic problems in computational intelligence. CAMEL.AI, an acronym for *Communicative Agents for “Mind” Exploration of Large-Scale Language Model Society*, is an outstanding open-source community that aims to refine how AI agents interact within an AI system. The Multi-Agent System, proposed by CAMEL.AI, endeavors to meet the nuanced requirements and expectations of users and enterprises, which demand systems that are both adaptive and capable of advanced problem-solving.

The architecture of the Multi-Agent System in CAMEL.AI comprises two main modules: the **Module of Task Driven** and the **Module of Dynamic Environment Maintenance**. 

The innovation of our system lies in a multi-faceted approach, incorporating tools such as Gantt charts, concurrent calls, memory retrieval, information extraction, and pre-prompt strategies, enabling our the Multi-Agent System to address a vast majority of practical challenges. These features are not only unique and insightful but also synergistic, as evidenced by our experiments and manual evaluations, which have shown combined application to exceed the industry expectations.

Moreover, in the realm of prompt engineering within the Multi-Agent System, the essential objective is to uphold generality and versatility of the system rather than confining it to niche domains like software development. To date, the deployment of the Multi-Agent System in many problem-solving scenarios — from mathematical reasoning and modeling to novel writing, software development, and educational instruction — has yielded results that surpass anticipated effectiveness.

## Installation
### Local Hosting
1. Clone the repository, and then navigate to the project directory:
    ``` sh
    git clone https://github.com/camel-ai/multi-agent-streamlit-ui.git
    cd multi-agent-streamlit-ui
    ```
2. Create and activate a virtual environment (optional but recommended):
    ``` sh
    python -m venv myenvname
    ./myenvname/Scripts/activate # Windows
    source myenvname/bin/activate # MacOS

    ```
3. Install the dependencies: 
    ``` sh
    python -m pip install --upgrade pip
    pip uninstall camel-ai  # Make sure you will get the latest version of Camel
    pip install streamlit
    pip install -r requirements.txt
    ```
4. Set up the streamlit app:
    ``` sh
    streamlit run streamlit_app.py
    ```
5. After starting the Streamlit application, if the system requires the API keys for certain functionalities, you will typically be prompted to enter them within the Streamlit UI. Enter your API keys in the designated field and submit or save it to enable the full features of the application. Ensure that your API key is kept secure and not shared publicly, as it might provide access to sensitive data or functionalities.
    - OpenAI API Key
    - Google API Key ([Google Cloud Console](https://cloud.google.com/))
    - Search Engine ID ([Google Custom Search JSON API page](https://developers.google.com/custom-search/v1/overview))

### Remote Hosting
1. This project is also available on a remote host for easier access and testing. You can find the application hosted: [CAMEL Multi-Agent UI](https://camel-multi-agent-ui.streamlit.app/).
2. After starting the Streamlit application, if the system requires the API keys for certain functionalities, you will typically be prompted to enter them within the Streamlit UI. Enter your API keys in the designated field and submit or save it to enable the full features of the application. Ensure that your API key is kept secure and not shared publicly, as it might provide access to sensitive data or functionalities.
    - OpenAI API Key
    - Google API Key ([Google Cloud Console](https://cloud.google.com/))
    - Search Engine ID ([Google Custom Search JSON API page](https://developers.google.com/custom-search/v1/overview))

### 🚨 Warnings
- ❗Cloud Deployment Stability: The cloud-hosted version of this application is still in testing phases and may be unstable or subject to downtime.
- ⌛Response Time: The free version hosted in the cloud may have longer response times.
- ⚠️Deployment Risk: Be aware of the risks associated with deploying this version, as it is public and still under active development.
- ⚠️ API Influence: The functionality of this version is also influenced by external API dependencies. If you encounter a failure in operation, please refresh the page and attempt to retry. This step can help resolve issues caused by temporary API disruptions or limitations.




## Documentation

[CAMEL package documentation pages](https://camel-ai.github.io/camel/)


## Acknowledgement
Special thanks to [Nomic AI](https://home.nomic.ai/) for giving us extended access to their data set exploration tool (Atlas).

We would also like to thank Haya Hammoud for designing the logo of our project.

## License

The intended purpose and licensing of CAMEL is solely for research use.

The source code is licensed under Apache 2.0.

The datasets are licensed under CC BY NC 4.0, which permits only non-commercial usage. It is advised that any models trained using the dataset should not be utilized for anything other than research purposes.

## Contributing to CAMEL 🐫
We appreciate your interest in contributing to our open-source initiative. We provide a document of [contributing guidelines](https://github.com/camel-ai/camel/blob/master/CONTRIBUTING.md) which outlines the steps for contributing to CAMEL. Please refer to this guide to ensure smooth collaboration and successful contributions. 🤝🚀

## Contact
For more information please contact camel.ai.team@gmail.com.
