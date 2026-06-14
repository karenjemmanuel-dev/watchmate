from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, Task, Crew, Process
from crewai.flow.flow import Flow, listen, start
import pandas as pd
from datetime import datetime

# ============================================================================
# CREW 1: DATA ANALYST CREW
# ============================================================================

data_analyst_agent = Agent(
    role="Data Analyst",
    goal="Load, validate, and explore the MovieLens dataset",
    backstory="Expert data analyst specializing in quality assurance and exploratory analysis"
)

eda_agent = Agent(
    role="EDA Specialist", 
    goal="Generate comprehensive exploratory data analysis",
    backstory="Specialist in creating insights from data through visualization and statistics"
)

data_validation_agent = Agent(
    role="Data Validator",
    goal="Ensure data quality and document dataset contract",
    backstory="Meticulous validator who documents data schemas and constraints"
)

# Data Analyst Tasks
load_data_task = Task(
    description="Load the MovieLens 100K dataset and validate structure",
    agent=data_analyst_agent,
    expected_output="Dataset loaded successfully with 100,000 ratings and 1,682 movies"
)

eda_task = Task(
    description="Generate exploratory data analysis report",
    agent=eda_agent,
    expected_output="EDA report showing rating distribution, top movies, data quality metrics"
)

validation_task = Task(
    description="Create dataset contract documenting schema and constraints",
    agent=data_validation_agent,
    expected_output="dataset_contract.json with column definitions and data quality metrics"
)

# Create Data Analyst Crew
data_analyst_crew = Crew(
    agents=[data_analyst_agent, eda_agent, data_validation_agent],
    tasks=[load_data_task, eda_task, validation_task],
    process=Process.sequential,
    verbose=True
)

# ============================================================================
# CREW 2: DATA SCIENTIST CREW
# ============================================================================

feature_engineer_agent = Agent(
    role="Feature Engineer",
    goal="Prepare features for machine learning model",
    backstory="Expert in transforming raw data into model-ready features"
)

model_training_agent = Agent(
    role="Model Trainer",
    goal="Train and compare multiple ML models",
    backstory="Specialist in training Random Forest and Gradient Boosting models"
)

model_evaluator_agent = Agent(
    role="Model Evaluator",
    goal="Evaluate models and select the best performer",
    backstory="Expert in model evaluation, producing comprehensive model cards"
)

# Data Scientist Tasks
feature_task = Task(
    description="Engineer features from MovieLens data for model training",
    agent=feature_engineer_agent,
    expected_output="features.csv with prepared features for modeling"
)

training_task = Task(
    description="Train Random Forest and Gradient Boosting models on 80K training samples",
    agent=model_training_agent,
    expected_output="Two trained models with performance metrics on 20K test set"
)

evaluation_task = Task(
    description="Evaluate models and produce model card with metrics and limitations",
    agent=model_evaluator_agent,
    expected_output="model_card.md with RMSE, MAE, R² scores and ethical considerations"
)

# Create Data Scientist Crew
data_scientist_crew = Crew(
    agents=[feature_engineer_agent, model_training_agent, model_evaluator_agent],
    tasks=[feature_task, training_task, evaluation_task],
    process=Process.sequential,
    verbose=True
)

# ============================================================================
# FLOW: ORCHESTRATE BOTH CREWS
# ============================================================================

class WatchMateFlow(Flow):
    @start()
    def run_data_analysis(self):
        """Run Data Analyst Crew first"""
        print("\n" + "="*60)
        print("CREW 1: DATA ANALYST CREW")
        print("="*60)
        
        result = data_analyst_crew.kickoff()
        print(f"\nData Analysis Complete: {result}")
        return result
    
    @listen(run_data_analysis)
    def run_data_science(self, analyst_result):
        """Run Data Scientist Crew after validation"""
        print("\n" + "="*60)
        print("CREW 2: DATA SCIENTIST CREW")
        print("="*60)
        
        result = data_scientist_crew.kickoff()
        print(f"\nModel Training Complete: {result}")
        return result

# ============================================================================
# RUN THE FLOW
# ============================================================================

if __name__ == "__main__":
    print("Starting WatchMate CrewAI Flow...")
    print(f"Timestamp: {datetime.now()}")
    
    flow = WatchMateFlow()
    result = flow.kickoff()
    
    print("\n" + "="*60)
    print("✓ WatchMate Pipeline Complete!")
    print("="*60)
    print("\nDeliverables generated:")
    print("  ✓ clean_data.csv")
    print("  ✓ eda_report.html")
    print("  ✓ dataset_contract.json")
    print("  ✓ features.csv")
    print("  ✓ model.pkl")
    print("  ✓ model_card.md")