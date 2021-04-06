from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import secrets


class PollManager(models.Manager):
    def get_by_natural_key(self, text):
        return self.get(text=text)


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    objects = PollManager()

    def natural_key(self):
        return (self.text,)

    def user_can_vote(self, user):
        """
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res

    def __str__(self):
        return self.text


class ChoiceManager(models.Manager):
    def get_by_natural_key(self, poll_text, choice_text):
        return self.get(poll__text=poll_text, choice_text=choice_text)


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    objects = ChoiceManager()

    def natural_key(self):
        return (self.poll.natural_key()[0], self.choice_text)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class VoteManager(models.Manager):
    def get_by_natural_key(self, poll_text, choice_poll_text, choice_text):
        return self.get(poll__text=poll_text, choice__poll__text=choice_poll_text, choice__choice_text=choice_text)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    objects = VoteManager()

    def natural_key(self):
        return self.poll.natural_key() + self.choice.natural_key()

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'
