![](nya_app/static/img/logo.png)

```
 __   __     __  __     ______     __  __     ______     ______     __              
/\ "-.\ \   /\ \_\ \   /\  __ \   /\ \/\ \   /\  == \   /\  __ \   /\ \            
\ \ \-.  \  \ \____ \  \ \  __ \  \ \ \_\ \  \ \  __<   \ \  __ \  \ \ \____      
 \ \_\\"\_\  \/\_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\    
  \/_/ \/_/   \/_____/   \/_/\/_/   \/_____/   \/_/ /_/   \/_/\/_/   \/_____/   
  __   __     __  __     ______     ______   __     __     ______     ______     __  __     ______
 /\ "-.\ \   /\ \_\ \   /\  __ \   /\__  _\ /\ \  _ \ \   /\  __ \   /\  == \   /\ \/ /    /\  ___\
 \ \ \-.  \  \ \____ \  \ \  __ \  \/_/\ \/ \ \ \/ ".\ \  \ \ \/\ \  \ \  __<   \ \  _"-.  \ \___  \
  \ \_\\"\_\  \/\_____\  \ \_\ \_\    \ \_\  \ \__/".~\_\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \/\_____\
   \/_/ \/_/   \/_____/   \/_/\/_/     \/_/   \/_/   \/_/   \/_____/   \/_/ /_/   \/_/\/_/   \/_____/ 
                                                                                                                                                                                                                                                                                                                                                              
```                                                                                                                                                                                   

## Api
### Модели

`GET` /models/ - список моделей
#### Пример ответа
 ```json
[
  {
    "local_name": "sentiment/const_random",
    "name": "Random constant",
    "struct": "OrderedDict()",
    "target": "sentiment"
  }
]
```
### Анализ
`GET` /predict/
#### Параметры
- **input**: тип ввода (auto, vk, youtube, ...)
- **text**: что анализировать (текст или ссылка)
- **toxic**: local_name модели анализа токсичности
- **sentiment**: local_name модели анализа эмоциональности
- **sarcasm**: local_name модели анализа саркастичности
- **page**: номер страницы для пагинации (если 0, то все комментарии на одной странице)
- **per_page**: количество комментариев на странице
- **styled(временно)**: добавить стили для комментария
- **stats(временно)**: добавить стили для общей оценки
### Пример ответа
page=1&per_page=1
```json
{
    "items": [
        {
            "text": "...",
            "author": {
                "name": "...",
                "photo": "..."
            },
            "date": "2022-01-31",
            "level": 0,
            "sentiment": {
                "positive": 0.08320649713277817,
                "neutral": 0.9154757857322693,
                "negative": 0.0013178198132663965
            },
            "toxic": {
                "no toxic": 0.5578645467758179,
                "toxic": 0.44213545322418213
            },
            "sarcasm": null,
            "comments": 10
        }
    ],
    "count": 1
}
```
### Статьи
- [Как использовать BERT для мультиклассовой классификации текста](https://neurohive.io/ru/tutorial/bert-klassifikacya-teksta/)
- [BERT Fine-Tuning Tutorial with PyTorch](https://mccormickml.com/2019/07/22/BERT-fine-tuning/)
### Датасеты
