from django import forms

from . import models


class ScoreForm(forms.ModelForm):
    class Meta:
        model = models.Mark
        fields = ('user', 'film', 'score')

    def clean_score(self):
        score = self.cleaned_data['score']
        if score < 0 or score > 10:
            raise forms.ValidationError('评分范围 0 ~ 10')

        film = self.cleaned_data['film']
        user = self.cleaned_data['user']
        if models.Mark.objects.filter(film__id=film.id, user__id=user.id):
            raise forms.ValidationError('此用户已对此电影评论')

        return score




