schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Response'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Request'}}}}}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'required': ['image'], 'properties': {'image': {'type': 'string', 'title': 'Image', 'format': 'uri', 'x-order': 0, 'description': 'Input image'}, 'scale': {'type': 'number', 'title': 'Scale', 'default': 4, 'maximum': 10, 'minimum': 0, 'x-order': 1, 'description': 'Factor to scale image by'}, 'face_enhance': {'type': 'boolean', 'title': 'Face Enhance', 'default': True, 'x-order': 2, 'description': 'Face enhance'}}}, 'Output': {'type': 'string', 'title': 'Output', 'format': 'uri'}, 'Status': {'enum': ['processing', 'succeeded', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'Request': {'type': 'object', 'title': 'Request', 'properties': {'input': {'$ref': '#/components/schemas/Input'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}}, 'description': 'The request body for a prediction'}, 'Response': {'type': 'object', 'title': 'Response', 'required': ['status'], 'properties': {'error': {'type': 'string', 'title': 'Error'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}}, 'description': 'The response body for a prediction'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'nightmareai/real-esrgan'
model_version = '42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b'
model_info = {'hardware': 'Nvidia T4 GPU'}
