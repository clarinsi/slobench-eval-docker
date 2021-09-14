def evaluate(test, submission):
     try:
          shared_items = {k: test[k] for k in test if k in submission and test[k] == submission[k]}
          metrics = {
               'overall': float(len(shared_items) / len(test)) * 100,
               'metric1': 11.0,
               'metric2': 12.0,
               'metric3': 13.0
          }
          return metrics
     except Exception as e:
          raise Exception('Evaluation script exception')