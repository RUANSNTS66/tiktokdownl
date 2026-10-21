"""
Baixador de vídeos do TikTok em HD
------------------------------------
Como usar:
    1. Instale o yt-dlp (só precisa fazer isso uma vez):
         pip install -U yt-dlp

    2. Rode o script:
         python baixar_tiktok.py

    3. Cole o link do TikTok quando for pedido.
    4. Informe a pasta onde quer salvar (ou deixe em branco para salvar
       na pasta "Downloads" do usuário).

O script baixa sempre a melhor qualidade de vídeo + áudio disponível
e já junta tudo em um único arquivo .mp4.
"""

import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("O pacote 'yt-dlp' não está instalado.")
    print("Instale com:  pip install -U yt-dlp")
    sys.exit(1)


def pasta_padrao() -> Path:
    """Retorna a pasta Downloads do usuário como sugestão padrão."""
    return Path.home() / "Downloads"


def escolher_pasta() -> Path:
    sugestao = pasta_padrao()
    entrada = input(
        f"Pasta para salvar o vídeo [Enter para usar: {sugestao}]: "
    ).strip()

    pasta = Path(entrada) if entrada else sugestao
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def baixar_video(link: str, pasta_destino: Path) -> None:
    modelo_nome = str(pasta_destino / "%(title).150s.%(ext)s")

    opcoes = {
        # pega o melhor vídeo + melhor áudio disponíveis (HD) e junta em mp4
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "outtmpl": modelo_nome,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        print("\nBaixando... isso pode levar alguns segundos.\n")
        ydl.download([link])

    print(f"\n✅ Download concluído! Arquivo salvo em: {pasta_destino}\n")


def main():
    print("=== Baixador de vídeos do TikTok em HD ===\n")

    link = input("Cole o link do vídeo do TikTok: ").strip()
    if not link:
        print("Nenhum link informado. Encerrando.")
        return

    pasta_destino = escolher_pasta()

    try:
        baixar_video(link, pasta_destino)
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Erro ao baixar o vídeo: {e}")
        print("Verifique se o link está correto e se o vídeo é público.")


if __name__ == "__main__":
    main()
