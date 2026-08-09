"""
    Módulo do conversor utilitário para normalizar a Política de Privacidade em Markdown
"""

from markdownify import MarkdownConverter

# Suprimir os avisos abaixo, pois não usamos todos os parâmetros,
# mas eles são necessários para a assinatura do método.
# pylint: disable=unused-argument
class PrivacyNormalizer(MarkdownConverter):
    """
        Conversor utilitário para tentar normalizar a Política de Privacidade
        do Codeforces em Markdown.
    """
    def convert_h2(self, el, text, parent_tags):
        """Normaliza <h2> para <h1>"""
        return f"\n\n# {text}\n\n"

    def convert_h3(self, el, text, parent_tags):
        """Normaliza <h3> para <h2>"""
        return f"\n\n## {text}\n\n"

    def convert_h4(self, el, text, parent_tags):
        """Normaliza <h4> para <h3>"""
        return f"\n\n### {text}\n\n"

    def convert_h5(self, el, text, parent_tags):
        """Normaliza <h5> para <h4>"""
        return f"\n\n#### {text}\n\n"

    def convert_h6(self, el, text, parent_tags):
        """Normaliza <h6> para <h5>"""
        return f"\n\n##### {text}\n\n"
