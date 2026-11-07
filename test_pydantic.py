from pydantic import ValidationError

from models import Brief

good = '{"summary": "Coffee began in Ethiopia.", "key_points": ["Ethiopia", "Yemen"], "sources": ["https://en.wikipedia.org/wiki/Coffee"]}'
bad = '{"summary": "Coffee began in Ethiopia.", "key_points": "not a list"}'

brief = Brief.model_validate_json(good)
print(brief)
print(brief.summary)
print(brief.key_points[0])

try:
    Brief.model_validate_json(bad)
except ValidationError as e:
    print(e)
