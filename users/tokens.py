from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, order, timestamp):
        return (
            six.text_type(order.pk) + six.text_type(timestamp)
        )
account_activation_token = TokenGenerator()
