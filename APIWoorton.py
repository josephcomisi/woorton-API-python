import requests
import json
import time


class APIWoorton(object):
    """
    Woorton OTC Public API
    Clients must be registered to Woorton OTC service to use this API.
    """

    def __init__(self, token):
        """
        Create an object to make API requests with authentification information
        :param token: token provided by Woorton team
        """

        self.__api_url = 'https://woorton-sandbox.herokuapp.com/api/'
        self.__version = 'v1'

        self.__name_path_map = {}
        self.__add_path_map('rfq', '/request_quotes')
        self.__add_path_map('trades', '/trades')
        self.__add_path_map('instruments', '/instruments')
        self.__add_path_map('balances', '/balances')
        self.__add_path_map('exposures', '/exposures')
        self.__add_path_map('ledger', '/ledger')

        self.__headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        self.rfq = {}
        self.response = {}
        self.execution = {}
        self.state = ''

        self.__methods = ['GET', 'POST']

        self.instrument_list = []
        self.__update_instruments()

        self.ledger_operations = ['trade', 'withdrawal', 'deposit']

    def __add_path_map(self, name, uri):
        self.__name_path_map[name] = self.__api_url + self.__version + uri

    def help(self):
        print 'Woorton API - Endpoints:'
        for key, value in self.__name_path_map.items():
            print('Action: {}, URL: {}'.format(key, value))

    def __call(self, action_name, method, params):
        if method not in self.__methods:
            raise Exception('wrong method')

        if action_name not in self.__name_path_map.keys():
            raise Exception('wrong action name')

        # URL
        url = str(self.__name_path_map[action_name])

        # Body
        body = json.dumps(params)

        try:
            # Request
            if method == 'GET':
                request = requests.get(url, body, headers=self.__headers)
            else:
                request = requests.post(url, body, headers=self.__headers)

            # Response
            self.response = request.json()

            if 'errors' in self.response:
                raise Exception(self.response['errors'][0]['message'])

            return self.response

        except Exception as ex:
            print 'API Woorton Error: ' + str(ex)

    # API Endpoints

    def request_for_quote(self, amount, instrument, direction):
        """
        Request For Quote at Woorton. Once the quotation is returned (in response),
        you will have a short delay to confirm with the function execute
        :param amount: amount in base currency
        :param instrument: product (example: BTCEUR.SPOT)
        :param direction: 'buy' or 'sell' the base currency
        :return: json result from API
        """
        direction = str(direction).lower()

        if direction not in ['buy', 'sell']:
            raise Exception('wrong direction')

        if instrument not in self.instrument_list:
            raise Exception('wrong instrument')

        if not isinstance(amount, (float, int)) or not isinstance(float(amount), (float, int)) or amount < 0.0:
            raise Exception('wrong amount')

        params = {
            'client_request_id': str(int(100000*time.time())),
            'amount': amount,
            'instrument': instrument,
            'direction': direction,
        }

        self.rfq = params
        self.state = 'pending'
        self.response = self.__call('rfq', 'POST', params)

        return self.response

    def execute(self):
        """
        Confirm the last Request For Quote at Woorton
        Quotation can only be confirmed, not changed.
        :return: json result from API
        """
        params = {
            'request_id': self.response['request_id'],
            'amount': self.response['amount'],
            'instrument': self.response['instrument'],
            'direction': self.response['direction'],
            'total': self.response['total'],
        }

        self.execution = self.__call('trades', 'POST', params)
        self.state = self.execution['state']

        return self.execution

    def ledger(self, operation=''):
        """
        List all ledger operations at Woorton
        :param operation: category can be trade, withdrawal or deposit.
        :return: json result from API
        """
        params = {}
        if operation != '':
            if operation not in self.ledger_operations:
                raise Exception('wrong operation')
            else:
                params = {'operation': operation}

        return self.__call('ledger', 'GET', params)

    def trades(self, page=0):
        """
        List all trades executed at Woorton
        At most 50 items are returned per query
        :return: json result from API
        """
        if not isinstance(page, int) or not isinstance(int(page), int) or page < 0:
            raise Exception('wrong page')

        params = {}
        if page != 0:
            params = {'page': page}

        return self.__call('trades', 'GET', params)

    def balances(self):
        """
        List all your balances at Woorton
        Negative amount: you owe Woorton the amount
        Positive amount: Woorton owe you the amount
        :return: json result from API
        """
        return self.__call('balances', 'GET', {})

    def exposures(self):
        """
        List your allowed exposures for all currencies at Woorton
        Remaining exposures = Exposures - Balances
        :return: json result from API
        """
        return self.__call('exposures', 'GET', {})

    def instruments(self):
        """
        List all instruments available on the API Woorton
        :return: json result from API
        """
        return self.__call('instruments', 'GET', {})

    # Functions

    def __update_instruments(self):
        instruments = self.instruments()
        for instrument in instruments['instrument']:
            self.instrument_list.append(instrument)

    def market_order(self, amount, instrument, direction):
        self.request_for_quote(amount, instrument, direction)
        self.execute()
        return self.state

    def remaining_exposures(self):
        exposures = self.exposures()
        balances = self.balances()

        remaining_exposures = {}
        for currency, balance in exposures.items():
            remaining_exposures[currency] = float(balance) - float(balances[currency])

        return remaining_exposures
