import os
import io
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    # Get inputs from the HTML form
    name_hi = request.form.get('name_hi', '')
    name_eng = request.form.get('name_eng', '').strip().upper()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'sample.txt')

    # 1. Verify template exists
    if not os.path.exists(source_path):
        return "Error: sample.txt not found on the server."

    try:
        # 2. Read template with UTF-8 encoding
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 3. Perform the replacement
        content = content.replace("##NAMEHI##", name_hi)
        content = content.replace("##NAMEENG##", name_eng)
        
        # 4. Convert to BytesIO (Memory Stream)
        # This prevents the "blank file" issue by ensuring data is fully processed 
        # before the download starts.
        mem_file = io.BytesIO()
        mem_file.write(content.encode('utf-8'))
        mem_file.seek(0)

        return send_file(
            mem_file,
            mimetype='application/x-mimearchive',
            as_attachment=True,
            download_name=f"{name_eng}.mhtml"
        )

    except Exception as e:
        return f"Process Error: {str(e)}"

if __name__ == '__main__':
    # Use environment variable for Port to ensure compatibility with Render/Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
