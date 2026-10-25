"""Build a portable, self-contained HTML app from the inspectable source files."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent
def main():
    template=(ROOT/'dist/index.template.html').read_text()
    values={
      'CSS':(ROOT/'dist/style.css').read_text(),
      'DATA':(ROOT/'dist/data.json').read_text(),
      'SQL':json.dumps((ROOT/'analysis/metrics.sql').read_text()),
      'PY':json.dumps((ROOT/'analysis/generate_data.py').read_text()),
      'ANALYTICS':(ROOT/'dist/analytics.js').read_text(),
      'APP':(ROOT/'dist/app.js').read_text(),
    }
    for key,value in values.items():template=template.replace('/*__'+key+'__*/',value)
    assert '/*__' not in template
    (ROOT/'dist/index.html').write_text(template)
    print(f'Built {ROOT / "dist/index.html"} ({len(template):,} characters)')
if __name__=='__main__': main()
