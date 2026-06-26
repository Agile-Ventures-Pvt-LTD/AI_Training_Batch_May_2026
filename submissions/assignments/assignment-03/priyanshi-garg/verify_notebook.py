import json
from pathlib import Path

nb_path = Path('Hypothetical_question_assignment/hypothetical.ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))
for i, cell in enumerate(nb['cells'], start=1):
    if cell.get('cell_type') == 'code':
        src = ''.join(cell.get('source', []))
        if 'batch_questions' in src or 'question_docs' in src or 'add_documents' in src:
            print('\n=== CELL', i, '===')
            print(src)
