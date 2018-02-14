from nupic.swarming import permutations_runner
from swarm_description import SWARM_DESCRIPTION
import os
import pprint as pp

from nupic.swarming.ModelRunner import OPFModelRunner

# The logger for this method
#logger = logging.getLogger('com.numenta.nupic.hypersearch.utils')

def writeModelParams(modelParams):
    outDir = os.path.join(os.getcwd(), "model_params_hard")
    if not os.path.isdir(outDir):
        os.mkdir(outDir)
    outPath = os.path.join(outDir, "model_params_hard.py")
    with open(outPath, 'wb') as of:
        modelParamsString = pp.pformat(modelParams)
        of.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
    return outPath

def swarm(inputFile):
    swarmWorkDir = os.path.abspath("swarmGT")
    if not os.path.exists(swarmWorkDir):
        os.mkdir(swarmWorkDir)
    modelParams = permutations_runner.runWithConfig(
        SWARM_DESCRIPTION,
        {"maxWorkers": 4, "overwrite": True},
        outputLabel="rki_faelle",
        outDir = swarmWorkDir,
        permWorkDir=swarmWorkDir
    )
    writeModelParams(modelParams)

if __name__ == "__main__":
    swarm('RKIGTData.csv')