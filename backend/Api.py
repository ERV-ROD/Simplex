from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from Simplex import Simplex

app = Flask(__name__)

CORS(app)


@app.route('/api/data', methods=['GET'])
def get_data():
    """
    The function `get_data` returns a JSON object containing the message "Hello from the backend!".
    
    @return a JSON object containing the message "Hello from the backend!".
    """
    data = {'message': 'Hello from the backend!'}
    return jsonify(data)


@app.route('/post/data', methods=['POST'])
def post_data():
    """
    The function `post_data` receives JSON data, performs some calculations using the Simplex algorithm,
    and returns the result as a JSON response.
    
    @return a JSON response and an HTTP status code of 200.
    """
    data = request.get_json()
    json_data = data
    simplex = Simplex(json_data)
    simplex.start_simplex()
    resultado = simplex.getInfo()
    return jsonify(resultado), 200

@app.route('/download/csv', methods=['GET'])
def download_csv():
    """
    The function `download_csv` downloads a CSV file named 'tabla.csv' as an attachment.
    
    @return the file specified by the file_path variable as an attachment.
    """
    file_path = 'tabla.csv'
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


