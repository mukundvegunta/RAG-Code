# market_value_agent.py

#This market value agent will first take in data from the data analysis agent and video agent. 
#Next, it will calculate market value using a series of equations for different player factors including performance, age, injury susceptibility,etc.
#The agent will combine the different equation values into a variable called raw_value which is rounded to 2 digits via the estimated_value_million variable.
#The confidence variable tracks the reliability of the market value score though considering factors like injury risk which may make the value of a player unpredictable.
#The output is structured in neat columns.

from datetime import datetime

class MarketValueAgent:
    def __init__(self, data_agent, video_agent):
        self.data_agent = data_agent
        self.video_agent = video_agent
        self.market_trend_factor = 1.03  # example inflation factor: sports transfer market increase in prices per year

    def compute_market_value(self, player_id):
        #Step 1: Gather data from other agents
        data_metrics = self.data_agent.get_player_metrics(player_id)
        video_score = self.video_agent.get_video_score(player_id)

        # Step 2: Base model using performance data
        # Assume data_agent returns dict like:
        # {'goals': 10, 'assists': 5, 'minutes': 1500, 'age': 24, 'position': 'forward', 'injury_risk': 0.1}
        performance_score = (
            data_metrics['goals'] * 2.5 +
            data_metrics['assists'] * 1.8 +
            (data_metrics['minutes'] / 90) * 0.05
        )

        # Step 3: Apply video qualitative adjustment
        # video_score might be between 0 and 1: will change according to scoring format used in video agent
        adjusted_score = performance_score * (0.8 + 0.4 * video_score)

        #Step 4: Adjust for other factors
        age_factor = 1 - abs(26 - data_metrics['age']) * 0.03  # peak value around age 26
        position_factor = {'forward': 1.2, 'midfielder': 1.0, 'defender': 0.8, 'goalkeeper': 0.7}.get(data_metrics['position'], 1)
        injury_penalty = (1 - data_metrics['injury_risk'])

        #Step 5: Combine all factors
        raw_value = adjusted_score * age_factor * position_factor * injury_penalty * self.market_trend_factor

        #Step 6: Output structured response
        estimated_value_million = round(raw_value, 2)
        confidence = round(0.8 + 0.2 * video_score * (1 - data_metrics['injury_risk']), 2)

        return {
            "player_id": player_id,
            "estimated_value_million": estimated_value_million,
            "confidence": confidence,
            "last_updated": datetime.now().isoformat(),
            "explanation": {
                "data_metrics": data_metrics,
                "video_score": video_score,
                "factors": {
                    "age_factor": age_factor,
                    "position_factor": position_factor,
                    "injury_penalty": injury_penalty
                }
            }
        }
    


# Example Use Case: will change according to title of data analysis agent and video agent
from data_agent import DataAnalysisAgent
from video_agent import VideoAgent

data_agent = DataAnalysisAgent()
video_agent = VideoAgent()
market_agent = MarketValueAgent(data_agent, video_agent)

player_value = market_agent.compute_market_value("player_123") #replace with actual player
print(player_value)