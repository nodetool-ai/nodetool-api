schema = {'info': {'title': 'Cog', 'version': '0.1.0'}, 'paths': {'/': {'get': {'summary': 'Root', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Root  Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'root__get'}}, '/shutdown': {'post': {'summary': 'Start Shutdown', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Start Shutdown Shutdown Post'}}}, 'description': 'Successful Response'}}, 'operationId': 'start_shutdown_shutdown_post'}}, '/predictions': {'post': {'summary': 'Predict', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model', 'operationId': 'predict_predictions_post', 'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionRequest'}}}}}}, '/health-check': {'get': {'summary': 'Healthcheck', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Healthcheck Health Check Get'}}}, 'description': 'Successful Response'}}, 'operationId': 'healthcheck_health_check_get'}}, '/predictions/{prediction_id}': {'put': {'summary': 'Predict Idempotent', 'responses': {'200': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PredictionResponse'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}, {'in': 'header', 'name': 'prefer', 'schema': {'type': 'string', 'title': 'Prefer'}, 'required': False}], 'description': 'Run a single prediction on the model (idempotent creation).', 'operationId': 'predict_idempotent_predictions__prediction_id__put', 'requestBody': {'content': {'application/json': {'schema': {'allOf': [{'$ref': '#/components/schemas/PredictionRequest'}], 'title': 'Prediction Request'}}}, 'required': True}}}, '/predictions/{prediction_id}/cancel': {'post': {'summary': 'Cancel', 'responses': {'200': {'content': {'application/json': {'schema': {'title': 'Response Cancel Predictions  Prediction Id  Cancel Post'}}}, 'description': 'Successful Response'}, '422': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}, 'description': 'Validation Error'}}, 'parameters': [{'in': 'path', 'name': 'prediction_id', 'schema': {'type': 'string', 'title': 'Prediction ID'}, 'required': True}], 'description': 'Cancel a running prediction', 'operationId': 'cancel_predictions__prediction_id__cancel_post'}}}, 'openapi': '3.0.2', 'components': {'schemas': {'Input': {'type': 'object', 'title': 'Input', 'properties': {'protect': {'type': 'number', 'title': 'Protect', 'default': 0.33, 'maximum': 0.5, 'minimum': 0, 'x-order': 9, 'description': "Control how much of the original vocals' breath and voiceless consonants to leave in the AI vocals. Set 0.5 to disable."}, 'rvc_model': {'allOf': [{'$ref': '#/components/schemas/rvc_model'}], 'default': 'Squidward', 'x-order': 1, 'description': "RVC model for a specific voice. If using a custom model, this should match the name of the downloaded model. If a 'custom_rvc_model_download_url' is provided, this will be automatically set to the name of the downloaded model."}, 'index_rate': {'type': 'number', 'title': 'Index Rate', 'default': 0.5, 'maximum': 1, 'minimum': 0, 'x-order': 4, 'description': "Control how much of the AI's accent to leave in the vocals."}, 'song_input': {'type': 'string', 'title': 'Song Input', 'format': 'uri', 'x-order': 0, 'description': 'Upload your audio file here.'}, 'reverb_size': {'type': 'number', 'title': 'Reverb Size', 'default': 0.15, 'maximum': 1, 'minimum': 0, 'x-order': 14, 'description': 'The larger the room, the longer the reverb time.'}, 'pitch_change': {'allOf': [{'$ref': '#/components/schemas/pitch_change'}], 'default': 'no-change', 'x-order': 3, 'description': 'Adjust pitch of AI vocals. Options: `no-change`, `male-to-female`, `female-to-male`.'}, 'rms_mix_rate': {'type': 'number', 'title': 'Rms Mix Rate', 'default': 0.25, 'maximum': 1, 'minimum': 0, 'x-order': 6, 'description': "Control how much to use the original vocal's loudness (0) or a fixed loudness (1)."}, 'filter_radius': {'type': 'integer', 'title': 'Filter Radius', 'default': 3, 'maximum': 7, 'minimum': 0, 'x-order': 5, 'description': 'If >=3: apply median filtering median filtering to the harvested pitch results.'}, 'output_format': {'allOf': [{'$ref': '#/components/schemas/output_format'}], 'default': 'mp3', 'x-order': 18, 'description': 'wav for best quality and large file size, mp3 for decent quality and small file size.'}, 'reverb_damping': {'type': 'number', 'title': 'Reverb Damping', 'default': 0.7, 'maximum': 1, 'minimum': 0, 'x-order': 17, 'description': 'Absorption of high frequencies in the reverb.'}, 'reverb_dryness': {'type': 'number', 'title': 'Reverb Dryness', 'default': 0.8, 'maximum': 1, 'minimum': 0, 'x-order': 16, 'description': 'Level of AI vocals without reverb.'}, 'reverb_wetness': {'type': 'number', 'title': 'Reverb Wetness', 'default': 0.2, 'maximum': 1, 'minimum': 0, 'x-order': 15, 'description': 'Level of AI vocals with reverb.'}, 'crepe_hop_length': {'type': 'integer', 'title': 'Crepe Hop Length', 'default': 128, 'x-order': 8, 'description': 'When `pitch_detection_algo` is set to `mangio-crepe`, this controls how often it checks for pitch changes in milliseconds. Lower values lead to longer conversions and higher risk of voice cracks, but better pitch accuracy.'}, 'pitch_change_all': {'type': 'number', 'title': 'Pitch Change All', 'default': 0, 'x-order': 13, 'description': 'Change pitch/key of background music, backup vocals and AI vocals in semitones. Reduces sound quality slightly.'}, 'main_vocals_volume_change': {'type': 'number', 'title': 'Main Vocals Volume Change', 'default': 0, 'x-order': 10, 'description': 'Control volume of main AI vocals. Use -3 to decrease the volume by 3 decibels, or 3 to increase the volume by 3 decibels.'}, 'pitch_detection_algorithm': {'allOf': [{'$ref': '#/components/schemas/pitch_detection_algorithm'}], 'default': 'rmvpe', 'x-order': 7, 'description': 'Best option is rmvpe (clarity in vocals), then mangio-crepe (smoother vocals).'}, 'instrumental_volume_change': {'type': 'number', 'title': 'Instrumental Volume Change', 'default': 0, 'x-order': 12, 'description': 'Control volume of the background music/instrumentals.'}, 'backup_vocals_volume_change': {'type': 'number', 'title': 'Backup Vocals Volume Change', 'default': 0, 'x-order': 11, 'description': 'Control volume of backup AI vocals.'}, 'custom_rvc_model_download_url': {'type': 'string', 'title': 'Custom Rvc Model Download Url', 'x-order': 2, 'description': "URL to download a custom RVC model. If provided, the model will be downloaded (if it doesn't already exist) and used for prediction, regardless of the 'rvc_model' value."}}}, 'Output': {'type': 'string', 'title': 'Output', 'format': 'uri'}, 'Status': {'enum': ['starting', 'processing', 'succeeded', 'canceled', 'failed'], 'type': 'string', 'title': 'Status', 'description': 'An enumeration.'}, 'rvc_model': {'enum': ['Squidward', 'MrKrabs', 'Plankton', 'Drake', 'Vader', 'Trump', 'Biden', 'Obama', 'Guitar', 'Voilin', 'CUSTOM'], 'type': 'string', 'title': 'rvc_model', 'description': 'An enumeration.'}, 'WebhookEvent': {'enum': ['start', 'output', 'logs', 'completed'], 'type': 'string', 'title': 'WebhookEvent', 'description': 'An enumeration.'}, 'pitch_change': {'enum': ['no-change', 'male-to-female', 'female-to-male'], 'type': 'string', 'title': 'pitch_change', 'description': 'An enumeration.'}, 'output_format': {'enum': ['mp3', 'wav'], 'type': 'string', 'title': 'output_format', 'description': 'An enumeration.'}, 'ValidationError': {'type': 'object', 'title': 'ValidationError', 'required': ['loc', 'msg', 'type'], 'properties': {'loc': {'type': 'array', 'items': {'anyOf': [{'type': 'string'}, {'type': 'integer'}]}, 'title': 'Location'}, 'msg': {'type': 'string', 'title': 'Message'}, 'type': {'type': 'string', 'title': 'Error Type'}}}, 'PredictionRequest': {'type': 'object', 'title': 'PredictionRequest', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'input': {'$ref': '#/components/schemas/Input'}, 'webhook': {'type': 'string', 'title': 'Webhook', 'format': 'uri', 'maxLength': 65536, 'minLength': 1}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'output_file_prefix': {'type': 'string', 'title': 'Output File Prefix'}, 'webhook_events_filter': {'type': 'array', 'items': {'$ref': '#/components/schemas/WebhookEvent'}, 'default': ['start', 'output', 'logs', 'completed']}}}, 'PredictionResponse': {'type': 'object', 'title': 'PredictionResponse', 'properties': {'id': {'type': 'string', 'title': 'Id'}, 'logs': {'type': 'string', 'title': 'Logs', 'default': ''}, 'error': {'type': 'string', 'title': 'Error'}, 'input': {'$ref': '#/components/schemas/Input'}, 'output': {'$ref': '#/components/schemas/Output'}, 'status': {'$ref': '#/components/schemas/Status'}, 'metrics': {'type': 'object', 'title': 'Metrics'}, 'version': {'type': 'string', 'title': 'Version'}, 'created_at': {'type': 'string', 'title': 'Created At', 'format': 'date-time'}, 'started_at': {'type': 'string', 'title': 'Started At', 'format': 'date-time'}, 'completed_at': {'type': 'string', 'title': 'Completed At', 'format': 'date-time'}}}, 'HTTPValidationError': {'type': 'object', 'title': 'HTTPValidationError', 'properties': {'detail': {'type': 'array', 'items': {'$ref': '#/components/schemas/ValidationError'}, 'title': 'Detail'}}}, 'pitch_detection_algorithm': {'enum': ['rmvpe', 'mangio-crepe'], 'type': 'string', 'title': 'pitch_detection_algorithm', 'description': 'An enumeration.'}}}}
model_id = 'zsxkib/realistic-voice-cloning'
model_version = '0a9c7c558af4c0f20667c1bd1260ce32a2879944a0b9e44e1398660c077b1550'
model_info = {'hardware': 'Nvidia T4 GPU'}
