# JSON Schema Notes

## Required Early Fields

These should be gathered first:
- `concept`
- `role`
- `name`
- `drive`

## Recommended Supporting Fields

- `fear`
- `edge`
- `flaw`
- `core_traits`
- `starter_gear`

## Derived Fields

Recompute these after any meaningful change:
- `derived.one_line_pitch`
- `derived.campaign_hook`
- `derived.notable_edge`

## Relationships

Keep relationships lightweight:

```json
[
  {
    "name": "Ferryman Edda",
    "type": "owes a favor",
    "status": "uneasy"
  }
]
```
