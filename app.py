from flask import Flask, request, jsonify, send_file, render_template
from serpapi import GoogleSearch
import csv

app = Flask(__name__)

API_KEY = "b6f38873e14d51bb7b6359c63ef713100c0b82f5430399db37cf77ace9d93850"

def search(query):
    params = {
        "q": query,
        "api_key": API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results["organic_results"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_route():
    query = request.args.get('query')
    results = search(query)
    simplified_results = [{"title": res["title"], "link": res["link"], "snippet": res["snippet"]} for res in results]
    return jsonify({"results": simplified_results})

@app.route('/download_csv')
def download_csv():
    query = request.args.get('query')
    results = search(query)
    simplified_results = [{"title": res["title"], "link": res["link"], "snippet": res["snippet"]} for res in results]
    
    csv_file = "search_results.csv"
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Link", "Snippet"])
        for result in simplified_results:
            writer.writerow([result["title"], result["link"], result["snippet"]])
    
    return send_file(csv_file, as_attachment=True, download_name=csv_file)

if __name__ == "__main__":
    app.run(debug=True)
