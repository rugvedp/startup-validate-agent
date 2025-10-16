from crewai.flow.flow import Flow, start, listen
from crewai import Agent, Crew, Task, Process, LLM
from crewai_tools import SerperDevTool
from startup_validate.tools.custom_tool import QuickChartTool
from startup_validate.crew import StartupValidate as StartupValidateCrew
from typing import List
import os
import json
import yaml

class StartupValidateFlow(Flow):
    """StartupValidate Flow - Hierarchical Multi-Agent System"""
    
    # Configure Gemini LLM
    gemini_llm = LLM(
        model="gemini/gemini-2.0-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        max_rpm=13,
        temperature=0,
        stop=["<stop>"]
    )
    
    # Load configs
    agents_config = yaml.safe_load(open('/Users/rugvedpatil/Documents/crewai/startup_validate/src/startup_validate/config/agents.yaml'))   
    tasks_config = yaml.safe_load(open('/Users/rugvedpatil/Documents/crewai/startup_validate/src/startup_validate/config/tasks.yaml'))

    @start()
    def initialize_validation(self):
        """Initialize the startup validation process"""
        print("🚀 Starting Hierarchical Startup Validation Flow")
        print(f"Flow State ID: {self.state['id']}")
        
        # Store initial state
        self.state["validation_status"] = "initialized"
        self.state["startup_idea"] = "Sample startup idea"  # This would come from user input
        
        print("✅ Validation process initialized")
        return "Validation initialized"

    @listen(initialize_validation)
    def startup_validation_manager(self, initialization_result):
        """Manager Agent - Coordinates and oversees all specialist agents"""
        print("👑 Manager Agent: Coordinating startup validation process...")
        
        # Create manager agent
        manager_agent = Agent(
            config=self.agents_config['startup_validation_manager'],
            verbose=True,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )
        
        # Manager coordinates the validation process
        coordination_result = f"Manager coordinating validation for: {self.state['startup_idea']}"
        self.state["manager_coordination"] = coordination_result
        self.state["validation_status"] = "manager_coordinating"
        
        print("✅ Manager Agent activated and coordinating")
        return coordination_result

    @listen(startup_validation_manager)
    def run_market_analysis(self, manager_coordination):
        """Market Analyst - Analyzes market size, trends, and opportunities"""
        print("📊 Market Analyst: Analyzing market size and trends...")
        
        # Create market analyst agent
        market_agent = Agent(
            config=self.agents_config['market_analyst'],
            verbose=True,
            tools=[SerperDevTool()],
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )
        
        # Create market analysis task
        market_task = Task(
            config=self.tasks_config['market_analysis_task'],
            agent=market_agent
        )
        
        # Execute market analysis
        result = market_task.execute()
        
        # Store result in state
        self.state["market_analysis"] = result
        self.state["validation_status"] = "market_analysis_complete"
        
        print("✅ Market Analysis completed")
        return result

    @listen(startup_validation_manager)
    def run_competitive_analysis(self, manager_coordination):
        """Competitive Researcher - Researches competitors and market positioning"""
        print("🔍 Competitive Researcher: Analyzing competitive landscape...")
        
        # Create competitive researcher agent
        competitive_agent = Agent(
            config=self.agents_config['competitive_researcher'],
            verbose=True,
            tools=[SerperDevTool()],
            max_retry_limit=3,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )
        
        # Create competitive analysis task
        competitive_task = Task(
            config=self.tasks_config['competitive_analysis_task'],
            agent=competitive_agent
        )
        
        # Execute competitive analysis
        result = competitive_task.execute()
        
        # Store result in state
        self.state["competitive_analysis"] = result
        self.state["validation_status"] = "competitive_analysis_complete"
        
        print("✅ Competitive Analysis completed")
        return result

    @listen(startup_validation_manager)
    def run_business_model_analysis(self, manager_coordination):
        """Business Model Analyst - Evaluates revenue models and monetization"""
        print("💰 Business Model Analyst: Evaluating business models...")
        
        # Create business model analyst agent
        business_agent = Agent(
            config=self.agents_config['business_model_analyst'],
            verbose=True,
            tools=[SerperDevTool()],
            max_retry_limit=3,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )
        
        # Create business model task
        business_task = Task(
            config=self.tasks_config['business_model_task'],
            agent=business_agent
        )
        
        # Execute business model analysis
        result = business_task.execute()
        
        # Store result in state
        self.state["business_model_analysis"] = result
        self.state["validation_status"] = "business_model_analysis_complete"
        
        print("✅ Business Model Analysis completed")
        return result

    @listen(startup_validation_manager)
    def run_funding_analysis(self, manager_coordination):
        """Funding Analyst - Analyzes funding landscape and investor activity"""
        print("💼 Funding Analyst: Analyzing funding landscape...")
        
        # Create funding analyst agent
        funding_agent = Agent(
            config=self.agents_config['funding_analyst'],
            verbose=True,
            tools=[SerperDevTool()],
            max_retry_limit=3,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )
        
        # Create funding analysis task
        funding_task = Task(
            config=self.tasks_config['funding_analysis_task'],
            agent=funding_agent
        )
        
        # Execute funding analysis
        result = funding_task.execute()
        
        # Store result in state
        self.state["funding_analysis"] = result
        self.state["validation_status"] = "funding_analysis_complete"
        
        print("✅ Funding Analysis completed")
        return result

    @listen(startup_validation_manager)
    def run_validation_scoring(self, manager_coordination):
        """Validation Scorer - Provides comprehensive scoring and assessment"""
        print("📈 Validation Scorer: Providing comprehensive scoring...")
        
        # Create validation scorer agent
        scorer_agent = Agent(
            config=self.agents_config['validation_scorer'],
            verbose=True,
            tools=[SerperDevTool(), QuickChartTool()],
            max_retry_limit=3,
            llm=self.gemini_llm,
            respect_context_window=True,
            inject_date=True
        )
        
        # Create validation scoring task
        scoring_task = Task(
            config=self.tasks_config['validation_scoring_task'],
            agent=scorer_agent
        )
        
        # Execute validation scoring
        result = scoring_task.execute()
        
        # Store result in state
        self.state["validation_scoring"] = result
        self.state["validation_status"] = "validation_scoring_complete"
        
        print("✅ Validation Scoring completed")
        return result

    @listen(run_validation_scoring)
    def generate_final_report(self, validation_scoring_result):
        """Generate final comprehensive validation report"""
        print("📋 Generating Final Comprehensive Validation Report...")
        
        # Create comprehensive report
        final_report = {
            "startup_idea": self.state["startup_idea"],
            "flow_id": self.state["id"],
            "manager_coordination": self.state.get("manager_coordination", ""),
            "market_analysis": self.state.get("market_analysis", ""),
            "competitive_analysis": self.state.get("competitive_analysis", ""),
            "business_model_analysis": self.state.get("business_model_analysis", ""),
            "funding_analysis": self.state.get("funding_analysis", ""),
            "validation_scoring": self.state.get("validation_scoring", ""),
            "validation_status": "all_analyses_complete"
        }
        
        # Store final report in state
        self.state["final_report"] = final_report
        self.state["validation_status"] = "completed"
        
        print("✅ Final Comprehensive Report generated")
        return final_report

    @listen(generate_final_report)
    def save_results(self, final_report):
        """Save the validation results"""
        print("💾 Saving validation results...")
        
        # Create comprehensive report
        comprehensive_report = {
            "startup_idea": self.state["startup_idea"],
            "flow_id": self.state["id"],
            "manager_coordination": self.state.get("manager_coordination", ""),
            "market_analysis": self.state.get("market_analysis", ""),
            "competitive_analysis": self.state.get("competitive_analysis", ""),
            "business_model_analysis": self.state.get("business_model_analysis", ""),
            "funding_analysis": self.state.get("funding_analysis", ""),
            "validation_scoring": self.state.get("validation_scoring", ""),
            "final_report": final_report,
            "validation_status": self.state["validation_status"]
        }
        
        # Save results to file
        output_file = "startup_validation_results.json"
        with open(output_file, 'w') as f:
            json.dump(comprehensive_report, f, indent=2)
        
        self.state["output_file"] = output_file
        self.state["validation_status"] = "saved"
        
        print(f"✅ Results saved to {output_file}")
        return f"Results saved to {output_file}"

# Flow execution functions
def plot():
    """Generate a plot of the startup validation flow"""
    flow = StartupValidateFlow()
    flow.plot("flow_visualization")
    print("📊 Flow visualization saved as flow_visualization.html")

def kickoff():
    """Run the startup validation flow"""
    flow = StartupValidateFlow()
    result = flow.kickoff()
    print("🎉 Flow execution completed!")
    print(f"Final result: {result}")
    return result

if __name__ == "__main__":
    # Generate the flow plot
    plot()
    
    # Optionally run the flow (uncomment to execute)
    # kickoff()