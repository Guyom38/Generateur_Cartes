from flask import Flask, jsonify, send_from_directory, request, abort
import os, json, re
from pathlib import Path

app = Flask(__name__)
BASE_DIR  = Path(__file__).parent
CARDS_DIR = BASE_DIR / 'cards'
CARDS_DIR.mkdir(exist_ok=True)


def safe_name(name: str) -> str | None:
    """Valide et nettoie un nom de fichier JSON."""
    name = os.path.basename(name)
    if re.match(r'^[\w\-. ]+\.json$', name, re.UNICODE):
        return name
    return None


# ── Fichiers statiques ────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/<path:filename>')
def static_file(filename):
    return send_from_directory(BASE_DIR, filename)


# ── API cartes ────────────────────────────────────────────────────────────────

@app.route('/api/cards', methods=['GET'])
def list_cards():
    """Liste tous les fichiers .json dans /cards, triés par date décroissante."""
    files = [
        {'name': f.name, 'modified': f.stat().st_mtime}
        for f in CARDS_DIR.glob('*.json')
    ]
    files.sort(key=lambda x: x['modified'], reverse=True)
    return jsonify(files)


@app.route('/api/cards/<path:name>', methods=['GET'])
def get_card(name):
    name = safe_name(name)
    if not name:
        abort(400)
    path = CARDS_DIR / name
    if not path.exists():
        abort(404)
    return jsonify(json.loads(path.read_text('utf-8')))


@app.route('/api/cards/<path:name>', methods=['POST'])
def save_card(name):
    name = safe_name(name)
    if not name:
        abort(400)
    data = request.get_json(force=True)
    (CARDS_DIR / name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), 'utf-8'
    )
    return jsonify({'ok': True, 'name': name})


@app.route('/api/cards/<path:name>', methods=['DELETE'])
def delete_card(name):
    name = safe_name(name)
    if not name:
        abort(400)
    path = CARDS_DIR / name
    if path.exists():
        path.unlink()
    return jsonify({'ok': True})


# ── Lancement ─────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import webbrowser, threading
    url = 'http://localhost:5000'
    threading.Timer(0.9, lambda: webbrowser.open(url)).start()
    print(f'\n  ╔══════════════════════════════════╗')
    print(f'  ║  Générateur de Cartes            ║')
    print(f'  ║  {url}          ║')
    print(f'  ╚══════════════════════════════════╝')
    print(f'\n  Cartes sauvegardées dans : {CARDS_DIR}')
    print(f'  Ctrl+C pour arrêter\n')
    app.run(host='127.0.0.1', port=5000, debug=False)
