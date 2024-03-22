schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'required': ['input_image'], 'properties': {'seed': {'type': 'integer', 'title': 'Seed', 'maximum': 2147483647, 'minimum': 0, 'x-order': 11, 'description': 'Seed. Leave blank to use a random number'}, 'prompt': {'type': 'string', 'title': 'Prompt', 'default': 'A photo of a person img', 'x-order': 4, 'description': "Prompt. Example: 'a photo of a man/woman img'. The phrase 'img' is the trigger word."}, 'num_steps': {'type': 'integer', 'title': 'Num Steps', 'default': 20, 'maximum': 100, 'minimum': 1, 'x-order': 7, 'description': 'Number of sample steps'}, 'style_name': {'allOf': [{'$ref': '#/components/schemas/style_name'}], 'default': 'Photographic (Default)', 'x-order': 5, 'description': "Style template. The style template will add a style-specific prompt and negative prompt to the user's prompt."}, 'input_image': {'type': 'string', 'title': 'Input Image', 'format': 'uri', 'x-order': 0, 'description': 'The input image, for example a photo of your face.'}, 'num_outputs': {'type': 'integer', 'title': 'Num Outputs', 'default': 1, 'maximum': 4, 'minimum': 1, 'x-order': 9, 'description': 'Number of output images'}, 'input_image2': {'type': 'string', 'title': 'Input Image2', 'format': 'uri', 'x-order': 1, 'description': 'Additional input image (optional)'}, 'input_image3': {'type': 'string', 'title': 'Input Image3', 'format': 'uri', 'x-order': 2, 'description': 'Additional input image (optional)'}, 'input_image4': {'type': 'string', 'title': 'Input Image4', 'format': 'uri', 'x-order': 3, 'description': 'Additional input image (optional)'}, 'guidance_scale': {'type': 'number', 'title': 'Guidance Scale', 'default': 5, 'maximum': 10, 'minimum': 1, 'x-order': 10, 'description': 'Guidance scale. A guidance scale of 1 corresponds to doing no classifier free guidance.'}, 'negative_prompt': {'type': 'string', 'title': 'Negative Prompt', 'default': 'nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry', 'x-order': 6, 'description': 'Negative Prompt. The negative prompt should NOT contain the trigger word.'}, 'style_strength_ratio': {'type': 'number', 'title': 'Style Strength Ratio', 'default': 20, 'maximum': 50, 'minimum': 15, 'x-order': 8, 'description': 'Style strength (%)'}, 'disable_safety_checker': {'type': 'boolean', 'title': 'Disable Safety Checker', 'default': False, 'x-order': 12, 'description': 'Disable safety checker for generated images.'}}}, 'Output': {'type': 'array', 'items': {'type': 'string', 'format': 'uri'}, 'title': 'Output'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'style_name': {'enum': ['(No style)', 'Cinematic', 'Disney Charactor', 'Digital Art', 'Photographic (Default)', 'Fantasy art', 'Neonpunk', 'Enhance', 'Comic book', 'Lowpoly', 'Line art'], 'type': 'string', 'title': 'style_name', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}}}}
model_id = 'tencentarc/photomaker'
model_version = 'ddfc2b08d209f9fa8c1eca692712918bd449f695dabb4a958da31802a9570fe4'