from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import PyPDF2
import easyocr
import speech_recognition as sr
import networkx as nx
import matplotlib.pyplot as plt
import requests
import google.generativeai as genai
import re  # Import the re module for regular expressions

# Flask app configuration
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ocr_reader = easyocr.Reader(['en'])  # Initialize EasyOCR

# Ensure the API key is stored in an environment variable
os.environ["GOOGLE_API_KEY"] = "AIzaSyCHhYF4oQjodg7ypr3b6kmuHkHd96-5QMc"  # Replace with your key
API_KEY = os.getenv("GOOGLE_API_KEY")
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def structure_text(text):
    """Format extracted text into structured paragraphs or bullet points."""
    # Split text into paragraphs based on double newlines or sentence boundaries
    paragraphs = [p.strip() for p in re.split(r'\n\n|\.\s+', text) if p.strip()]

    # Create bullet points from paragraphs
    bullet_points = ['• ' + paragraph for paragraph in paragraphs]

    return bullet_points

def extract_text_from_pdf(file_path):
    """Extract text from PDF files and format it into structured content."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''.join([page.extract_text() for page in reader.pages if page.extract_text()])
            sentences = re.split(r'(?<=[.!?])\s+', text)
            formatted_text = '<br>'.join([sentence.strip() for sentence in sentences if sentence.strip()])
        return structure_text(text)
    except Exception as e:
        return [f"Error reading PDF: {str(e)}"]

def extract_text_from_audio(file_path):
    """Extract text from audio files and format it into structured content."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return structure_text(text)
    except Exception as e:
        return [f"Error extracting text from audio: {str(e)}"]

def extract_text_from_image(file_path):
    """Extract text from images and format it into structured content."""
    try:
        results = ocr_reader.readtext(file_path)
        text = ' '.join([result[1] for result in results])
        return structure_text(text)
    except Exception as e:
        return [f"Error reading image: {str(e)}"]

def extract_keywords_from_text(text):
    """Extract keywords using the Gemini API."""
    try:
        # Start a chat session and send the input text
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"Extract key terms from the following text:\n{text}")

        # Split the response by lines to extract keywords
        keywords = response.text.split('\n\n')
        pattern = r"(?m)^\*\*\s*([\w\s]+)\s*\*\*:"  # Matches "**Heading:**" format
        side_headings = [match.strip() for match in re.findall(pattern, text)]

        # Select only the first 10 keywords
        main_keywords = [keyword.strip() for keyword in keywords[:10] if keyword.strip()]

        return side_headings if side_headings else ["No headings found."], main_keywords if main_keywords else ["No keywords found."]
    
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return ["Error with Gemini API"], []
    
    except Exception as e:
        return [f"Error with Gemini API: {str(e)}"], []

def generate_knowledge_graph(keywords):
    """Generate a tree-structured knowledge graph from keywords, limiting each node to two words."""
    G = nx.DiGraph()  # Use a directed graph for tree structure

    # Create a root node
    root_node = "Keywords"
    G.add_node(root_node)

    # Function to limit each keyword to two words
    def limit_to_two_words(keyword):
        return ' '.join(keyword.split()[:2])  # Take the first two words

    # Add keywords as children of the root node
    for keyword in keywords:
        limited_keyword = limit_to_two_words(keyword)
        G.add_node(limited_keyword)
        G.add_edge(root_node, limited_keyword)  # Connect each keyword to the root node

    pos = nx.spring_layout(G)  # Layout for a better visual representation
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, arrows=True)

    graph_path = os.path.join(app.config['UPLOAD_FOLDER'], 'knowledge_graph.png')
    plt.savefig(graph_path)
    plt.close()
    return 'knowledge_graph.png'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Determine file type and extract text
            if filename.endswith('.pdf'):
                extracted_text = extract_text_from_pdf(file_path)
            elif filename.endswith(('.mp3', '.wav')):
                extracted_text = extract_text_from_audio(file_path)
            elif filename.endswith(('.png', '.jpg', '.jpeg')):
                extracted_text = extract_text_from_image(file_path)
            else:
                return jsonify({"error": "Unsupported file type"}), 400

            # Extract keywords and generate knowledge graph
            side_headings, keywords = extract_keywords_from_text(' '.join(extracted_text))  # Join structured text for keywords
            graph_image = generate_knowledge_graph(keywords) if keywords else None

            return jsonify({
                'extracted_text': extracted_text,  # Will be a list of bullet points now
                'side_headings': side_headings,
                'keywords': keywords,
                'knowledge_graph': graph_image
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)