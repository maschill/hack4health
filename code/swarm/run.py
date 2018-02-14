import csv
import datetime
import sys
import os
import time
sys.path.insert(0, os.path.join(os.getcwd(), 'model_params'))
from model_params import MODEL_PARAMS
from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.data.inference_shifter import InferenceShifter
import nupic_output

#MODEL_PARAMS_ = os.path.join(os.getcwd(), "model_params")
DATE_FORMAT = "%Y-%m-%d"
#OUTPUT_FILE = "rki_faelle.csv"
#output = open(OUTPUT_FILE, 'w')

def createModel():
    model = ModelFactory.create(MODEL_PARAMS)
    model.enableInference({
        "predictedField": "faelle"
    })
    return model

def runModel(model):
    predictions = []
    inputFilePath = "RKIGTData.csv"
    inputFile = open(inputFilePath, 'rb')
    csvReader = csv.reader(inputFile)
    # Skip header
    csvReader.next()
    csvReader.next()
    csvReader.next()

    shifter = InferenceShifter()
    output = nupic_output.NuPICPlotOutput(["rki_faelle"])

    counter = 0
    for row in csvReader:
        counter += 1
        if (counter % 100 == 0):
            print("Read %i lines ..." % counter)
            time.sleep(1)
        timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
        grippe = float(row[1])
        flu = float(row[2])
        faelle = float(row[3])
        result = model.run({
            "wstday": timestamp,
            "Grippe": grippe,
            "Influenza": flu,
            "faelle": faelle
        })

        result = shifter.shift(result)
        prediction = result.inferences["multiStepBestPredictions"][1]
        output.write(str(timestamp) + ',' + str(faelle) + ','+ str(prediction) + '\n')
        #output.write([timestamp], [faelle], [prediction])
    inputFile.close()
    output.close()
        #predictions += [prediction]
    #return predictions

def runInfluenza():
    model = createModel()
    runModel(model)

if __name__ == "__main__":
    runInfluenza()