from . import local

def get_github_release(session):
    url = 'https://api.github.com/repos/wulfre/e621dl/releases/latest'
    response = session.get(url).json()
    return response['tag_name'].strip('v')

def get_posts(search_string, min_score, earliest_date, page_number, max_results, session):
    url = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>=' + str(earliest_date) + \
        ' score:>=' + str(min_score) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    return session.get(url).json()

def get_tag_alias(user_tag, session):
    prefix = ''

    if ':' in user_tag:
        return user_tag

    if user_tag[0] == '~':
        prefix = '~'
        user_tag = user_tag[1:]

    if user_tag[0] == '-':
        prefix = '-'
        user_tag = user_tag[1:]

    url = 'https://e621.net/tag/index.json?name=' + user_tag
    response = session.get(url).json()

    if '*' in user_tag and response:
        return user_tag

    for tag in response:
        if user_tag == tag['name']:
            return prefix + user_tag

    url = 'https://e621.net/tag_alias/index.json?query=' + user_tag + '&approved=true'
    response = session.get(url).json()

    for tag in response:
        if user_tag == tag['name']:
            url = 'https://e621.net/tag/show.json?id=' + str(tag['alias_id'])
            response = session.get(url).json()

            local.print_log('remote', 'info', 'Tag aliased: ' + prefix + user_tag + ' -> ' + prefix + response['name'])

            return prefix + response['name']

    local.print_log('remote', 'error', 'The tag ' + prefix + user_tag + ' is spelled incorrectly or does not exist.')
    exit()

def download_post(url, path, session):
    with open(path, 'wb') as outfile:
        for chunk in session.get(url, stream = True).iter_content(chunk_size = 1024):
            outfile.write(chunk)
