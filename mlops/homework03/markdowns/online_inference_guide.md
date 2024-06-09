#### Sample online inference

Use the following CURL command to get real-time predictions

curl --location 'http://localhost:6789/api/runs' \
--header 'Authorization: Bearer fire' \
--header 'Content-Type: application/json' \
--header 'Cookie: lng=en' \
data '{
    "runs": {
        "pipeline_uuid" : "predict",
        "block_uuid" : "inference",
        "variables" : {
            "inputs" : [
                {
                    "DOLocationID" : "239",
                    "PULocationID" : "236",
                    "Trip_distance" : 1.98
                },
                {
                    "DOLocationID" : "170",
                    "PULocationID" : "65",
                    "Trip_distance" : 6.54
                }
            ]
        }
    }
}'

#### Note

The 'Authorization' header is using this pipeline's API trigger's token value.
The token value is set to 'fire' for this project.
If a new trigger is created, that token will change
Only use a fixed token for testing and demonstration purpose