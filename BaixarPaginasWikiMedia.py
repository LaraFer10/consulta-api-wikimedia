import requests

def downloadPage(pages, endpoint):
    titles_not_load = ""
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
        title = page['title']+".txt"
        #Algumas paginas com esses caracteres emitem erro ao serem salvas
        if '/' not in title and '"' in title and '?' in title:
            page_content = page_extract['extract']
            with open(title, "w", encoding="utf-8") as f:
                f.write(page_content)
                f.close()
        else:
            titles_not_load += title + "\n"

    # Salva o titulo das paginas que não consegui baixar
    file_not_load = open("Paginas não baixadas", "w")
    file_not_load.write(titles_not_load)
    file_not_load.close()

def main():

    #Categorias: Direito, Saude ....
    request = requests.Session()

    endpoint = "https://pt.wikipedia.org/w/api.php"
    #Busca o titulo das paginas por categoria(principal)
    param_titles = {
        "action": "query",
        "cmtitle": "Category:Nome da categoria principal",
        "cmlimit": "max",
        "list": "categorymembers",
        "format": "json",
        "prop":"extracts"
    }

    response = request.get(url=endpoint, params=param_titles)
    data = response.json()

    pages = data['query']['categorymembers']


    #Baixa as paginas por titulo
    downloadPage(pages, endpoint)

    #Buscar o titulo das subcategorias da categoria principal
    param_subcategory = {
        "action": "query",
        "cmtitle": "Category:Nome da categoria principal",
        "cmtype": "subcat",
        "list": "categorymembers",
        "format": "json"
    }

    response = request.get(url=endpoint, params=param_subcategory)
    data = response.json()

    pagesSub = data['query']['categorymembers']
    # Baixa as paginas da subcategoria
    for page in pagesSub:
        param_titles = {
            "action": "query",
            "cmtitle": page["title"],
            "cmlimit": "max",
            "list": "categorymembers",
            "format": "json",
            "prop": "extracts"
        }
        response = request.get(url=endpoint, params=param_titles)
        data = response.json()
        pageSub = data['query']['categorymembers']
        downloadPage(pageSub, endpoint)

main()
