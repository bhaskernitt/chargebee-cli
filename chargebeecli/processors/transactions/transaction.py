from chargebeecli.client.actionsImpl import ActionsImpl
from chargebeecli.constants.constants import Formats
from chargebeecli.export.Exporter import Exporter
from chargebeecli.formater.response_formatter import ResponseFormatter
from chargebeecli.printer.printer import Printer
from chargebeecli.processors.processor import Processor
from chargebeecli.validator.validator import Validator

API_URI = '/api/v2/transactions'


class Transaction(Processor, Validator, ResponseFormatter, Exporter, Printer):
    __action_processor = ActionsImpl()

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
        return ["amount", "amount_capturable", "authorization_reason", "base_currency_code", "currency_code",
                "customer_id", "date", "deleted", "exchange_rate", "fraud_reason", "gateway", "gateway_account_id",
                "id", "id_at_gateway", "linked_payments", "masked_card_number", "object", "payment_method",
                "payment_source_id", "resource_version", "status", "type", "updated_at"]

    def process(self, ctx, operation, payload, resource_id):
        return super(Transaction, self).process(ctx, operation, payload, resource_id)

    def to_be_formatted(self):
        return self.response_format.lower() == Formats.TABLE.value

    def format(self):
        if self.to_be_formatted():
            self.tables = super(Transaction, self).format(self.response, self.response_format, self.operation,
                                                          self.headers, 'transaction', 'list')
        return self

    def get(self, ctx, payload, resource_id):
        return self.__action_processor.get(API_URI + '/' + resource_id)

    def list(self, ctx):
        return self.__action_processor.get(API_URI)

    def delete(self, ctx, payload, resource_id):
        return self.__action_processor.delete(API_URI + '/' + resource_id + '/' + 'delete')

    def table_to_be_printed(self):
        return self.to_be_formatted()
