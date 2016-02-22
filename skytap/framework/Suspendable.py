from skytap.framework.ApiClient import ApiClient
import time


class Suspendable(object):
    valid_states = ['running', 'suspended', 'reset', 'stopped', 'halted']

    def suspend(self, wait=False):
        self.change_state('suspended', wait)

    def run(self, wait=False):
        self.change_state('running', wait)

    def halt(self, wait=False):
        self.change_state('halted', wait)

    def reset(self, wait=False):
        self.change_state('reset', wait)

    def stop(self, wait=False):
        self.change_state('stopped', wait)

    def change_state(self, state, wait=False):
        if state not in Suspendable.valid_states:
            raise ValueError(str(state) + ' not a valid state.')

        self.refresh()
        if self.runstate == state:
            return True

        self.notes.add("Changing state via API to '" + state + "'")

        api = ApiClient()
        url = self.url + '.json'
        data = {"runstate": state}
        response = api.rest(url, {}, 'PUT', data)
        if not wait:
            return True

        if state == 'reset':
            state = 'running'

        if state == 'halted':
            state = 'stopped'

        self.refresh()
        counter = 0
        while not self.runstate == state and counter < 12:
            time.sleep(10)
            self.refresh()
        if self.runstate == state:
            return True
        return False
