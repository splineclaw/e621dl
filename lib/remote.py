from . import local, constants
import os

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

def get_known_post(id, session):
    url = 'https://e621.net/post/show.json?id=' + id

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
    raise SystemExit

def download_post(url, path, session):
    temp_path = path + '.' + constants.PARTIAL_DOWNLOAD_EXT

    with open(temp_path, 'wb') as outfile:
        for chunk in session.get(url, stream = True).iter_content(chunk_size = constants.REQUEST_CHUNK_SIZE):
            outfile.write(chunk)
    os.rename(temp_path, path)

def finish_partial_downloads(session):
    for root, dirs, files in os.walk('downloads/'):
        for file in files:
            if file.endswith(constants.PARTIAL_DOWNLOAD_EXT):
                local.print_log('remote', 'info', 'Partial download found: ' + file + '. Finishing download.')

                path = os.path.join(root, file)

                with open(path, 'ab') as outfile:
                    header = {'Range':'bytes=' + str(os.path.getsize(path)) + '-'}
                    url = get_known_post(file.split('.')[0], session)['file_url']

                    for chunk in session.get(url, stream = True, headers = header).iter_content(chunk_size = constants.REQUEST_CHUNK_SIZE):
                        outfile.write(chunk)
                os.rename(path, path.replace('.' + constants.PARTIAL_DOWNLOAD_EXT, ''))
