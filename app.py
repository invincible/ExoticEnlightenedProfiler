from flask import Flask, render_template, request
from compare_files import compare_texts
import pandas as pd
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    result_html = None
    file1_content = ""
    file2_content = ""
    if request.method == 'POST':
        if 'file1' in request.files and 'file2' in request.files:
            file1 = request.files['file1']
            file2 = request.files['file2']
            
            if file1 and file2:
                file1_ext = file1.filename.split('.')[-1]
                file2_ext = file2.filename.split('.')[-1]
                
                if file1_ext in ['xls', 'xlsx'] and file2_ext in ['xls', 'xlsx']:
                    df1 = pd.read_excel(io.BytesIO(file1.read()))
                    df2 = pd.read_excel(io.BytesIO(file2.read()))
                    
                    # Align DataFrames by columns and index
                    df1, df2 = df1.align(df2, join='outer', axis=1, fill_value=None)
                    df1, df2 = df1.align(df2, join='outer', axis=0, fill_value=None)
                    
                    # Create a new DataFrame to store the comparison results
                    comparison_df = df2.copy()
                    changes = df1.compare(df2)
                    
                    for index, row in changes.iterrows():
                        for col in row.index.levels[0]:
                            old_value = row[(col, 'self')]
                            new_value = row[(col, 'other')]
                            if pd.notna(old_value) and pd.notna(new_value):
                                comparison_df.at[index, col] = f"{old_value} -> {new_value}"
                                comparison_df.at[index, col] = f'<span class="highlight">{comparison_df.at[index, col]}</span>'
                    
                    # Replace NaN and NaT with empty strings
                    comparison_df = comparison_df.fillna('').replace({pd.NaT: ''})
                    
                    result_html = comparison_df.to_html(escape=False)
                else:
                    file1_content = file1.read().decode('utf-8')
                    file2_content = file2.read().decode('utf-8')
                    result_html = compare_texts(file1_content, file2_content)
    
    return render_template('upload.html', result_html=result_html, 
                           file1_content=file1_content, file2_content=file2_content)

if __name__ == '__main__':
    app.run(debug=True)