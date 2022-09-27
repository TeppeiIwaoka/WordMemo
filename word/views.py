import json
import logging

import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from environs import Env

from .models import Word

env = Env()
env.read_env()


class DictionaryAPIException(Exception):
    pass


class WordList(LoginRequiredMixin, ListView):
    model = Word
    template_name = 'word/home.html'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(created_user=self.request.user)
        return queryset


class WordAdd(CreateView):
    model = Word
    template_name = 'word/new_word.html'
    fields = ('word', 'part_of_speech')
    success_url = reverse_lazy('word:home')

    def form_valid(self, form):
        word = form.save(commit=False)
        try:
            word.definition = self._get_definition(word=word.word,
                                                   part_of_speech=word.get_part_of_speech_display().lower())
            word.created_user = self.request.user
            return super().form_valid(form)
        except DictionaryAPIException as e:
            logging.error(e)
            return render(self.request, 'word/new_word.html', {'form': form, 'error_message': e})

    def _get_definition(self, word, part_of_speech):
        app_id = env.str("APP_ID")
        app_key = env.str("APP_KEY")
        url = f"https://od-api.oxforddictionaries.com/api/v2/words/en-gb?q={word}&lexicalCategory={part_of_speech}&fields=definitions"
        response = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
        if response.status_code != 200:
            raise DictionaryAPIException(
                "Get word definition failed. please confirm again if word and part of speech are correct.")
        response_data = json.loads(response.text)
        return response_data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]


class WordEdit(UpdateView):
    model = Word
    template_name = 'word/edit.html'
    fields = ('definition',)


class WordDelete(DeleteView):
    model = Word
    template_name = 'word/delete.html'
    success_url = reverse_lazy('word:home')
