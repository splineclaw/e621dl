from . import local

def get_posts(search_string, uploaded_after, page_number, max_results, session, timeout):
    request = 'https://e621.net/post/index.json?' + \
        'tags=' + search_string + \
        ' date:>' + str(uploaded_after) + \
        '&page=' + str(page_number) + \
        '&limit=' + str(max_results)

    local.print_log('remote', 'debug', 'Post request URL: \"' + request + '\".')

    return session.get(request, timeout = timeout).json()

def download_post(url, path, session, timeout):
    with open(path, 'wb') as outfile:
        for chunk in session.get(url, stream = True, timeout = timeout).iter_content(chunk_size = 1024):
            if chunk:
                outfile.write(chunk)
