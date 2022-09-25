from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class StudentTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_harsh_value(self,user, timestamp):
        return (six.text_type (user.id) + six.text_type(timestamp) + six.text_type(user.student.verified))
    
    
generate_student_token = StudentTokenGenerator()