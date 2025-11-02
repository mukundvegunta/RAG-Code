import random
from datetime import datetime
import numpy as np

class MockDataAgent:
    """Mock data agent that generates sample player data with intentional mistakes"""
    
    def __init__(self, error_rate=0.2):
        self.error_rate = error_rate
        self.known_mistakes = {}  # Track introduced mistakes for evaluation
        
    def _introduce_error(self, value, field_name, player_id):
        """Randomly introduce errors in data based on error_rate"""
        if random.random() < self.error_rate:
            if isinstance(value, (int, float)):
                # Introduce significant deviation (±50%)
                error_multiplier = random.uniform(0.5, 1.5)
                wrong_value = value * error_multiplier
                
                self.known_mistakes[f"{player_id}_{field_name}"] = {
                    "original": value,
                    "erroneous": wrong_value,
                    "error_type": "value_inflation" if error_multiplier > 1 else "value_deflation",
                    "error_magnitude": abs(1 - error_multiplier)
                }
                return wrong_value
        return value

    def get_player_metrics(self, player_id):
        """Generate sample player metrics with potential errors"""
        
        # Base stats (realistic ranges for a season)
        base_metrics = {
            'goals': random.randint(0, 30),
            'assists': random.randint(0, 20),
            'minutes': random.randint(500, 3000),
            'age': random.randint(17, 40),
            'position': random.choice(['forward', 'midfielder', 'defender', 'goalkeeper']),
            'injury_risk': round(random.uniform(0.05, 0.4), 2)
        }
        
        # Apply potential errors to each metric
        metrics_with_errors = {
            key: self._introduce_error(value, key, player_id) 
            for key, value in base_metrics.items()
        }
        
        return metrics_with_errors

class MockVideoAgent:
    """Mock video agent that generates sample video scores with intentional mistakes"""
    
    def __init__(self, error_rate=0.2):
        self.error_rate = error_rate
        self.known_mistakes = {}
        
    def get_video_score(self, player_id):
        """Generate a sample video score (0-1) with potential errors"""
        true_score = random.uniform(0.3, 0.9)
        
        if random.random() < self.error_rate:
            # Introduce significant deviation (±40%)
            error_multiplier = random.uniform(0.6, 1.4)
            wrong_score = min(1.0, true_score * error_multiplier)  # Cap at 1.0
            
            self.known_mistakes[player_id] = {
                "original_score": true_score,
                "erroneous_score": wrong_score,
                "error_type": "score_inflation" if error_multiplier > 1 else "score_deflation",
                "error_magnitude": abs(1 - error_multiplier)
            }
            return wrong_score
            
        return true_score

def evaluate_market_value_agent(num_players=10):
    """Run evaluation with multiple sample players and collect mistakes"""
    
    # Initialize agents
    mock_data = MockDataAgent(error_rate=0.3)  # 30% chance of errors in data
    mock_video = MockVideoAgent(error_rate=0.2)  # 20% chance of errors in video scores
    
    from market_value_agent import MarketValueAgent
    market_agent = MarketValueAgent(mock_data, mock_video)
    
    evaluation_results = {
        "total_players": num_players,
        "data_mistakes": mock_data.known_mistakes,
        "video_mistakes": mock_video.known_mistakes,
        "predictions": [],
        "timestamp": datetime.now().isoformat()
    }
    
    # Generate and evaluate multiple players
    for i in range(num_players):
        player_id = f"test_player_{i}"
        
        try:
            # Get market value prediction
            prediction = market_agent.compute_market_value(player_id)
            evaluation_results["predictions"].append({
                "player_id": player_id,
                "prediction": prediction,
                "has_data_errors": any(k.startswith(player_id) for k in mock_data.known_mistakes),
                "has_video_errors": player_id in mock_video.known_mistakes
            })
        except Exception as e:
            evaluation_results["predictions"].append({
                "player_id": player_id,
                "error": str(e)
            })
    
    return evaluation_results

if __name__ == "__main__":
    # Run evaluation with 10 sample players
    results = evaluate_market_value_agent(10)
    
    # Print summary
    print("\nEvaluation Summary:")
    print(f"Total players evaluated: {results['total_players']}")
    print(f"\nData mistakes introduced: {len(results['data_mistakes'])}")
    print(f"Video score mistakes introduced: {len(results['video_mistakes'])}")
    
    print("\nDetailed mistakes:")
    print("\nData mistakes:")
    for key, mistake in results['data_mistakes'].items():
        print(f"{key}:")
        print(f"  Original value: {mistake['original']}")
        print(f"  Erroneous value: {mistake['erroneous']}")
        print(f"  Error type: {mistake['error_type']}")
        print(f"  Error magnitude: {mistake['error_magnitude']:.2%}")
    
    print("\nVideo score mistakes:")
    for player_id, mistake in results['video_mistakes'].items():
        print(f"{player_id}:")
        print(f"  Original score: {mistake['original_score']:.2f}")
        print(f"  Erroneous score: {mistake['erroneous_score']:.2f}")
        print(f"  Error type: {mistake['error_type']}")
        print(f"  Error magnitude: {mistake['error_magnitude']:.2%}")