Invisible Crisis AI 

AI-powered early warning system that detects community environmental risks before they escalate into full-scale crises.

What It Does

Communities often face slow-building crises like contaminated water, unsafe transport, power outages that go unreported until it's too
late. Invisible Crisis AI gives residents a way to report issues in real time and uses AI to detect patterns, score risk level
and recommend urgent actions before things spiral.

Features

- Live risk heatmap — visualises high-risk zones across the community
- AI response engine — powered by Mistral AI, generates actionable crisis response plans
- Incident trend tracking — shows how reports are building over time
- Automatic risk scoring — classifies reports into Health, Safety, and Infrastructure categories
- Community report submission — residents can submit issues directly in the app
- Real-time simulation — simulates incoming reports for demo and testing purposes

Tech Stack

Tool | Purpose 

Python | Core language

Streamlit | Web app framework 

Pandas | Data processing 

Plotly | Interactive charts and heatmap 

Mistral AI API | AI-generated crisis response plans 

Scikit-learn | Text vectorisation and clustering 

Faker | Synthetic data generation for simulation 

How to Run Locally

1. Clone the repo
```bash git clone https://github.com/galaletsangmodise/Invisible-Crisis-AI-App.git
cd Invisible-Crisis-AI-App
```

2.Install dependencies

```bash pip install -r requirements.txt```

3. Set up your API key
   
Create a `.env` file in the root folder:
```MISTRAL_API_KEY=your_api_key_here```

4. Run the app
   
```bash streamlit run app.py```

Project Structure
Invisible-Crisis-AI-App/
├── app.py               # Main Streamlit application

├── reports.csv          # Community reports dataset

├── requirements.txt     # Python dependencies

├── .env                 # API key (not pushed to GitHub)

├── .gitignore           # Excludes .env from version control

└── README.md            # Project documentation


Why I Built This

I've seen how slow information flow turns small community problems into full-scale crises. This project is my attempt to use 
AI to give communities an early warning system  turning scattered resident reports into actionable intelligence for decision-makers.

Author

Galaletsang Modise
Self-taught Data Analyst | Johannesburg, South Africa  
[GitHub](https://github.com/galaletsangmodise) • [LinkedIn](https://www.linkedin.com/in/galaletsang-modise-33a734264?utm_source=share_via&utm_content=profile&utm_medium=member_ios)



*Built as part of an AI hackathon project — April 2026
