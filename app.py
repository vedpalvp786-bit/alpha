import os
from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    name_hi = request.form.get('name_hi', '')
    name_eng = request.form.get('name_eng', '').strip().upper()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(script_dir, 'sample.txt')

    if not os.path.exists(source_path):
        return "Error: sample.txt not found."

    def generate():
        # Open file as a stream to handle large sizes
        with open(source_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Replace tags line by line to save memory
                line = line.replace("##NAMEHI##", name_hi)
                line = line.replace("##NAMEENG##", name_eng)
                yield line.encode('utf-8')

    # We return a Streaming Response
    return Response(
        generate(),
        mimetype='application/x-mimearchive',
        headers={
            "Content-Disposition": f"attachment; filename={name_eng}.mhtml"
        }
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
