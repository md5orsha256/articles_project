def article_validate(title, content, author):
    errors = {}
    if not title:
        errors['title'] = "Поле title обязательно для заполнения"
    elif len(title) > 200:
        errors['title'] = "Длина этого поля должна быть меньше 200"
    if not content:
        errors['content'] = "Поле content обязательно для заполнения"
    elif len(content) > 2000:
        errors['content'] = "Длина этого поля должна быть меньше 2000"
    if not author:
        errors['author'] = "Поле author обязательно для заполнения"
    elif len(author) > 200:
        errors['author'] = "Длина этого поля должна быть меньше 200"
    return errors
