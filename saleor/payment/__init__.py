import importlib
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import pgettext_lazy


class PaymentError(Exception):
    pass


class TransactionType:
    AUTH = 'auth'
    CHARGE = 'charge'
    VOID = 'void'
    REFUND = 'refund'

    CHOICES = [(AUTH, pgettext_lazy('transaction type', 'Authorization')),
               (CHARGE, pgettext_lazy('transaction type', 'Charge')),
               (REFUND, pgettext_lazy('transaction type', 'Refund')),
               (VOID, pgettext_lazy('transaction type', 'Void'))]


class PaymentMethodChargeStatus:
    CHARGED = 'charged'
    NOT_CHARGED = 'not-charged'
    FULLY_REFUNDED = 'fully-refunded'

    CHOICES = [
        (CHARGED, pgettext_lazy('payment method status', 'Charged')),
        (NOT_CHARGED, pgettext_lazy('payment method status', 'Not charged')), (
            FULLY_REFUNDED,
            pgettext_lazy('payment method status', 'Fully refunded'))]


# FIXME: move to settings
PROVIDERS_MAP = {
    'default': {
        'module': 'saleor.payment.providers.dummy',
        'params': {}},

    'braintree': {
        'module': 'saleor.payment.providers.braintree',
        'params': {
            'sandbox_mode': True,
            'merchant_id': '',
            'public_key': '',
            'private_key': ''
        }
    }

}


def get_provider(provider_name):
    if provider_name not in PROVIDERS_MAP:
        raise ImproperlyConfigured(
            f'Payment provider {provider_name} is not configured.')
    provider_module = importlib.import_module(PROVIDERS_MAP[provider_name]['module'])
    provider_params = PROVIDERS_MAP[provider_name]['params']
    return provider_module, provider_params