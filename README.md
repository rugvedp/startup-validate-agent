# StartupValidate Crew

Welcome to the StartupValidate Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `GEMINI_API_KEY` into the `.env` file**

- Modify `src/startup_validate/config/agents.yaml` to define your agents
- Modify `src/startup_validate/config/tasks.yaml` to define your tasks
- Modify `src/startup_validate/crew.py` to add your own logic, tools and specific args
- Modify `src/startup_validate/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the startup_validate Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The startup_validate Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

### Agents and Roles

- **market_analyst**: Startup Market Research Specialist
  - Focus: Market size (TAM/SAM/SOM), industry trends, maturity, demand dynamics
  - Output: Market sizing with assumptions/formulas, trends analysis, scenarios and sensitivity notes

- **competitive_researcher**: Competitive Intelligence Analyst
  - Focus: Direct/indirect competitors, substitutes, positioning, differentiation, barriers to entry
  - Output: Competitor tables with sourced metrics, positioning insights, gaps and differentiation strategies

- **business_model_analyst**: Business Model & Monetization Expert
  - Focus: Revenue models, pricing benchmarks, target segments, unit economics, go-to-market (GTM)
  - Output: Pricing/monetization options, unit economics mini-model, phased GTM plan, risks and mitigations

- **funding_analyst**: Startup Funding & Investment Specialist
  - Focus: Funding trends, active investors, round sizes, valuations, regional/stage patterns
  - Output: Representative deals with sources, investor landscape, fundraising strategy and runway planning

- **validation_scorer**: Startup Validation & Scoring Expert
  - Focus: Multi-dimensional scoring and investment readiness
  - Output: Weighted rubric, rationale per dimension, strengths/weaknesses, recommendations, charts

- **startup_validation_manager**: Project Manager (Manager Agent)
  - Focus: Planning, delegation, cross-verification, synthesis
  - Output: A single, publication-quality, long-form markdown report with inline citations and full references that integrates all specialist outputs. The manager does not use tools directly and is not a chatbot; it receives only the startup idea and must coordinate specialists to cover all aspects before producing the final report.

### Tasks and Flow

Tasks are defined in `src/startup_validate/config/tasks.yaml` and executed hierarchically with the manager coordinating:

1. `market_analysis_task` → Market sizing and trends
2. `competitive_analysis_task` → Competitive landscape and positioning
3. `business_model_task` → Monetization, pricing, unit economics, GTM
4. `funding_analysis_task` → Investor and funding ecosystem
5. `validation_scoring_task` → Scoring and readiness assessment
6. `manager_report_task` → Manager synthesizes a comprehensive final report

Each specialist produces detailed, citation-rich markdown. The manager aggregates and synthesizes these into the final output, ensuring completeness, evidence quality, and clarity.

### Visualizations with QuickChart

Specialists can suggest or embed charts via QuickChart to visualize key insights (e.g., scoring radar charts, market breakdowns). The manager embeds these visuals (from specialists) in the final markdown report with captions and sources.

### Output

- Final output: A single long-form markdown report with inline citations and a References section.
- Saved path (example): written to `res.md` by `main.py` when you run locally.

## Support

For support, questions, or feedback regarding the StartupValidate Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
