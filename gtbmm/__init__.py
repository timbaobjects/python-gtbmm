from datetime import datetime
from decimal import Decimal
from exceptions import EXCEPTIONS_MAP
from lxml import etree
import re
import requests


class GTBResponse(object):
    def __init__(self, response):
        try:
            self.xml = etree.fromstring(response)
        except:
            self.xml = etree.Element('response')

    def xpath(self, xpath):
        return self.xml.xpath(xpath).pop()

    @property
    def code(self):
        try:
            return self.xpath('/response/message/@code')
        except IndexError:
            return None

    def get(self, param):
        try:
            return self.xpath('/response/{}/text()'.format(param))
        except IndexError:
            return None


class GTBMobileMoney():
    base_url = "https://mm.gtbank.com:8443/webapi/sdynamic"
    _authenticated = False

    def post(self, payload={}):
        r = requests.post(self.base_url, payload)
        return GTBResponse(r.text)

    def __init__(self, account, pin):
        self.account = account
        self.pin = pin

    def auth(self, account=None, pin=None):
        self.account = account or self.account
        self.pin = pin or self.pin

        self._authenticated = False
        postdata = {
            'service': 'Account', 'txnName': 'Login',
            'sourceMDN': self.account, 'authenticationString': self.pin,
            'apptype': 'subapp', 'channelID': 7, 'institutionID': ''
        }

        response = self.post(postdata)
        if response.code == '630':
            self._authenticated = True
        elif response.code in EXCEPTIONS_MAP:
            raise EXCEPTIONS_MAP.get(response.code)

        return self._authenticated

    def balance(self):
        if (self._authenticated or self.auth()):
            postdata = {
                'service': 'Wallet', 'txnName': 'CheckBalance',
                'sourceMDN': self.account, 'sourcePIN': self.pin,
                'sourcePocketCode': '1', 'apptype': 'subapp', 'channelID': 7,
                'institutionID': ''
            }

            response = self.post(postdata)
            if response.code == '274':
                transaction_time = datetime.strptime(
                    response.get('transactionTime'),
                    '%d/%m/%y %H:%M'
                )
                transaction_id = response.get('sctlID')
                transaction_amount = Decimal(response.get('amount'))
                return {
                    'txn_id': transaction_id,
                    'txn_time': transaction_time,
                    'balance': transaction_amount
                }
            elif response.code == '631':
                self._authenticated = False
                raise EXCEPTIONS_MAP.get(response.code)
            elif response.code in EXCEPTIONS_MAP:
                raise EXCEPTIONS_MAP.get(response.code)

    def history(self):
        if (self._authenticated or self.auth()):
            postdata = {
                'service': 'Wallet', 'txnName': 'History',
                'sourceMDN': self.account, 'sourcePIN': self.pin,
                'sourcePocketCode': '1', 'apptype': 'subapp', 'channelID': 7,
                'institutionID': ''
            }

            response = self.post(postdata)
            if response.code == '39':
                for txn in response.xml.xpath(
                    '/response/transactionDetails/transactionDetail'
                ):
                    try:
                        transaction_time = datetime.strptime(
                            txn.xpath('./transactionTime/text()').pop(),
                            '%d/%m/%y %H:%M %Z'
                        )
                        transaction_id = txn.xpath('./refID/text()').pop()
                        commodity = txn.xpath('./commodityType/text()').pop()
                        txn_type = txn.xpath('./transactionType/text()').pop()
                        status = txn.xpath('./transactionStatus/text()').pop()
                        service_charge = Decimal(
                            re.sub('[^0-9\.]', '', txn.xpath(
                                './serviceCharge/text()').pop()))
                        source = txn.xpath('./sourceMDN/text()').pop()
                        destination = txn.xpath('./destMDN/text()').pop()
                        amount = Decimal(
                            re.sub('[^0-9\.]', '', txn.xpath(
                                './amount/text()').pop()))
                        yield {
                            'txn_id': transaction_id,
                            'txn_time': transaction_time,
                            'txn_amt': amount,
                            'txn_commodity': commodity,
                            'txn_type': txn_type,
                            'txn_status': status,
                            'txn_sc': service_charge,
                            'txn_from': source,
                            'txn_to': destination
                        }
                    except IndexError:
                        pass
            elif response.code == '631':
                self._authenticated = False
                raise EXCEPTIONS_MAP.get(response.code)
            elif response.code in EXCEPTIONS_MAP:
                raise EXCEPTIONS_MAP.get(response.code)

    def _beforeSend(self, to, amount):
        if (self._authenticated or self.auth()):
            postdata = {
                'service': 'Wallet', 'txnName': 'transferInquiry',
                'sourceMDN': self.account, 'sourcePIN': self.pin,
                'sourcePocketCode': '1', 'apptype': 'subapp', 'channelID': 7,
                'destMDN': to, 'destPocketCode': '1', 'amount': amount,
                'institutionID': ''
            }

            response = self.post(postdata)
            if response.code == '72':
                transaction_time = datetime.strptime(
                    response.get('transactionTime'),
                    '%d/%m/%y %H:%M'
                )
                debit_amt = Decimal(
                    response.get('debitamt'))
                credit_amt = Decimal(
                    response.get('creditamt'))
                charges = Decimal(
                    response.get('charges'))
                dest = response.get('destinationMDN')
                transfer_id = response.get('transferID')
                parent_id = response.get('parentTxnID')
                transaction_id = response.get('sctlID')
                mfa_mode = response.get('mfaMode')
                return {
                    'txn_id': transaction_id,
                    'txn_time': transaction_time,
                    'transfer_id': transfer_id,
                    'parent_id': parent_id,
                    'debit_amt': debit_amt,
                    'credit_amt': credit_amt,
                    'charges': charges,
                    'to': dest,
                    'mfa': mfa_mode
                }
            elif response.code == '631':
                self._authenticated = False
                raise EXCEPTIONS_MAP.get(response.code)
            elif response.code in EXCEPTIONS_MAP:
                raise EXCEPTIONS_MAP.get(response.code)

    def send(self, to, amount):
        if (self._authenticated or self.auth()):
            params = self._beforeSend(to, amount)

            if params:
                postdata = {
                    'service': 'Wallet', 'txnName': 'Transfer',
                    'sourceMDN': self.account, 'sourcePIN': self.pin,
                    'sourcePocketCode': '1', 'apptype': 'subapp',
                    'channelID': 7, 'destMDN': to, 'destPocketCode': '1',
                    'institutionID': '', 'confirmed': 'true',
                    'parentTxnID': params.get('parent_id'),
                    'transferID': params.get('transfer_id')
                }

                response = self.post(postdata)
                if response.code == '293':
                    transaction_time = datetime.strptime(
                        response.get('transactionTime'),
                        '%d/%m/%y %H:%M'
                    )
                    debit_amt = Decimal(
                        response.get('debitamt'))
                    credit_amt = Decimal(
                        response.get('creditamt'))
                    charges = Decimal(
                        response.get('charges'))
                    ref_id = response.get('refID')
                    transaction_id = response.get('sctlID')
                    return {
                        'txn_id': transaction_id,
                        'txn_time': transaction_time,
                        'transfer_id': params.get('transfer_id'),
                        'parent_id': params.get('parent_id'),
                        'debit_amt': debit_amt,
                        'credit_amt': credit_amt,
                        'charges': charges,
                        'to': params.get('to'),
                        'ref_id': ref_id
                    }
                elif response.code == '631':
                    self._authenticated = False
                    raise EXCEPTIONS_MAP.get(response.code)
                elif response.code in EXCEPTIONS_MAP:
                    raise EXCEPTIONS_MAP.get(response.code)
