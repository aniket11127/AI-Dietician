from flask import Flask, request, jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
import bcrypt
import os
import logging
from functools import wraps

app = Flask(__name__)
CORS(app)
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')  # Should be set in environment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_user_data(data):
    """Validate user input data"""
    errors = []
    
    # Required fields
    required_fields = ['age', 'weight', 'height', 'gender', 'activity_level', 
                      'goal', 'dietary_preferences', 'allergies']
    
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # Value validation
    if 'age' in data:
        try:
            age = int(data['age'])
            if not (0 < age < 120):
                errors.append("Age must be between 1 and 120")
        except ValueError:
            errors.append("Age must be a number")
    
    if 'weight' in data:
        try:
            weight = float(data['weight'])
            if not (20 < weight < 500):
                errors.append("Weight must be between 20 and 500 kg")
        except ValueError:
            errors.append("Weight must be a number")
    
    if 'height' in data:
        try:
            height = float(data['height'])
            if not (50 < height < 300):
                errors.append("Height must be between 50 and 300 cm")
        except ValueError:
            errors.append("Height must be a number")
    
    if 'gender' in data and data['gender'] not in ['male', 'female']:
        errors.append("Gender must be 'male' or 'female'")
    
    if 'activity_level' in data and data['activity_level'] not in ['sedentary', 'light', 'moderate', 'active', 'very_active']:
        errors.append("Invalid activity level")
    
    if 'goal' in data and data['goal'] not in ['weight_loss', 'maintain', 'weight_gain']:
        errors.append("Invalid goal")
    
    return errors

class DietPlanner:
    def calculate_bmr(self, weight, height, age, gender):
        """Calculate Basal Metabolic Rate"""
        try:
            # Convert inputs to float/int
            weight = float(weight)
            height = float(height)
            age = int(age)
            
            # Validate inputs
            if not (20 <= weight <= 500):
                raise ValueError("Weight must be between 20 and 500 kg")
            if not (50 <= height <= 300):
                raise ValueError("Height must be between 50 and 300 cm")
            if not (0 < age <= 120):
                raise ValueError("Age must be between 1 and 120 years")
            if gender.lower() not in ['male', 'female']:
                raise ValueError("Gender must be 'male' or 'female'")

            # Calculate BMR
            if gender.lower() == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            return round(bmr, 2)
        except Exception as e:
            logger.error(f"Error calculating BMR: {str(e)}")
            raise ValueError(f"Error calculating BMR: {str(e)}")

    def generate_meal_plan(self, user_data):
        """Generate a personalized meal plan"""
        try:
            # Validate required fields
            required_fields = ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"Missing required field: {field}")

            # Calculate BMR
            bmr = self.calculate_bmr(
                user_data['weight'],
                user_data['height'],
                user_data['age'],
                user_data['gender']
            )
            
            # Define activity multipliers
            activity_multipliers = {
                'sedentary': 1.2,
                'light': 1.375,
                'moderate': 1.55,
                'active': 1.725,
                'very_active': 1.9
            }
            
            # Calculate daily calories
            activity_level = user_data['activity_level'].lower()
            if activity_level not in activity_multipliers:
                raise ValueError(f"Invalid activity level. Must be one of: {', '.join(activity_multipliers.keys())}")
            
            daily_calories = bmr * activity_multipliers[activity_level]
            
            # Adjust calories based on goal
            goal_multipliers = {
                'weight_loss': 0.85,
                'maintain': 1.0,
                'weight_gain': 1.15
            }
            
            goal = user_data['goal'].lower()
            if goal not in goal_multipliers:
                raise ValueError(f"Invalid goal. Must be one of: {', '.join(goal_multipliers.keys())}")
            
            daily_calories *= goal_multipliers[goal]
            
            # Get meal plan
            plan = self.get_meals_for_calories(
                daily_calories,
                user_data.get('dietary_preferences', []),
                user_data.get('allergies', [])
            )
            
            return plan
        except Exception as e:
            logger.error(f"Error generating meal plan: {str(e)}")
            raise ValueError(str(e))

    def get_meals_for_calories(self, calories, preferences, allergies):
        """Generate meal recommendations based on calories and preferences"""
        try:
            # Sample meal database
            meal_database = {
                'breakfast': [
                    'Oatmeal with banana and honey',
                    'Greek yogurt with berries and granola',
                    'Whole grain toast with avocado and eggs',
                    'Protein smoothie with spinach and fruits',
                    'Scrambled eggs with whole grain toast',
                    'Overnight oats with almond milk and chia seeds'
                ],
                'lunch': [
                    'Grilled chicken salad with olive oil dressing',
                    'Quinoa bowl with roasted vegetables',
                    'Turkey and avocado sandwich on whole grain bread',
                    'Lentil soup with whole grain crackers',
                    'Mixed green salad with tuna',
                    'Black bean and sweet potato bowl'
                ],
                'dinner': [
                    'Baked salmon with roasted vegetables',
                    'Lean beef stir-fry with brown rice',
                    'Chickpea curry with brown rice',
                    'Grilled chicken breast with sweet potato',
                    'Tofu and vegetable stir-fry',
                    'Baked cod with quinoa and vegetables'
                ]
            }

            # Calculate macro distribution
            protein_ratio = 0.3
            carbs_ratio = 0.4
            fat_ratio = 0.3

            macros = {
                'protein': round((calories * protein_ratio) / 4, 1),  # 4 calories per gram of protein
                'carbs': round((calories * carbs_ratio) / 4, 1),    # 4 calories per gram of carbs
                'fat': round((calories * fat_ratio) / 9, 1)         # 9 calories per gram of fat
            }

            # Filter meals based on preferences and allergies
            def filter_meals(meals):
                filtered = meals.copy()
                # Filter by allergies
                for allergy in allergies:
                    if allergy:
                        filtered = [meal for meal in filtered if allergy.lower() not in meal.lower()]
                # Filter by preferences
                if preferences:
                    filtered = [meal for meal in filtered if any(pref.lower() in meal.lower() for pref in preferences)]
                return filtered or meals  # Return original meals if all filtered out

            breakfast = filter_meals(meal_database['breakfast'])
            lunch = filter_meals(meal_database['lunch'])
            dinner = filter_meals(meal_database['dinner'])

            # Select meals
            import random
            selected_meals = {
                'breakfast': random.sample(breakfast, min(3, len(breakfast))),
                'lunch': random.sample(lunch, min(3, len(lunch))),
                'dinner': random.sample(dinner, min(3, len(dinner)))
            }

            return {
                'daily_calories': round(calories),
                'macros': macros,
                'meals': selected_meals
            }

        except Exception as e:
            logger.error(f"Error getting meals: {str(e)}")
            raise ValueError(f"Error getting meal recommendations: {str(e)}")

diet_planner = DietPlanner()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
            
        user_message = data.get('message', '').strip()
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Simple response without NLP
        response = "I understand you're asking about: " + user_message
        return jsonify({
            'response': response,
            'sentiment': 'neutral'
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/diet-plan', methods=['POST'])
def create_diet_plan():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        # Log incoming request
        logger.info(f"Received diet plan request: {data}")
            
        # Validate input data
        validation_errors = validate_user_data(data)
        if validation_errors:
            logger.warning(f"Validation errors: {validation_errors}")
            return jsonify({'error': 'Validation failed', 'details': validation_errors}), 400
            
        # Generate plan
        try:
            plan = diet_planner.generate_meal_plan(data)
            logger.info("Successfully generated diet plan")
            return jsonify(plan)
        except ValueError as e:
            logger.error(f"Error in diet plan generation: {str(e)}")
            return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error in create_diet_plan: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
