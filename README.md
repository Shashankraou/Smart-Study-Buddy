## St.Joseph Engineering College - Phoenix

Glen Elric Fernandes

Shashank Rao U

Sherol Chrissel Dsouza

## 3.1 Problem Statement: Knowledge Distiller App
Smart Study Buddy is a Knowledge Distiller App addresses the challenges students face in organizing and retrieving study materials. It allows users to upload notes in various formats—text, images, or audio—and automatically generates a personal knowledge graph. This graph visually connects key concepts, enhancing study efficiency and catering to individual learning styles. The app must parse different input types to extract meaningful information and construct an evolving knowledge graph that updates as new materials are added.

The expected solution involves an intuitive user interface that enables easy uploading of study materials, along with features for exploring and searching the graph. Bonus features could include collaboration tools for sharing knowledge graphs, adaptive learning suggestions based on identified knowledge gaps, integration with existing educational platforms, and innovative functionalities like automatic tagging, summarization, and cross-referencing across subjects. Overall, the app aims to empower students in their study practices and improve academic performance.


# Prerequisites
## Python: ## Ensure Python (3.6+) is installed. You can download it from here.
## pip: ## Python's package installer (comes bundled with Python).


# Step-by-Step Instructions
## 1. Clone the Project or Save the Files
Save the Python Flask app code in a file named app.py.
Save the HTML file inside a folder named templates as upload.html.
##  2. Create a Virtual Environment (Optional but Recommended)
```bash
Copy code
python -m venv venv
source venv/bin/activate  # On macOS/Linux
.\venv\Scripts\activate   # On Windows
```
## 3. Install Required Dependencies
Run the following command to install the necessary Python libraries:

bash
Copy code
```pip install flask flask-cors easyocr PyPDF2 SpeechRecognition matplotlib networkx google-generativeai werkzeug```
## 4. Set Up Google Generative AI API Key
Ensure you have a valid Google Generative AI API key.

Replace the placeholder AIzaSyCHhYF4... in your app.py with your actual API key.
Optionally, you can set the API key via the environment:
bash
Copy code
```export GOOGLE_API_KEY=your-api-key-here``` # On macOS/Linux
```set GOOGLE_API_KEY=your-api-key-here```     # On Windows
5. Create the Project Directory Structure
Make sure your project directory looks like this:

bash
Copy code 
```
/project-root
│
├── /uploads              # For storing uploaded files and generated knowledge graphs
│
├── /templates            # For HTML templates
│   └── upload.html
│
└── app.py                # Your Flask app code
```
6. Run the Flask Application
In your terminal, navigate to the project directory and run:

bash
Copy code
```python app.py ```
You should see output similar to:

csharp
Copy code
``` Running on http://127.0.0.1:5000/ ```
(Press CTRL+C to quit)
7. Open the Application in Your Browser
Open your browser and visit: http://127.0.0.1:5000/
You should see the Smart Study Buddy interface.




## References
- [Flask Documentation](https://flask.palletsprojects.com/)
- [EasyOCR Documentation](https://www.jaided.ai/easyocr/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [spaCy Documentation](https://spacy.io/)
- [React Documentation](https://reactjs.org/)

### Contributors

This project was developed by:
- [Glen Elric Fernandes](https://github.com/glen-elric-fernandes) - St. Joseph Engineering College
- [Shashank Rao U](https://github.com/Shashankraou) - St. Joseph Engineering College
- [Sherol Chrissel Dsouza](https://github.com/sheroldsouza) - St. Joseph Engineering College
