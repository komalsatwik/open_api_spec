import json
import yaml
from openapi_spec_validator import validate_spec


class BaseParser:
    def parse(self, content: str) -> dict:
        pass


class JsonParser(BaseParser):
    def parse(self, content: str) -> dict:
        return json.loads(content)


class YamlParser(BaseParser):
    def parse(self, content: str) -> dict:
        return yaml.safe_load(content)


class ParserFactory:
    @staticmethod
    def get_parser(filename: str) -> BaseParser:
        ext = filename.split(".")[-1].lower()

        if ext == "json":
            return JsonParser()

        elif ext == "yaml":
            return YamlParser()

        else:
            raise ValueError(f"Unsupported file type: {ext}")


class SpecValidator:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def validate(self, content: str) -> bool:
        try:
            spec = self.parser.parse(content)
            validate_spec(spec)
            return True
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            raise ValueError("Invalid OpenAPI Spec")
        except Exception as e:
            raise Exception(f"Invalid OpenAPI Spec: {e}")

