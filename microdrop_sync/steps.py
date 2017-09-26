from .utils import MicrodropUtils


class Steps(object):

    def __init__(self, ms):
        self.ms = ms

    def current_step(self):
        return self.ms.get_state_sync("step-model", "step")

    def delete_step(self, step_number):
        self.validate_step_number(len(self.steps())-2)
        self.validate_step_number(step_number)
        msg = {'stepNumber': step_number}
        success_topic = MicrodropUtils.get_state_topic('step-model', 'steps')
        return self.ms.trigger_sync('step-model', 'delete-step', msg,
                                    success_topic=success_topic)

    def get_step_params(self, step_number):
        s = self.get_step(step_number)
        return {k: v for d in s.values() for k, v in d.items()}

    def get_step(self, step_number):
        self.validate_step_number(step_number)
        steps = self.steps()
        return steps[step_number]

    def insert_step(self, step_number):
        self.validate_step_number(step_number)
        msg = {'stepNumber': step_number}
        success_topic = MicrodropUtils.get_state_topic('step-model', 'steps')
        return self.ms.trigger_sync('step-model', 'insert-step', msg,
                                    success_topic=success_topic)

    def set_step_param(self, key, val, step_number):
        data = {'key': key, 'val': val, 'stepNumber': step_number}
        msg = {'data': data}
        success_topic = MicrodropUtils.get_state_topic('step-model', 'steps')
        return self.ms.trigger_sync('step-model', 'update-step', msg,
                                    success_topic=success_topic)

    def steps(self):
        return self.ms.get_state_sync("step-model", "steps")

    def step_number(self):
        return self.ms.get_state_sync("step-model",
                                      "step-number")['stepNumber']

    def switch_step(self, step_number):
        self.validate_step_number(step_number)
        msg = {'stepNumber': step_number}
        success_topic = MicrodropUtils.get_state_topic('step-model',
                                                       'step-number')
        return self.ms.put_sync('step-model', 'step-number', msg,
                                success_topic)

    def validate_step_number(self, step_number):
        steps = self.steps()
        if (step_number >= len(steps)):
            raise RuntimeError("STEP NUMBER OUT OF REACH")
        if (step_number < 0):
            raise RuntimeError("STEP NUMBER LESS THAN ZERO")
