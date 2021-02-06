from pathlib import Path
import regex

def removerPalavras(name):
    text = "C:\\Users\\laraf\\PycharmProjects\\TestGUETOS\\src\\Juridico_limpo\\"+name
    try:
        content = open(text, encoding='utf-8')
    except UnicodeDecodeError:
        content = open(text, encoding='cp1252')
    lines = content.readlines()
    file_return = ""
    for line in lines:

        if "Referências " in line or "Ver também" in line or "Bibliografia" in line \
                or "Ligações externas" in line or "Notas" in line:
            return file_return
        else:
            file_return += line

def limpezaDosDados(content, name):
    # Substituir hífens, desde que não estejam entre palavras e caracteres especiais
    #content = regex.sub(r'[!-,.:-@\p{Ps}\p{Pe}]|(?<![a-z])-|-(?![a-z])', '', content)

    # Substituir o caractere =
    #content = regex.sub('=', '', content)

    # Escrevendo de novo o arquivo
    content = removerPalavras(name)
    if content is not None:
        new_file = Path("Juridico_limpo", name)
        new_file.write_text(content, encoding='utf-8')

def main():
    for path_files in Path("Juridico_limpo").glob("*.txt"):
        try:
            content = path_files.read_text(encoding="utf-8")
            limpezaDosDados(content, path_files.name)
        except UnicodeDecodeError:
            content = path_files.read_text(encoding="latin-1")
            limpezaDosDados(content, path_files.name)


main()