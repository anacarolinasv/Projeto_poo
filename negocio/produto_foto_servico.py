import base64
from pathlib import Path


class ProdutoFotoServico:
    FOTOS_DIR = Path("produtos/fotos")
    EXTENSOES = ("jpg", "jpeg", "png", "webp")

    def _garantir_dir(self):
        self.FOTOS_DIR.mkdir(parents=True, exist_ok=True)

    def caminho_foto(self, id_produto):
        self._garantir_dir()
        for ext in self.EXTENSOES:
            caminho = self.FOTOS_DIR / f"{id_produto}.{ext}"
            if caminho.exists():
                return caminho
        return None

    def salvar_foto(self, id_produto, arquivo):
        ext = (arquivo.name or "").rsplit(".", 1)[-1].lower()
        if ext not in self.EXTENSOES:
            raise ValueError("Formato inválido. Use JPG, PNG ou WEBP.")
        self._garantir_dir()
        self.excluir_foto(id_produto)
        destino = self.FOTOS_DIR / f"{id_produto}.{ext}"
        destino.write_bytes(arquivo.getvalue())

    def excluir_foto(self, id_produto):
        self._garantir_dir()
        for caminho in self.FOTOS_DIR.glob(f"{id_produto}.*"):
            caminho.unlink()

    def html_imagem(self, id_produto, fallback):
        foto = self.caminho_foto(id_produto)
        if not foto:
            return fallback
        ext = foto.suffix.lstrip(".").lower()
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}.get(ext, "jpeg")
        b64 = base64.b64encode(foto.read_bytes()).decode()
        return (
            f'<img class="loja-produto-foto" src="data:image/{mime};base64,{b64}" '
            f'alt="Foto do produto" />'
        )
