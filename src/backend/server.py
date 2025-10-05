from flask import Flask, jsonify, request
import json
from pathlib import Path
import os
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/data")
def get_data():
    # Resolve processed_data.json relative to this backend module so the
    # server works regardless of current working directory.
    base_dir = Path(os.path.dirname(__file__))
    file_path = base_dir.joinpath("processed_data.json")

    if not file_path.exists():
        return jsonify({"error": f"{file_path} not found"}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "processed_data.json is malformed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(data)



def read_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def atomic_write(path, data):
    # Write to a temp file and atomically replace the target
    dirpath = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=dirpath)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass


@app.route('/summarize')
def summarize_on_demand():
    """Summarize a single URL on demand and cache the result in processed_data.json.

    Query params:
      url=full_url

    Behavior:
      - If URL already in processed_data.json, return it.
      - Else, find scraped content in data.json, call summarizer, append to processed_data.json and return.
    """
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Missing url parameter'}), 400

    base_dir = Path(os.path.dirname(__file__))
    data_path = base_dir.joinpath('data.json')
    proc_path = base_dir.joinpath('processed_data.json')

    # load processed data and check cache
    processed = read_json(proc_path) or []
    for item in processed:
        try:
            if isinstance(item, dict) and item.get('url') == url:
                return jsonify(item)
        except Exception:
            continue

    # load scraped data
    scraped = read_json(data_path) or []
    found = None
    for rec in scraped:
        if isinstance(rec, dict) and rec.get('url') == url:
            found = rec
            break

    if not found:
        return jsonify({'error': 'URL not found in scraped data.json'}), 404

    # Lazy import summarizer to avoid import-time API key errors
    try:
        from geminiSummarizer import summarize_text
    except Exception as e:
        return jsonify({'error': f'Summarizer not available: {e}'}), 503

    text = found.get('content', '')
    try:
        summary = summarize_text(text)
    except Exception as e:
        # if summarization fails, return error but do not crash
        return jsonify({'error': f'Gemini summarization failed: {e}'}), 502

    # Normalize summary
    if isinstance(summary, dict):
        out = {
            'id': len(processed) + 1,
            'url': url,
            'title': summary.get('title') or found.get('title'),
            'author': summary.get('author') or found.get('author'),
            'summary': summary.get('summary') or '',
            'sections': summary.get('sections') or {},
        }
    else:
        out = {
            'id': len(processed) + 1,
            'url': url,
            'title': found.get('title'),
            'author': found.get('author'),
            'summary': str(summary),
            'sections': {},
        }

    # append and save atomically
    processed.append(out)
    try:
        atomic_write(str(proc_path), processed)
    except Exception as e:
        return jsonify({'error': f'Failed to write processed file: {e}'}), 500

    return jsonify(out)


@app.route('/kg')
def get_for_kg():
    """Return processed data to be used by an external knowledge-graph generator.

    The KG generator can filter and transform this JSON as needed.
    """
    base_dir = Path(os.path.dirname(__file__))
    proc_path = base_dir.joinpath('processed_data.json')
    processed = read_json(proc_path)
    if processed is None:
        return jsonify({'error': 'processed_data.json not found or malformed'}), 404
    # Optionally we could return a lighter-weight projection. For now return full data.
    return jsonify(processed)


@app.route('/process', methods=['POST'])
def process_all():
    """Do one-time bulk processing of scraped data into structured format.
    
    This processes the content in data.json and saves structured results
    to processed_data.json WITHOUT calling the Gemini API. It extracts:
    - titles
    - authors
    - sections
    - other metadata
    
    This is safe to run multiple times - it will overwrite processed_data.json
    with fresh structured data from data.json.
    """
    try:
        from data_processor import enrich_data
        enrich_data()  # uses default paths data.json -> processed_data.json
        return jsonify({'message': 'Processing complete. Check processed_data.json'})
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route("/")
def home():
    return {"message": "Backend API is running 🚀"}


if __name__ == "__main__":
    # Use 0.0.0.0 when you want to access from other machines, keep 127.0.0.1 for local dev
    app.run(debug=True, port=5000)
