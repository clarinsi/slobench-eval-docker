from eval_seq_pair import calculate_nli


def evaluate(data_ground_truth_path, data_submission_path):
     try:
          with open(f'./{data_ground_truth_path}/si-nli.txt') as f_submission:
               ground_truth = list(filter(lambda _line: len(_line) > 0, map(lambda _s: _s.strip().lower(), f_submission.readlines())))
     except Exception as e:
          raise Exception(f'Exception in opening ground truth file: {e}')

     try:
          with open(f'./{data_submission_path}/submission.txt') as f_correct:
               submission = list(filter(lambda _line: len(_line) > 0, map(lambda _s: _s.strip().lower(), f_correct.readlines())))
               if not submission:
                    raise Exception(f'Submission file is empty.')
     except Exception as e:
          raise Exception(f'Exception in opening submission file: {e}')

     assert len(ground_truth) == len(submission), f'Mismatch in number of rows: got {len(submission)} submitted predictions, ' \
                                                  f'expected {len(ground_truth)} predictions'

     try:
          metrics = calculate_nli(submission, ground_truth)
          return metrics
     except Exception as e:
          raise Exception(f'Exception in metric calculation: {e}')