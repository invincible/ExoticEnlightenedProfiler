from flask import Flask, render_template, request
from compare_files import compare_texts

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    result_html = None
    file1_content = ""
    file2_content = ""
    if request.method == 'POST':
        file1_content = request.form['file1_content']
        file2_content = request.form['file2_content']
        result_html = compare_texts(file1_content, file2_content)
    
    return render_template('upload.html', result_html=result_html, 
                           file1_content=file1_content, file2_content=file2_content)

if __name__ == '__main__':
    app.run(debug=True)