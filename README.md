# AI Dietician Bot

## Overview
An AI-powered dietician bot that creates personalized diet plans based on user metrics, preferences, and goals. The application uses modern web technologies and provides an intuitive interface for users to get customized meal recommendations.

## Features
- 🍽️ Personalized meal recommendations
- 📊 BMR and calorie calculations
- 🎯 Goal-based diet plans (weight loss, maintenance, gain)
- 🥗 Dietary preference support
- ⚠️ Allergy considerations
- 📱 Responsive design
- 💬 Interactive chat interface

## Tech Stack
- Backend: Python, Flask
- Frontend: HTML5, CSS3, JavaScript
- UI Framework: Bootstrap 5
- APIs: Flask-CORS

## Prerequisites
- Python 3.8 or higher
- Modern web browser
- Internet connection (for CDN resources)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd windsurf-project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Windows
set SECRET_KEY=your-secret-key
# Unix/MacOS
export SECRET_KEY=your-secret-key
```

## Running the Application

1. Start the backend server:
```bash
cd backend
python app.py
```
The server will start at `http://localhost:5000`

2. Open the frontend:
- Navigate to the `frontend` directory
- Open `index.html` in a web browser
- Or use a local server:
```bash
python -m http.server 8000
```
Then visit `http://localhost:8000`

## Usage

1. Fill in your details:
   - Age (1-120 years)
   - Weight (20-500 kg)
   - Height (50-300 cm)
   - Gender (male/female)
   - Activity Level (sedentary to very active)
   - Fitness Goal (weight loss, maintain, weight gain)
   - Dietary Preferences
   - Allergies

2. Submit the form to receive:
   - Daily calorie target
   - Macronutrient breakdown
   - Personalized meal suggestions
   - Nutritional information

## Directory Structure
```
windsurf-project/
├── backend/
│   └── app.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── images/
├── requirements.txt
└── README.md
```

## Security Considerations
- User data is validated both client and server-side
- CORS is properly configured
- Error handling is implemented
- Sensitive data is not stored
- Input sanitization is in place

## Known Limitations
- Limited meal database
- Basic chat functionality
- No user authentication yet
- No persistent storage

## Future Enhancements
1. User authentication and profiles
2. Database integration
3. Advanced meal planning
4. Progress tracking
5. Mobile app version
6. Integration with fitness trackers
7. Expanded meal database
8. Nutritional analysis
9. Recipe details and instructions
10. Shopping lists generation

## Troubleshooting
1. If the server won't start:
   - Check Python version
   - Verify all dependencies are installed
   - Ensure port 5000 is available

2. If meals don't display:
   - Check browser console for errors
   - Verify backend is running
   - Check network connectivity

## Contributing
Contributions are welcome! Please read our contributing guidelines and submit pull requests to our repository.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please open an issue in the repository or contact the development team.
