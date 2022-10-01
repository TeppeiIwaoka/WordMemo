from django import forms

from .models import Word


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ('word', 'part_of_speech',)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        word = self.cleaned_data.get('word')
        part_of_speech = self.cleaned_data.get('part_of_speech')
        word_exists = Word.objects.filter(word=word, part_of_speech=part_of_speech, created_user=self.user).exists()
        if word_exists:
            raise forms.ValidationError(
                'The pair of word and part_of_speech already exists. Please change word or part of speech')
