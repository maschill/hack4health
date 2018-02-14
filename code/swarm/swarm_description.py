SWARM_DESCRIPTION = {
    "includedFields":[
        {
            "fieldName": "wstday",
            "fieldType": "datetime"
        },
        {
            "fieldName": "Grippe",
            "fieldType": "float",
            "maxValue": 100,
            "minValue": 0
        },
        {
            "fieldName": "Influenza",
            "fieldType": "float",
            "minValue": 0,
            "maxValue": 25
        },
        {
            "fieldName": "faelle",
            "fieldType": "float",
            "maxValue": 98,
            "minValue": 1
        }
    ],
    "streamDef": {
        "info": "RKIGTData",
        "version": 1,
        "streams": [
            {
                "info": "rki_gt_faelle",
                "source": "testtt/RKIGTData.csv",
                "columns": [
                    "*"
                ]
            }
        ]
    },
    "inferenceType":"TemporalMultiStep",
    "inferenceArgs":{
        "predictionSteps": [
            1
        ],
        "predictedField": "faelle"
    },
    "iterationCount": -1,
    "swarmSize": "medium"
}