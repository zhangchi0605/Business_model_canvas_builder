from groq import Groq
import streamlit as st
import os
import tempfile
from crewai import Crew, Agent, Task, Process
import json
import os
import requests
from crewai_tools import tool
from crewai import Crew, Process
import tomllib
from langchain_groq import ChatGroq


# create title for the streamlit app

st.title('Business Model Canvas Builder')

# create a description

st.write(f"""This application will help you in building a business model canvas. A first team of agents will create an initial business model canvas based on a provided value proposition and customer segment. Subsequently, the second team of agents will critically analyze the business model canvas and try to maximize its consistency. For more information, contact Dries Faems at https://www.linkedin.com/in/dries-faems-0371569/""")

#ask user for groq api key in password form

groq_api_key = st.secrets["GROQ_API_KEY"]

# create a text input for the user to input the name of the customer

value_proposition = st.text_input('What is the value prposition for your business model')
customer_pofile = st.text_input('Please provide a description of the customer segment that you are targeting')


# create a button to start the generation of the business model canvas

if st.button('Start Business Model Canvas Generation'):
    os.environ["GROQ_API_KEY"] = groq_api_key
    client = Groq()
    GROQ_LLM = ChatGroq(
            # api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-70b-8192"
        )
    customer_relationship_analyzer = Agent(
        role='Analyzing customer relationships for the business model',
        goal=f"""Analyze the optimal customer relationship for the business model.""", 
        backstory=f"""You are a great expert in analyzing the customer relationships for a business model. The customer relationship dimension of the Business Model Canvas describes the type of relationship a company establishes with its customers. It covers how a business interacts with its customers, manages customer expectations, and fosters customer loyalty. """,
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )

    distribution_channel_analyzer = Agent(
        role='Analyzing distribution channels for the business model',
        goal=f"""Analyze the optimal distribution channels for the business model.""",
        backstory=f"""You are a great expert in analyzing the distirubtion channel for a business model. The Distribution Model dimension of the Business Model Canvas refers to the way a company delivers its value proposition to customers. It involves the channels through which a product or service reaches the end customer and includes the methods used to distribute, sell, and deliver offerings.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )

    revenue_streams_analyzer = Agent(
        role='Analyzing revenue streams for the business model',
        goal=f"""Analyze the optimal revenue streams for the business model.""",
        backstory="""You are a great expert in analyzing the revenue streams for the business model. The Revenue Streams dimension of the Business Model Canvas refers to the various ways in which a business generates income from each customer segment. It outlines how a company makes money by detailing the sources of revenue and the mechanisms used to capture value from customers. This dimension helps to clarify which methods are most effective and sustainable for the business's financial health.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )
    cost_structure_analyzer = Agent(
        role='Analyzing cost structure for the business model',
        goal=f"""Analyze the optimal cost structure for the business model.""",
        backstory="""You are a great expert in analyzing the cost structure for the business model. The Cost Structure dimension of the Business Model Canvas refers to the expenses incurred by a business to operate and deliver its value proposition. It includes all costs associated with running the business, such as fixed and variable costs, direct and indirect costs, and one-time and ongoing expenses. By analyzing the cost structure, you can identify opportunities to reduce costs, increase efficiency, and improve profitability.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )

    key_activities_analyzer = Agent(
        role='Analyzing key activities for the business model',
        goal=f"""Analyze the optimal key activities for the business model.""",
        backstory="""You are a great expert in analyzing the key activities for the business model. The Key Activities dimension of the Business Model Canvas refers to the most important tasks and processes a business must perform to deliver its value proposition. It includes the core activities that drive the business's operations, create value for customers, and differentiate the company from competitors. By analyzing the key activities, you can identify the critical tasks that need to be performed and optimize the processes to achieve the business's strategic goals.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )

    key_resources_analyzer = Agent(
        role='Analyzing key resources for the business model',
        goal=f"""Analyze the optimal key resources for the business model.""",
        backstory="""You are a great expert in analyzing the key resources for the business model. The Key Resources dimension of the Business Model Canvas refers to the strategic assets a business needs to deliver its value proposition, reach its customer segments, and sustain its operations. It includes the physical, intellectual, human, and financial resources required to run the business effectively. By analyzing the key resources, you can identify the critical assets that are essential for the business's success and optimize their allocation to maximize value creation.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )

    key_partnerships_analyzer = Agent(
        role='Analyzing key partnerships for the business model',
        goal=f"""Analyze the optimal key partnerships for the business model.""",
        backstory="""You are a great expert in analyzing the key partnerships for the business model. The Key Partnerships dimension of the Business Model Canvas refers to the external relationships a business forms to leverage resources, share risks, and create value for customers. It includes the strategic alliances, joint ventures, and collaborations that help a company expand its reach, access new markets, and enhance its capabilities. By analyzing the key partnerships, you can identify the most valuable relationships that can drive growth, innovation, and competitive advantage for the business.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )

    business_model_canvas_reporter = Agent(
        role='Reporting the business model canvas',
        goal=f"""Report the business model canvas to provide a clear overview of the business model.""",
        backstory="""You are a great expert in reporting the business model canvas. The Business Model Canvas is a strategic management tool that helps businesses to visualize, design, and describe their business model. By reporting the business model canvas, you provide a clear overview of the business model and its key elements. This report can be used to communicate the business model to stakeholders, investors, and other interested parties.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )
    


    # Create tasks for the agents
    generate_customer_relationships = Task(
        description=f"""Generate a customer relationship description that can be used for the business model canvas. The value proposition for the business model is: {value_proposition}. The customer profile is: {customer_pofile}.""",
        expected_output='As output, you provide a clear description of the customer relationship dimension for the business model canvas.',
        agent=customer_relationship_analyzer
    )

    generate_ditribution_channels = Task(
        description=f"""Generate a distribution channel description that can be used for the business model canvas. The value proposition for the business model is: {value_proposition}. The customer profile is: {customer_pofile}.""",
        expected_output="""As output, you provide a clear description of the distribution channel dimension for the business model canvas.""",
        agent=distribution_channel_analyzer
    )

    generate_revnue_streams = Task(
        description=f"""Generate a revenue stream description that can be used for the business model canvas. The value proposition for the business model is: {value_proposition}. The customer profile is: {customer_pofile}..""",
        expected_output='As output, you provide a clear description of the revenue stream dimensio for the busimess model canvas.',
        agent=revenue_streams_analyzer
    )

    generate_cost_structure = Task(
        description=f"""Generate a cost structure description that can be used for the business model canvas. The value proposition for the business model is: {value_proposition}. The customer profile is: {customer_pofile}..""",
        expected_output='As output, you provide a clear description of the cost structure dimension for the business model canvas.',
        agent=cost_structure_analyzer
    )

    generate_key_activities = Task(
        description=f"""Generate a key activities description that can be used for the business model canvas. The value proposition for the business model is: {value_proposition}. The customer profile is: {customer_pofile}..""",
        expected_output='As output, you provide a clear description of the key activities dimension for the business model canvas.',
        agent=key_activities_analyzer
    )

    generate_key_resources = Task(
        description=f"""Generate a key resources description that can be used for the business model canvas. The value proposition for the business model is: {value_proposition}. The customer profile is: {customer_pofile}..""",
        expected_output='As output, you provide a clear description of the key resources dimension for the business model canvas.',
        agent=key_resources_analyzer
    )

    generate_key_partnerships = Task(
        description=f"""Generate a key partnerships description that can be used for the business model canvas. The value proposition for the business model is: {value_proposition}. The customer profile is: {customer_pofile}..""",
        expected_output='As output, you provide a clear description of the key partnerships dimension for the business model canvas.',
        agent=key_partnerships_analyzer
    )   

    report_business_model_canvas = Task(
        description=f"""Compile a report of the business model canvas by using the outputs generated by the customer relationship, distribution channel, revenue streams, cost structure, key activities, key resources, and key partnerships analyzers.""",
        expected_output='As output, provide a comprehensive report of the business model canvas, including all key dimensions analyzed by the prior agents as well as the value proposition and customer segment.',
        agent=business_model_canvas_reporter
    )


    # Instantiate the first crew with a sequential process
    crew = Crew(
        agents=[customer_relationship_analyzer, distribution_channel_analyzer, revenue_streams_analyzer, cost_structure_analyzer, key_activities_analyzer, key_resources_analyzer, key_partnerships_analyzer,  business_model_canvas_reporter],
        tasks=[generate_customer_relationships, generate_ditribution_channels, generate_revnue_streams, generate_cost_structure, generate_key_activities, generate_key_resources, generate_key_partnerships,  report_business_model_canvas],
        verbose=2,
        process=Process.sequential,
        full_output=True,
        share_crew=False,
    )
    # Kick off the crew's work and capture results
    results = crew.kickoff()
    
    # turn generate_interview_question into string and select substring after 'raw=' and before 'pydantic'

    initial_business_model_canvas = report_business_model_canvas.output.raw_output
    st.markdown("**Initial Business Model Canvas**")
    st.write(report_business_model_canvas.output.raw_output)

    #create second crew to optimize the business model canvas

    business_model_canvas_criticizer = Agent(
        role='Critiquing the business model canvas',
        goal=f"""Critique the business model canvas to identify areas for improvement and optimization. Pay special attention to inconsistencies between different parts of the business model.""",
        backstory = """You have more than 20 years of experience in evaluating business models. You are great in spotting inconsistencies in business models.""",
        verbose = True,
        llm = GROQ_LLM,
        allow_delegation = False,
        max_iter=5,
        memory=True,
    )

    business_model_canvas_optimizer = Agent(
        role='Optimize the business model canvas',
        goal=f"""Optimize the business model canvas by addressing the issues identified by the business_model_canvas_criticizer.""",
        backstory="""You are an expert in optimizing the business model canvas. You find creative ways to address the issues raised by the business_model_canvas_criticizer.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )
    business_model_canvas_reporter = Agent(
        role='Reporting the business model canvas',
        goal=f"""Report the business model canvas to provide a clear overview of the business model.""",
        backstory="""You are a great expert in reporting the business model canvas. By reporting the business model canvas, you provide a clear overview of the business model and its key elements. This report can be used to communicate the business model to stakeholders, investors, and other interested parties.""",
        verbose=True,
        llm=GROQ_LLM,
        allow_delegation=False,
        max_iter=5,
        memory=True,
    )

    # Create tasks for the agents
    critique_business_model_canvas = Task(
        description=f"""Critique the business model canvas to identify areas for improvement and optimization. The initial business model canvas is: {initial_business_model_canvas}.""",
        expected_output='As output, provide a list of potential inconsistencies among the different parts of the business models that need to be addressed.',
        agent=business_model_canvas_criticizer
    )

    optimize_business_model_canvas = Task(
        description=f"""Optimize the business model canvas to ensure that you adress the critical issues raised.""",
        expected_output='As output, provide an opimitzed business model canvas that solves as much as possible the critical issues identified in the analysis of the business_model_canvas_criticizer.',
        agent=business_model_canvas_optimizer
    )

    report_business_model_canvas = Task(
        description=f"""Compile a report of the business model canvas by using the outputs generated by the business model canvas aligner.""",
        expected_output='As output, provide a comprehensive report of the business model canvas, including all key dimensions analyzed by the prior agents as well as the value proposition and customer segment.',
        agent=business_model_canvas_reporter
    )

    # Instantiate the second crew with a sequential process

    second_crew = Crew(
        agents=[business_model_canvas_criticizer, business_model_canvas_optimizer, business_model_canvas_reporter],
        tasks=[critique_business_model_canvas, optimize_business_model_canvas, report_business_model_canvas],
        verbose=2,
        process=Process.sequential,
        full_output=True,
        share_crew=False,
    )

    # Kick off the crew's work
    second_results = second_crew.kickoff()

    st.markdown("**Optimizing Business Model Canvas**")
    st.write(f"""{critique_business_model_canvas.output.raw_output}""")
    st.write(f"""{report_business_model_canvas.output.raw_output}""")

else:
    st.write('Please click the button to start the interview')
