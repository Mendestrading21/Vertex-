# LOT 249 — Chiffrage outillé É1+É2 de la purge de terminal.py (AUCUNE purge).
# Mark-and-sweep sur l'AST : racines vivantes = fonctions routées (runtime)
# + code module-level exécutable + références externes (autres modules du dépôt).
# Tout nom top-level non atteignable depuis ces racines = candidat mort.
import ast, os, re, subprocess, sys

os.environ.setdefault('DEMO', '1')
os.environ.setdefault('NO_IBKR', '1')

SRC = open('terminal.py', encoding='utf-8').read()
LINES = SRC.split('\n')
TREE = ast.parse(SRC)

# --- 1. Définitions top-level : nom -> (node, span, noms référencés) ---------
defs = {}          # name -> dict(kind, lineno, end, refs)
def add_def(name, node, kind):
    refs = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
    d = defs.setdefault(name, {'kind': kind, 'spans': [], 'refs': set()})
    d['spans'].append((node.lineno, node.end_lineno))
    d['refs'] |= refs

module_level_refs = set()   # noms utilisés par le code exécutable module-level
decorated = set()           # fonctions décorées : le décorateur s'exécute à l'import
imported_names = set()
for node in TREE.body:
    if isinstance(node, ast.FunctionDef):
        add_def(node.name, node, 'func')
        if node.decorator_list:
            decorated.add(node.name)
            for d in node.decorator_list:
                module_level_refs |= {n.id for n in ast.walk(d) if isinstance(n, ast.Name)}
    elif isinstance(node, ast.Assign):
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        for nm in names:
            add_def(nm, node, 'const')
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        add_def(node.target.id, node, 'const')
    elif isinstance(node, (ast.Import, ast.ImportFrom)):
        for a in node.names:
            imported_names.add(a.asname or a.name.split('.')[0])
    else:
        module_level_refs |= {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}

# Un nom défini plusieurs fois (réassignation) garde l'union des refs/spans.

# --- 2. Racines vivantes -----------------------------------------------------
# 2a. Fonctions routées (vérité runtime : url_map réel)
sys.path.insert(0, '.')
import terminal  # DEMO, pas de START_ON_IMPORT -> pas de serveur
routed = set()
for rule in terminal.app.url_map.iter_rules():
    fn = terminal.app.view_functions.get(rule.endpoint)
    if fn is not None and getattr(fn, '__module__', '') == 'terminal':
        routed.add(fn.__name__)

# 2b. Références externes : autres fichiers du dépôt (hors tests) qui importent terminal
ext_refs = set()
out = subprocess.run(['grep', '-rn', '--include=*.py', '-E',
                      r'from terminal import|import terminal', '.',
                      '--exclude-dir=tests', '--exclude-dir=.git'],
                     capture_output=True, text=True).stdout
for line in out.splitlines():
    path = line.split(':', 1)[0]
    if path.endswith('terminal.py'):
        continue
    body = open(path, encoding='utf-8').read()
    m = re.findall(r'from terminal import ([^\n]+)', body)
    for grp in m:
        for nm in re.split(r'[,\s()]+', grp):
            if nm and nm != 'import':
                ext_refs.add(nm)
    for nm in re.findall(r'\bterminal\.(\w+)', body):
        ext_refs.add(nm)

roots = (routed | decorated | (module_level_refs & set(defs)) | (ext_refs & set(defs)))

# --- 3. Marquage (closure) ---------------------------------------------------
alive = set()
stack = [r for r in roots if r in defs]
while stack:
    nm = stack.pop()
    if nm in alive:
        continue
    alive.add(nm)
    for ref in defs[nm]['refs']:
        if ref in defs and ref not in alive:
            stack.append(ref)

dead = set(defs) - alive

def span_stats(names):
    ls = set()
    by = 0
    for nm in names:
        for a, b in defs[nm]['spans']:
            for i in range(a, b + 1):
                if i not in ls:
                    ls.add(i)
                    by += len(LINES[i - 1].encode()) + 1
    return len(ls), by

total_lines = len(LINES)
total_bytes = len(SRC.encode())
dead_funcs = sorted(n for n in dead if defs[n]['kind'] == 'func')
dead_consts = sorted(n for n in dead if defs[n]['kind'] == 'const')
dl, db = span_stats(dead)
fl, fb = span_stats(dead_funcs)
cl, cb = span_stats(dead_consts)

print(f'terminal.py : {total_lines} lignes / {total_bytes} octets')
print(f'defs top-level : {len(defs)} (funcs+consts) | racines vivantes : {len(roots & set(defs))} '
      f'(routées={len(routed)}, décorées={len(decorated)}, module-level={len(module_level_refs & set(defs))}, '
      f'externes={sorted(ext_refs & set(defs))})')
print(f'VIVANTS : {len(alive)} | MORTS : {len(dead)} '
      f'({len(dead_funcs)} fonctions, {len(dead_consts)} constantes)')
print(f'MORT total : {dl} lignes ({dl/total_lines:.1%}) / {db} octets ({db/total_bytes:.1%})')
print(f'  - fonctions : {fl} lignes / {fb} octets')
print(f'  - constantes : {cl} lignes / {cb} octets')
print()
print('== Constantes mortes (triées par taille) ==')
sized = sorted(((sum(b - a + 1 for a, b in defs[n]['spans']), n) for n in dead_consts), reverse=True)
for sz, n in sized[:40]:
    print(f'  {sz:6d} l.  {n}')
print()
print('== Fonctions mortes ==')
sizedf = sorted(((sum(b - a + 1 for a, b in defs[n]['spans']), n) for n in dead_funcs), reverse=True)
for sz, n in sizedf:
    print(f'  {sz:6d} l.  {n}')
print()
# Croisement avec le dossier 248 : PAGE_* mortes vs vivantes
page_dead = [n for n in dead_consts if n.startswith('PAGE_')]
page_alive = [n for n in alive if n.startswith('PAGE_') and defs.get(n, {}).get('kind') == 'const']
print(f'PAGE_* mortes : {len(page_dead)} | PAGE_* vivantes : {sorted(page_alive)}')

# --- 5. Borne conservatrice : références par CHAÎNE dans le code module-level -
# Les boucles d'injection font `globals()[_pg]` sur des noms passés en chaînes
# ('PAGE_WATCHLIST', ...) : invisibles à l'analyse par noms. On les compte
# vivantes ici → borne BASSE certaine de la purge.
string_refs = set()
for node in TREE.body:
    if isinstance(node, (ast.FunctionDef, ast.Import, ast.ImportFrom)):
        continue
    for s in ast.walk(node):
        if isinstance(s, ast.Constant) and isinstance(s.value, str) and s.value in defs:
            string_refs.add(s.value)
alive2 = set()
stack = [r for r in (roots | string_refs) if r in defs]
while stack:
    nm = stack.pop()
    if nm in alive2:
        continue
    alive2.add(nm)
    for ref in defs[nm]['refs']:
        if ref in defs and ref not in alive2:
            stack.append(ref)
dead2 = set(defs) - alive2
d2l, d2b = span_stats(dead2)
print()
print(f'Réfs par CHAÎNE (globals()[...]) trouvées module-level : {sorted(string_refs)}')
print(f'BORNE BASSE (chaînes comptées vivantes) : {len(dead2)} défs mortes, '
      f'{d2l} lignes ({d2l/total_lines:.1%}) / {d2b} octets ({d2b/total_bytes:.1%})')
print(f'BORNE HAUTE (boucles d\'injection retirées avec) : {len(dead)} défs, '
      f'{dl} lignes ({dl/total_lines:.1%}) / {db} octets ({db/total_bytes:.1%})')
rescued = sorted(dead - dead2)
print(f'Défs sauvées uniquement par une réf-chaîne : {rescued}')
