import requests
import json
from common.exception_detections import get_error


from config.global_variables import (
    CLASSIFICATION_INVOKE_SERVICE
)

# Dapr service details
dapr_app_id = "model_layer"
dapr_method = "adaboost_classification"
dapr_port = 3500  # Default Dapr sidecar port

# URL for invoking Dapr service
url = f"{CLASSIFICATION_INVOKE_SERVICE}/v1.0/invoke/{dapr_app_id}/method/events/pubsub/{dapr_method}"

# Data to send in the request
data = {"key": "value"}

# Set content type to JSON
headers = {"Content-Type": "application/json"}

# Make the HTTP request


def invoking_classification_service(image_path, x1, x2, y1, y2):
    try:
        response = requests.post(url, headers=headers, params={
                                "image_path": image_path,
                                "x1":int(x1),
                                "x2":int(x2),
                                "y1":int(y1),
                                "y2":int(y2)
                                })

        # Print the response
        print('here is the response',response.json())
        print(response.status_code)
        if int(response.status_code)!=200:
            raise RuntimeError(f'error occur in invoking classification service status code is {response.status_code}')
        print(response.json())
    except Exception as e:
        error = get_error(e)
        raise RuntimeError(error)
    else:
        return response.json()
