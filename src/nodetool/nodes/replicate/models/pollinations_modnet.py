schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'required': ['image'], 'properties': {'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 0, 'description': 'input image'}}}, 'Output': {'type': 'string', 'title': 'Output', 'format': 'uri'}, 'Status': {'enum': ['processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['logs', 'output', 'start', 'completed'], 'uniqueItems': True}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs'}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'pollinations/modnet'
model_version = 'da7d45f3b836795f945f221fc0b01a6d3ab7f5e163f13208948ad436001e2255'
model_info = {'hardware': 'Nvidia T4 GPU'}