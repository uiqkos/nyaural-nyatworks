from spacy.tokens import Doc, Token


def init_doc_extensions(extensions):

    for extension in extensions:
        Doc.set_extension(extension)


def init_token_extensions(extensions):
    for extension in extensions:
        Token.set_extension(extension)



