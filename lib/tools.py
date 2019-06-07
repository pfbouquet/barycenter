
def get_database_uri(**params):
    return '{type}://{user}:{password}@{host}:{port}/{db}'.format(**params)
