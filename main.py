import os
import json
from flask import Flask, render_template, url_for

app = Flask(__name__)

def load_munros():
    # This finds your data/munros.json
    json_path = os.path.join(app.root_path, 'data', 'munros.json')
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}

@app.route('/')
def index():
    munros = load_munros()
    return render_template('index.html', munros=munros)

@app.route('/munro/<m_id>')
def munro_detail(m_id):
    all_munros = load_munros()
    m_info = all_munros.get(m_id)
    
    if not m_info:
        return f"ID '{m_id}' not found in JSON", 404

    folder_path = os.path.join(app.root_path, 'static', 'images', 'munros', m_id)
    
    # Check if the folder even exists to Python
    folder_exists = os.path.exists(folder_path)
    
    # See what files are inside
    found_files = []
    if folder_exists:
        found_files = os.listdir(folder_path)

    # LOAD STORY
    story_content = "No story found."
    story_path = os.path.join(folder_path, 'story.txt')
    if os.path.exists(story_path):
        with open(story_path, 'r') as f:
            story_content = f.read()

    # FILTER IMAGES
    images = [f for f in found_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    images.sort()

    # If NO images are found, let's output a debug message to the screen
    if not images:
        return f"""
        <h1>Debug Mode</h1>
        <p><b>Folder Path:</b> {folder_path}</p>
        <p><b>Folder Exists:</b> {folder_exists}</p>
        <p><b>Files found in folder:</b> {found_files}</p>
        <p><b>Looking for ID:</b> {m_id}</p>
        <hr>
        <p>If 'Files found' is empty, your online IDE hasn't saved the upload yet.</p>
        <a href='/'>Go Back</a>
        """

    return render_template('munro_detail.html', m=m_info, m_id=m_id, story=story_content, images=images)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)