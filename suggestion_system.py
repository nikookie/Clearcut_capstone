# improved_suggestion_system.py
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum

class WoodCondition(Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    BAD = "bad"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class FurnitureProject:
    name: str
    difficulty: DifficultyLevel
    min_condition: WoodCondition
    durability_required: str
    typical_cost_range: str
    description: str

@dataclass
class WoodProperties:
    hardness: str  # "soft", "medium", "hard"
    durability: str  # "low", "medium", "high", "very_high"
    workability: str  # "easy", "moderate", "difficult"
    finish_quality: str  # "good", "excellent", "premium"
    moisture_resistance: str  # "low", "medium", "high"
    price_category: str  # "budget", "mid_range", "premium", "luxury"

class ImprovedWoodSuggestionSystem:
    def __init__(self):
        # Enhanced wood database with properties
        self.wood_database = {
            "Mahogany": WoodProperties(
                hardness="hard",
                durability="very_high", 
                workability="moderate",
                finish_quality="premium",
                moisture_resistance="high",
                price_category="luxury"
            ),
            "Narra": WoodProperties(
                hardness="hard",
                durability="very_high",
                workability="moderate", 
                finish_quality="premium",
                moisture_resistance="high",
                price_category="luxury"
            ),
            "Pine": WoodProperties(
                hardness="soft",
                durability="medium",
                workability="easy",
                finish_quality="good",
                moisture_resistance="low",
                price_category="budget"
            ),
            "Oak": WoodProperties(
                hardness="hard",
                durability="very_high",
                workability="difficult",
                finish_quality="excellent", 
                moisture_resistance="high",
                price_category="premium"
            ),
            "Acacia": WoodProperties(
                hardness="hard",
                durability="high",
                workability="moderate",
                finish_quality="excellent",
                moisture_resistance="high",
                price_category="mid_range"
            ),
            "Teak": WoodProperties(
                hardness="hard",
                durability="very_high",
                workability="moderate",
                finish_quality="premium", 
                moisture_resistance="high",
                price_category="luxury"
            ),
            "Cedar": WoodProperties(
                hardness="soft",
                durability="high",
                workability="easy",
                finish_quality="good",
                moisture_resistance="high",
                price_category="mid_range"
            )
        }
        
        # Comprehensive furniture project database
        self.furniture_projects = {
            "indoor_furniture": [
                FurnitureProject("Coffee Table", DifficultyLevel.BEGINNER, WoodCondition.GOOD, 
                                "medium", "$50-200", "Perfect starter project with visible grain"),
                FurnitureProject("Dining Table", DifficultyLevel.INTERMEDIATE, WoodCondition.GOOD,
                                "high", "$200-800", "Requires strong, durable wood for daily use"),
                FurnitureProject("Bookshelf", DifficultyLevel.BEGINNER, WoodCondition.FAIR,
                                "medium", "$30-150", "Great for practicing joints and finishing"),
                FurnitureProject("Kitchen Cabinets", DifficultyLevel.ADVANCED, WoodCondition.GOOD,
                                "high", "$500-2000", "Needs moisture-resistant wood with good finish"),
                FurnitureProject("Bed Frame", DifficultyLevel.INTERMEDIATE, WoodCondition.GOOD,
                                "high", "$150-600", "Requires strong wood for structural support"),
                FurnitureProject("Wardrobe", DifficultyLevel.EXPERT, WoodCondition.EXCELLENT,
                                "high", "$400-1500", "Complex project requiring premium materials")
            ],
            "outdoor_furniture": [
                FurnitureProject("Garden Bench", DifficultyLevel.BEGINNER, WoodCondition.GOOD,
                                "high", "$80-300", "Needs weather-resistant wood"),
                FurnitureProject("Outdoor Dining Set", DifficultyLevel.INTERMEDIATE, WoodCondition.EXCELLENT,
                                "very_high", "$300-1200", "Must withstand weather and heavy use"),
                FurnitureProject("Deck Railing", DifficultyLevel.ADVANCED, WoodCondition.EXCELLENT,
                                "very_high", "$200-800", "Critical for safety, needs premium wood")
            ],
            "decorative": [
                FurnitureProject("Picture Frames", DifficultyLevel.BEGINNER, WoodCondition.FAIR,
                                "low", "$10-50", "Good for practicing precision cuts"),
                FurnitureProject("Wooden Bowls", DifficultyLevel.INTERMEDIATE, WoodCondition.GOOD,
                                "medium", "$20-100", "Showcases wood grain beautifully"),
                FurnitureProject("Carved Sculptures", DifficultyLevel.EXPERT, WoodCondition.EXCELLENT,
                                "low", "$50-500", "Requires premium wood with fine grain")
            ]
        }

    def _get_condition_score(self, condition: str) -> int:
        """Convert condition to numeric score for comparison"""
        condition_scores = {
            "bad": 1, "poor": 2, "fair": 3, "good": 4, "excellent": 5
        }
        return condition_scores.get(condition.lower(), 3)

    def _condition_meets_requirement(self, actual_condition: str, required_condition: WoodCondition) -> bool:
        """Check if wood condition meets project requirements"""
        actual_score = self._get_condition_score(actual_condition)
        required_score = self._get_condition_score(required_condition.value)
        return actual_score >= required_score

    def _calculate_suitability_score(self, wood_type: str, project: FurnitureProject, condition: str) -> float:
        """Calculate how suitable a wood is for a specific project"""
        if wood_type not in self.wood_database:
            return 0.0
            
        wood_props = self.wood_database[wood_type]
        score = 0.0
        
        # Condition compatibility (40% weight)
        if self._condition_meets_requirement(condition, project.min_condition):
            score += 0.4
        
        # Durability match (30% weight)
        durability_match = {
            ("low", "low"): 0.3, ("medium", "medium"): 0.3, ("high", "high"): 0.3, ("very_high", "very_high"): 0.3,
            ("medium", "low"): 0.25, ("high", "low"): 0.3, ("very_high", "low"): 0.3,
            ("high", "medium"): 0.25, ("very_high", "medium"): 0.3,
            ("very_high", "high"): 0.25
        }
        score += durability_match.get((wood_props.durability, project.durability_required), 0.0)
        
        # Workability vs difficulty (20% weight)
        workability_difficulty_match = {
            ("easy", DifficultyLevel.BEGINNER): 0.2,
            ("moderate", DifficultyLevel.INTERMEDIATE): 0.2, 
            ("moderate", DifficultyLevel.ADVANCED): 0.15,
            ("difficult", DifficultyLevel.ADVANCED): 0.2,
            ("difficult", DifficultyLevel.EXPERT): 0.2
        }
        score += workability_difficulty_match.get((wood_props.workability, project.difficulty), 0.0)
        
        # Special bonuses (10% weight)
        if "outdoor" in project.name.lower() and wood_props.moisture_resistance == "high":
            score += 0.05
        if "premium" in project.description.lower() and wood_props.finish_quality == "premium":
            score += 0.05
            
        return min(score, 1.0)  # Cap at 1.0

    def get_comprehensive_suggestions(self, wood_type: str, condition: str, confidence: float, 
                                   skill_level: Optional[DifficultyLevel] = None) -> Dict:
        """Get comprehensive furniture suggestions with detailed analysis"""
        
        # Input validation
        condition = condition.lower()
        if condition not in ["excellent", "good", "fair", "poor", "bad"]:
            return {"error": "Invalid condition. Use: excellent, good, fair, poor, or bad"}
            
        if confidence < 0 or confidence > 1:
            return {"error": "Confidence must be between 0 and 1"}
        
        # Check if wood exists in database
        if wood_type not in self.wood_database:
            return {
                "wood_type": wood_type,
                "confidence": f"{confidence*100:.1f}%",
                "condition": condition.title(),
                "message": "Wood type not in database. Consider adding it for personalized suggestions.",
                "general_advice": self._get_general_advice(condition)
            }
        
        # Handle bad condition wood
        if condition == "bad":
            return {
                "wood_type": wood_type,
                "confidence": f"{confidence*100:.1f}%", 
                "condition": condition.title(),
                "recommendation": "❌ NOT RECOMMENDED for furniture projects",
                "alternatives": [
                    "Use for practice cuts or template making",
                    "Consider as firewood if untreated",
                    "Compost if no chemicals were used"
                ]
            }
        
        wood_props = self.wood_database[wood_type]
        all_projects = []
        
        # Collect all projects
        for category, projects in self.furniture_projects.items():
            for project in projects:
                if skill_level is None or project.difficulty == skill_level:
                    suitability = self._calculate_suitability_score(wood_type, project, condition)
                    if suitability > 0.3:  # Only include reasonably suitable projects
                        all_projects.append((project, suitability, category))
        
        # Sort by suitability score
        all_projects.sort(key=lambda x: x[1], reverse=True)
        
        # Prepare response
        response = {
            "wood_type": wood_type,
            "confidence": f"{confidence*100:.1f}%",
            "condition": condition.title(),
            "wood_properties": {
                "hardness": wood_props.hardness.title(),
                "durability": wood_props.durability.replace("_", " ").title(),
                "workability": wood_props.workability.title(), 
                "finish_quality": wood_props.finish_quality.title(),
                "moisture_resistance": wood_props.moisture_resistance.title(),
                "price_category": wood_props.price_category.replace("_", " ").title()
            },
            "top_recommendations": [],
            "suitable_projects": [],
            "tips": self._get_wood_specific_tips(wood_type, condition)
        }
        
        # Add top 3 recommendations with detailed info
        for project, score, category in all_projects[:3]:
            response["top_recommendations"].append({
                "project": project.name,
                "category": category.replace("_", " ").title(),
                "difficulty": project.difficulty.value.title(),
                "suitability_score": f"{score*100:.0f}%",
                "cost_range": project.typical_cost_range,
                "description": project.description
            })
        
        # Add other suitable projects (next 7)
        for project, score, category in all_projects[3:10]:
            response["suitable_projects"].append({
                "project": project.name,
                "category": category.replace("_", " ").title(),
                "suitability": f"{score*100:.0f}%"
            })
        
        return response

    def _get_wood_specific_tips(self, wood_type: str, condition: str) -> List[str]:
        """Get wood-specific tips based on properties"""
        if wood_type not in self.wood_database:
            return []
            
        wood_props = self.wood_database[wood_type]
        tips = []
        
        if wood_props.hardness == "hard":
            tips.append("🔨 Use sharp tools - hard woods can dull blades quickly")
            tips.append("⚡ Pre-drill for screws to prevent splitting")
        elif wood_props.hardness == "soft":
            tips.append("🪚 Soft wood cuts easily but dents easily too")
            tips.append("🛡️ Consider pre-finishing to protect surface")
            
        if wood_props.moisture_resistance == "low":
            tips.append("💧 Apply water-resistant finish if using in humid areas")
        elif wood_props.moisture_resistance == "high":
            tips.append("🌧️ Excellent for outdoor projects and kitchens")
            
        if wood_props.workability == "difficult":
            tips.append("⚙️ Consider professional help for complex joinery")
        elif wood_props.workability == "easy":
            tips.append("✨ Great choice for beginners")
            
        if condition in ["fair", "poor"]:
            tips.append("🔍 Sand thoroughly to improve surface quality")
            tips.append("🎨 Consider painted finish to hide imperfections")
            
        return tips

    def _get_general_advice(self, condition: str) -> List[str]:
        """General advice for unknown wood types"""
        advice = {
            "excellent": ["Perfect for any furniture project", "Showcase the natural grain"],
            "good": ["Suitable for most furniture projects", "Light sanding may improve finish"],
            "fair": ["Good for painted projects", "Sand well before finishing"],
            "poor": ["Consider for practice projects only", "May need significant preparation"],
            "bad": ["Not recommended for furniture", "Consider alternative uses"]
        }
        return advice.get(condition, ["Assess wood quality before use"])

# Example usage and testing
def main():
    system = ImprovedWoodSuggestionSystem()
    
    # Test with different scenarios
    test_cases = [
        ("Mahogany", "excellent", 0.95),
        ("Pine", "fair", 0.78),
        ("Oak", "good", 0.92),
        ("Unknown_Wood", "good", 0.85),
        ("Acacia", "bad", 0.90)
    ]
    
    print("🪵 Wood Furniture Suggestion System - Test Results\n" + "="*60)
    
    for wood, condition, confidence in test_cases:
        print(f"\n🔍 Testing: {wood} | Condition: {condition} | Confidence: {confidence*100:.1f}%")
        print("-" * 50)
        
        result = system.get_comprehensive_suggestions(wood, condition, confidence)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            continue
            
        print(f"Wood: {result['wood_type']} ({result['confidence']})")
        print(f"Condition: {result['condition']}")
        
        if "recommendation" in result:
            print(f"Recommendation: {result['recommendation']}")
        elif "top_recommendations" in result:
            print("\n🏆 Top Recommendations:")
            for i, rec in enumerate(result['top_recommendations'], 1):
                print(f"  {i}. {rec['project']} ({rec['suitability_score']} match)")
                print(f"     • {rec['description']}")
                print(f"     • Cost: {rec['cost_range']} | Difficulty: {rec['difficulty']}")
            
            if result.get('tips'):
                print(f"\n💡 Tips:")
                for tip in result['tips']:
                    print(f"  • {tip}")
        
        print()

if __name__ == "__main__":
    main()