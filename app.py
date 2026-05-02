import os
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    name_hi = request.form.get('name_hi')
    name_eng = request.form.get('name_eng').strip().upper()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'sample.txt')
    output_filename = f"{name_eng}.mhtml"
    output_path = os.path.join(script_dir, output_filename)

    if not os.path.exists(source_path):
        return "<h1>Error: sample.txt not found in the script folder.</h1>"

    try:
        # Read and Replace
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace("##NAMEHI##", name_hi).replace("##NAMEENG##", name_eng)
        
        # Save temporary MHTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        # Send file to browser as a download
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"<h1>An error occurred:</h1><p>{e}</p>"

if __name__ == '__main__':
    app.run(debug=True)