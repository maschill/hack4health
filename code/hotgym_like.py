

# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""A simple client to create a CLA model for hotgym."""

import csv
import datetime
import logging

from pkg_resources import resource_filename

from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.model_factory import ModelFactory
from nupic.frameworks.opf.prediction_metrics_manager import MetricsManager

import model_params_hotgym_like as model_params

_LOGGER = logging.getLogger(__name__)

_INPUT_FILE_PATH = '../local_hack4health/sim.csv'

print _INPUT_FILE_PATH

_METRIC_SPECS = (
    MetricSpec(field='count', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'aae', 'window': 100, 'steps': 2}),
    MetricSpec(field='count', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'aae', 'window': 100, 'steps': 2}),
    MetricSpec(field='count', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'altMAPE', 'window': 100, 'steps': 2}),
    MetricSpec(field='count', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'altMAPE', 'window': 100, 'steps': 2}),
)

_NUM_RECORDS =


def createModel():
  return ModelFactory.create(model_params.MODEL_PARAMS)

import matplotlib.pyplot as plt
def runHotgym():
  old, old2 = None,None
  predictions = []
  model = createModel()
  model.enableInference({'predictedField': 'count'})
  metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
                                  model.getInferenceType())
  with open (_INPUT_FILE_PATH) as fin:
    reader = csv.reader(fin)
    headers = reader.next()
    reader.next()
    reader.next()
    for i, record in enumerate(reader, start=1):
      modelInput = dict(zip(headers, record))
      modelInput["count"] = float(modelInput["count"])
      modelInput["Influenza"] = float(modelInput["Influenza"])
      modelInput["Windrichtung"] = float(modelInput["Windrichtung"])
      modelInput["Temperatur"] = float(modelInput["Temperatur"])
      modelInput["Luftfeuchte"] = float(modelInput["Luftfeuchte"])
      modelInput["Windgeschwindigkeit"] = float(modelInput["Windgeschwindigkeit"])
      modelInput["Barnim County"] = float(modelInput["Barnim County"])
      modelInput["Dahme-Spreewald County"] = float(modelInput["Dahme-Spreewald County"])
      modelInput["Havelland County"] = float(modelInput["Havelland County"])
      modelInput["Markisch-Oderland County"] = float(modelInput["Markisch-Oderland County"])
      modelInput["Oberhavel County"] = float(modelInput["Oberhavel County"])
      modelInput["Oder-Spree County"] = float(modelInput["Oder-Spree County"])
      modelInput["City of Potsdam"] = float(modelInput["City of Potsdam"])
      modelInput["Potsdam-Mittelmark County"] = float(modelInput["Potsdam-Mittelmark County"])
      modelInput["Teltow-Flaming County"] = float(modelInput["Teltow-Flaming County"])
      modelInput["timestamp"] = datetime.datetime.strptime(modelInput["timestamp"], "%Y-%m-%d")
    #   modelInput['x'] = float(modelInput['x'])
    #   modelInput['y'] = float(modelInput['y'])
      result = model.run(modelInput)
      result.metrics = metricsManager.update(result)
      isLast = i == _NUM_RECORDS
      if old2:
          predictions.append([old,float(result.inferences["multiStepBestPredictions"][1])])
      old2 = old
      old = modelInput["x"]
    #   print result.inferences["multiStepBestPredictions"][1]
      if i % 100 == 0 or isLast:
        _LOGGER.info("After %i records, 1-step altMAPE=%f", i,
                    result.metrics["multiStepBestPredictions:multiStep:"
                                   "errorMetric='altMAPE':steps=1:window=1000:"
                                   "field=count"])
      if isLast:
				print('=========================================================')
				print len(predictions)
				return predictions

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	predictions = runHotgym()
	with open('custom_err.csv', 'wb') as f:
		cw = csv.writer(f)
		cw.writerows(r for r in predictions)
