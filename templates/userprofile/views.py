
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import CreateView

from userprofile.forms import NewAccountForm
import random
import string


class CreateNewAccount(LoginRequiredMixin, CreateView):
    model = User
    template_name = 'location/location_form.html'
    form_class = NewAccountForm

    def get_success_url(self):
        psw = ''.join(
            random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + '$%^&') for _
            in range(8))

        if (user_instance := User.objects.filter(id=self.object.id)) and user_instance.exists():
            user_object = user_instance.first()
            user_object.set_password(psw)
            user_object.save()

            content1 = f'Buna ziua.\n Datele de aut sunt: \n username: {user_object.username} \nparola: {psw}'
            msg_html = render_to_string('registration/invite_user.html', {'content_email': content1})

            email = EmailMultiAlternatives(subject='Date contact platforma',
                                           body=content1,
                                           from_email='contact@jobs',
                                           to=[user_object.email()])
            email.attach_alternatives(msg_html, 'text/html')
            email.send()

        return reversed('location:lista_locatii')
