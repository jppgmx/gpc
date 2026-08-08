from markdownify import MarkdownConverter

class PrivacyNormalizer(MarkdownConverter):
    def convert_h2(self, el, text, parent_tags):
        return f"\n\n# {text}\n\n"

    def convert_h3(self, el, text, parent_tags):
        return f"\n\n## {text}\n\n"

    def convert_h4(self, el, text, parent_tags):
        return f"\n\n### {text}\n\n"

    def convert_h5(self, el, text, parent_tags):
        return f"\n\n#### {text}\n\n"

    def convert_h6(self, el, text, parent_tags):
        return f"\n\n##### {text}\n\n"
