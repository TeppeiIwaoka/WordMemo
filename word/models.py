from django.conf import settings
from django.db import models
from django.urls import reverse


class Word(models.Model):
    PART_OF_SPEECH = [
        ('n.', 'Noun'),
        ('pro.', 'Pronoun'),
        ('v.', 'Verb'),
        ('adj.', 'Adjective'),
        ('adv.', 'Adverb'),
        ('prep.', 'Preposition'),
        ('conj.', 'Conjunction'),
        ('int.', 'Interjection'),
    ]
    word = models.CharField(max_length=255)
    part_of_speech = models.CharField(max_length=255, choices=PART_OF_SPEECH)
    definition = models.TextField('word', max_length=255)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["word", "part_of_speech", "created_user"],
                name="word_unique"
            ),
        ]

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        return reverse('word:home')
