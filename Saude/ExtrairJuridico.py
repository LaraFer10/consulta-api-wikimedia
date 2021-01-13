import requests

def main():

    #Categorias: Direito, Saude
    request = requests.Session()

    endpoint = "https://pt.wikipedia.org/w/api.php"

    param_titles = {
        "action": "query",
        "cmtitle": "Category:Saúde",
        "list": "categorymembers",
        "format": "json",
        "prop":"extracts"
    }

    response = request.get(url=endpoint, params=param_titles)
    data = response.json()

    pages = data['query']['categorymembers']

    for page in pages:
        parametros_info = {
            'action': 'query',
            'format': 'json',
            'titles': page['title'],
            'prop': 'extracts',
            'explaintext': True
        }

        response = requests.get(
            url=endpoint,
            params=parametros_info
        ).json()

        page_extract = next(iter(response['query']['pages'].values()))
        arquivo = open(page['title']+'.txt', 'w+')
        arquivo.writelines(page_extract['extract'])
        arquivo.close()


main()
