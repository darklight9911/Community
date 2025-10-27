# Placeholder for schema validators.
# In a full implementation, you could use Marshmallow or Pydantic.


def validate_non_empty(value: str, field: str):
    if not value or not str(value).strip():
        raise ValueError(f"{field} is required")
