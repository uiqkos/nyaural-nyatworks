from django.forms import Form, ChoiceField, TextInput


class PredictForm(Form):
    input_type = ChoiceField(choices=('ручной ввод текста', 'vk', 'twitter', 'reddit', 'youtube'))
    text = TextInput()
