import json

from requests import Response

from chargebeecli.config.Configuration import Configuration
from chargebeecli.constants.constants import Formats
from chargebeecli.export.Exporter import Exporter
from chargebeecli.formater.response_formatter import ResponseFormatter
from chargebeecli.printer.printer import Printer, custom_print
from chargebeecli.processors.processor import Processor
from chargebeecli.processors.themes.available_themes import available_themes
from chargebeecli.validator.validator import Validator


class Theme(Processor, Validator, ResponseFormatter, Exporter, Printer):

    def __init__(self, export_format, export_path, file_name, response_format, _operation, _input_columns):
        self.headers = self.get_api_header()
        self.export_format = export_format
        self.export_path = export_path
        self.file_name = file_name
        self.tables = None
        self.response_format = response_format
        self.operation = _operation
        self.input_columns = _input_columns

    def validate_param(self):
        self.headers = super().validate_param(self.input_columns, self.headers)
        return self

    def get_api_header(self):
        return ['name', 'theme']

    def format(self):
        if self.to_be_formatted():
            self.tables = super(Theme, self).format(self.response, self.response_format, self.operation,
                                                    self.headers, 'theme', 'list')
        return self

    def process(self, ctx, operation, payload, resource_id):
        return super(Theme, self).process(ctx, operation, payload, resource_id)

    def get(self, ctx, payload, resource_id):
        response = Response()
        response.status_code = 200
        if resource_id is None:
            __active_profile = Configuration.Instance().fetch_section('active_profile', 'primary')
        else:
            __active_profile = resource_id
            if __active_profile not in Configuration.Instance().fetch_available_sections():
                exit()

        if __active_profile is None:
            return response
        res = {"theme": {"name": __active_profile,
                         "api_key": Configuration.Instance().fetch_section(__active_profile, "api_key"),
                         "account": Configuration.Instance().fetch_section(__active_profile, "account")}}
        response._content = json.dumps(res).encode('utf-8')
        return response

    def list(self, ctx):

        response = Response()
        response.status_code = 200

        res = []
        for __theme in available_themes:

            t1 = {"theme": {"name": __theme['name'], 'theme': 'sdfsad'}}
            res.append(t1)
        t = {"list": res}

        response._content = json.dumps(t).encode('utf-8')
        return response

    def delete(self, ctx, payload, resource_id):
        response = Response()
        response.status_code = 200
        response._content = json.dumps({'theme': {'name': resource_id, 'message': 'deleted'}}).encode('utf-8')
        Configuration.Instance().delete_section_or_profile(resource_id)
        return response

    def table_to_be_printed(self):
        return self.to_be_formatted()

    def to_be_formatted(self):
        return self.response_format.lower() == Formats.TABLE.value