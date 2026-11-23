import pytest
from src.dados import carregar_recorde, salvar_recorde


def test_recorde_ausente(tmp_path):
    assert carregar_recorde(tmp_path / "recorde.txt") == 0


@pytest.mark.parametrize("conteudo", [b"", b"  ", b"abc", b"12.5", b"-10", b"10\n20", b"\xff"])
def test_recorde_invalido(tmp_path, conteudo):
    arquivo = tmp_path / "recorde.txt"
    arquivo.write_bytes(conteudo)
    assert carregar_recorde(arquivo) == 0
    assert arquivo.read_bytes() == conteudo


def test_gravar_e_ler_recorde(tmp_path):
    arquivo = tmp_path / "recorde.txt"
    salvar_recorde(arquivo, 70)
    assert carregar_recorde(arquivo) == 70
    salvar_recorde(arquivo, 100)
    assert carregar_recorde(arquivo) == 100
    arquivo.write_text(" 80\n", encoding="utf-8")
    assert carregar_recorde(arquivo) == 80
