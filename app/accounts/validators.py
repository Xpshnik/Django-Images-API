import jsonschema
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
    

class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError:
            raise ValidationError(
                '%(value)s failed JSON schema check', params={'value': value}
            )
