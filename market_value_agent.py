# market_value_agent.py

from datetime import datetime

class MarketValueAgent:
    def __init__(self, data_agent=None, video_agent=None):
        self.data_agent = data_agent
        self.video_agent = video_agent
        self.market_trend_factor = 1.03  # example inflation factor
        
    def compute_market_value(self, player_id):
        if not self.data_agent or not self.video_agent:
            raise ValueError("Both data_agent and video_agent must be provided")
            
        # Get data from agents
        data_metrics = self.data_agent.get_player_metrics(player_id)
        video_score = self.video_agent.get_video_score(player_id)
        
        # Calculate performance score
        performance_score = (
            data_metrics['goals'] * 2.5 +
            data_metrics['assists'] * 1.8 +
            (data_metrics['minutes'] / 90) * 0.05
        )
        
        # Apply video score adjustment
        adjusted_score = performance_score * (0.8 + 0.4 * video_score)
        
        # Calculate factors
        age_factor = 1 - abs(26 - data_metrics['age']) * 0.03  # peak at age 26
        position_factors = {
            'forward': 1.2,
            'midfielder': 1.0,
            'defender': 0.8,
            'goalkeeper': 0.7
        }
        position_factor = position_factors.get(data_metrics['position'].lower(), 1.0)
        injury_penalty = (1 - data_metrics['injury_risk'])
        
        # Calculate final value
        raw_value = (
            adjusted_score * 
            age_factor * 
            position_factor * 
            injury_penalty * 
            self.market_trend_factor
        )
        
        # Prepare response
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