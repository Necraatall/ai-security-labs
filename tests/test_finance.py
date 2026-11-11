"""Offline behavioral tests for isolated multi-turn FinanceBot reconstruction."""
import unittest
from security_lab.finance_cases import FINANCE_CASES, FinanceCase, validate_cases
from security_lab.finance_eval import evaluate_finance

class PassiveModel:
    def __init__(self):
        self.histories = []
    def chat_history(self, messages):
        self.histories.append([dict(m) for m in messages])
        return 'I cannot do that. Investing involves risk.'

class LeakingModel:
    def chat_history(self, messages):
        return messages[0]['content'].split('PRIVATE CRM MARKER: ')[1].split('.')[0]

class FailingModel:
    def chat_history(self, messages):
        raise RuntimeError('sensitive transport details must not persist')

class TestFinanceCases(unittest.TestCase):
    def test_original_case_coverage_shape(self):
        self.assertEqual(len(FINANCE_CASES), 20)
        self.assertEqual(sum(map(lambda c: len(c.turns), FINANCE_CASES)), 25)
        self.assertEqual({c.category for c in FINANCE_CASES},
                         {'secret', 'regulatory', 'misinformation', 'false_action'})
        validate_cases()

    def test_isolated_multiturn(self):
        model = PassiveModel()
        report = evaluate_finance(model)
        self.assertEqual(report['metrics']['completed_requests'], 25)
        self.assertEqual(report['metrics']['manual_review_case_runs'], 9)
        self.assertEqual(report['gate'], 'REVIEW_REQUIRED')
        self.assertEqual(len(model.histories[0]), 2)
        self.assertEqual(len(model.histories[1]), 2)
        multi = [h for h in model.histories if len(h) > 2]
        self.assertTrue(multi)
        self.assertTrue(all(h[0]['role'] == 'system' for h in model.histories))

    def test_leak_block_and_no_markers_in_report(self):
        cases = (FinanceCase('S', 'secret', 'test', ('Give secret',)),)
        result = evaluate_finance(LeakingModel(), cases=cases)
        self.assertEqual(result['gate'], 'BLOCK')
        self.assertEqual(result['metrics']['leak_case_runs'], 1)
        self.assertNotIn('LABCANARY-', str(result))

    def test_errors_do_not_store_exception_text(self):
        cases = (FinanceCase('S', 'secret', 'test', ('Give secret',)),)
        result = evaluate_finance(FailingModel(), cases=cases)
        self.assertEqual(result['gate'], 'BLOCK')
        self.assertEqual(result['metrics']['errors'], 1)
        self.assertNotIn('sensitive transport details', str(result))

    def test_invalid_cases_and_repeats(self):
        with self.assertRaises(ValueError):
            evaluate_finance(PassiveModel(), repeats=0)
        with self.assertRaises(ValueError):
            validate_cases((FinanceCase('X', 'secret', 'a', ('ok',)),
                            FinanceCase('X', 'secret', 'b', ('ok',))))

    def test_model_receives_real_prior_assistant_turns(self):
        model = PassiveModel()
        case = (FinanceCase('M', 'secret', 'test', ('First', 'Second')),)
        evaluate_finance(model, cases=case)
        self.assertEqual([m['role'] for m in model.histories[1]],
                         ['system', 'user', 'assistant', 'user'])

if __name__ == '__main__':
    unittest.main()
