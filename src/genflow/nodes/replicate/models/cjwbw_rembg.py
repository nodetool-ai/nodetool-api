schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Response'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Request'}}}}}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'default': '', 'x-order': 0, 'description': 'Input image'}}}, 'Output': {'type': 'string', 'title': 'Output', 'format': 'uri'}, 'Status': {'enum': ['processing', 'succeeded', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'Request': {'type': 'object', 'title': 'Request', 'properties': {'input': {'$ref': '#/components/schemas/Input'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}}, 'description': 'The request body for a prediction'}, 'Response': {'type': 'object', 'title': 'Response', 'required': ['status'], 'properties': {'error': {'type': 'string', 'title': 'Error'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}}, 'description': 'The response body for a prediction'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'cjwbw/rembg'
model_version = 'fb8af171cfa1616ddcf1242c093f9c46bcada5ad4cf6f2fbe8b81b330ec5c003'
model_info = {'hardware': 'Nvidia A40 GPU'}
