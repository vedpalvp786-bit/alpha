import os
from flask import Flask, render_template, request, send_file, after_this_request

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
    # Create a unique filename to prevent browser cache issues
    output_filename = f"temp_{name_eng}.mhtml"
    output_path = os.path.join(script_dir, output_filename)

    if not os.path.exists(source_path):
        return "Error: sample.txt not found."

    try:
        # Step 1: Read and replace in a way that handles large strings
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace("##NAMEHI##", name_hi)
        content = content.replace("##NAMEENG##", name_eng)

        # Step 2: Write to disk first (Safer for large files than memory)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Step 3: Delete the file from server AFTER the user downloads it
        @after_this_request
        def remove_file(response):
            try:
                os.remove(output_path)
            except Exception:
                pass
            return response

        # Step 4: Send the file with a specific timeout-friendly method
        return send_file(
            output_path,
            mimetype='application/x-mimearchive',
            as_attachment=True,
            download_name=f"{name_eng}.mhtml"
        )

    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
