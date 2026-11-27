"""Cosméticos e carteira persistente, independentes do placar e do recorde."""
import json
import os
from pathlib import Path
import tempfile


INSPETORES = (
    {"id": "padrao", "nome": "Original", "preco": 0, "cor": None},
    {"id": "petroleo", "nome": "Petróleo", "preco": 100, "cor": (35, 94, 100)},
    {"id": "violeta", "nome": "Violeta", "preco": 200, "cor": (91, 57, 121)},
    {"id": "aco", "nome": "Aço", "preco": 300, "cor": (103, 117, 132)},
)


def perfil_novo():
    return {"saldo": 0, "comprados": ["padrao"], "equipado": "padrao"}


def carregar_perfil(caminho):
    """Arquivo ausente, ilegível ou com esquema inválido usa o padrão gratuito."""
    try:
        dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
        ids = {item["id"] for item in INSPETORES}
        if not isinstance(dados, dict):
            return perfil_novo()
        saldo, comprados = dados.get("saldo"), dados.get("comprados")
        if (type(saldo) is not int or saldo < 0 or not isinstance(comprados, list)
                or any(not isinstance(item, str) for item in comprados)):
            return perfil_novo()
        comprados = [item["id"] for item in INSPETORES
                     if item["id"] in comprados or item["id"] == "padrao"]
        equipado = dados.get("equipado")
        if not isinstance(equipado, str) or equipado not in ids or equipado not in comprados:
            equipado = "padrao"
        return {"saldo": saldo, "comprados": comprados, "equipado": equipado}
    except (OSError, ValueError, UnicodeError):
        return perfil_novo()


def salvar_perfil(caminho, perfil):
    """Troca atômica evita deixar meio JSON se a gravação for interrompida."""
    temporario = None
    try:
        caminho = Path(caminho)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=caminho.parent,
                                         prefix=".inspetores-", suffix=".tmp", delete=False) as arquivo:
            temporario = Path(arquivo.name)
            json.dump(perfil, arquivo, ensure_ascii=False, indent=2)
            arquivo.write("\n")
        os.replace(temporario, caminho)
        return True
    except OSError:
        return False
    finally:
        if temporario is not None:
            try:
                temporario.unlink(missing_ok=True)
            except OSError:
                pass


def persistir_carteira(estado):
    caminho = estado.get("caminho_perfil")
    salvo = caminho is not None and salvar_perfil(caminho, estado["perfil"])
    estado["aviso_carteira"] = "" if salvo else "Saldo em memória: não foi possível salvar a carteira."
    return salvo


def creditar_acerto(estado, pontos):
    estado["perfil"]["saldo"] += pontos
    persistir_carteira(estado)


def abrir_loja(estado):
    estado["fase"] = "loja"
    estado["loja_selecao"] = next(i for i, item in enumerate(INSPETORES)
                                  if item["id"] == estado["perfil"]["equipado"])
    estado["loja_mensagem"] = "Escolha uma aparência. Enter compra e equipa."


def comprar_ou_equipar(estado):
    item = INSPETORES[estado.get("loja_selecao", 0)]
    perfil = estado["perfil"]
    if perfil["equipado"] == item["id"]:
        estado["loja_mensagem"] = "Esta aparência já está equipada."
        return
    comprando = item["id"] not in perfil["comprados"]
    if comprando and perfil["saldo"] < item["preco"]:
        estado["loja_mensagem"] = f"Saldo insuficiente: faltam {item['preco'] - perfil['saldo']} pontos."
        return
    novo = {"saldo": perfil["saldo"] - (item["preco"] if comprando else 0),
            "comprados": perfil["comprados"] + ([item["id"]] if comprando else []),
            "equipado": item["id"]}
    caminho = estado.get("caminho_perfil")
    if caminho is None or not salvar_perfil(caminho, novo):
        estado["loja_mensagem"] = "Não foi possível salvar. Tente novamente; saldo preservado."
        return
    estado["perfil"] = novo
    estado["aviso_carteira"] = ""
    acao = "comprado e equipado" if comprando else "equipado"
    estado["loja_mensagem"] = f"Inspetor {item['nome']} {acao}!"
