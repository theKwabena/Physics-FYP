from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class SupervisorTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_harsh_value(self,user, timestamp):
        return (six.text_type (user.id) + six.text_type(timestamp) + six.text_type(user.supervisor.verified))
    
generate_supervisor_token = SupervisorTokenGenerator()



