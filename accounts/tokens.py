from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Generate the hash based on user-specific data
        return f"{user.pk}{timestamp}{user.is_active}"

account_activation_token = AccountActivationTokenGenerator()
