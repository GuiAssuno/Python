import wikipedia
wikipedia.set_lang("pt")

def pesquisar_wikipedia(termo):
    try:
        resumo = wikipedia.summary(termo, sentences=2)
        return resumo
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Encontrei várias opções para {termo}. Poderia ser mais específico?"
    except wikipedia.exceptions.PageError:
        return f"Desculpe, não encontrei informações sobre {termo} na Wikipedia."
    except Exception as e:
        return "Desculpe, tive um problema ao pesquisar na Wikipedia."