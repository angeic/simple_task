urls = [
'https://www.amazon.cn/s/ref=sr_pg_','?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143428071&ie=UTF8&qid=1488279084&page=,',
'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143428071&ie=UTF8&qid=1488279084&page=187',
'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143428071&ie=UTF8&qid=1488279084&page=191',
'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143428071&ie=UTF8&qid=1488279084&page=192',
'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143428071&ie=UTF8&qid=1488279084&page=195',
'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143428071&ie=UTF8&qid=1488279084&page=196']


def get_url(url_resouce,p=1):
    url = url_resouce
    url_list = []
    if isinstance(url, (list, tuple, set)):
        url_list = url
    elif isinstance(url, str):
        for k in range(1, p+1):
            urls = 'https://www.amazon.cn/s/ref=sr_pg_'+str(k)+url + str(k)
            url_list.append(urls)
    else:
        # logs('URL错误\n程序终止')
        a = 1

    return url_list

a=get_url('?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071%2Cn%3A143428071&ie=UTF8&qid=1488279084&page=,',10)
print(a)
