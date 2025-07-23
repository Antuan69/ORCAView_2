from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatter import Formatter

class PygmentsFormatter(Formatter):
    def __init__(self):
        super().__init__()
        self.data = []

    def format(self, tokensource, outfile):
        self.data = []
        for ttype, value in tokensource:
            self.data.append((ttype, value))

class OrcaSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.formatter = PygmentsFormatter()
        self.lexer = get_lexer_by_name('bash') # Using Bash lexer as a base for ORCA

    def highlightBlock(self, text):
        cb = self.currentBlock()
        p = cb.position()

        highlight(text, self.lexer, self.formatter)

        for ttype, value in self.formatter.data:
            length = len(value)
            color = self.color_for_token(ttype)
            if color:
                self.setFormat(p, length, color)
            p += length

    def color_for_token(self, ttype):
        color = QColor()
        if str(ttype) in ('Token.Keyword', 'Token.Keyword.Declaration', 'Token.Keyword.Type'):
            color.setRgb(0, 0, 255)
        elif str(ttype) in ('Token.Name.Function', 'Token.Name.Class'):
            color.setRgb(0, 128, 0)
        elif str(ttype) in ('Token.Comment', 'Token.Comment.Single'):
            color.setRgb(128, 128, 128)
        elif str(ttype) in ('Token.Literal.String', 'Token.Literal.String.Single'):
            color.setRgb(255, 0, 0)
        elif str(ttype) in ('Token.Number', 'Token.Literal.Number.Integer'):
            color.setRgb(255, 165, 0)
        else:
            return None
        
        text_format = QTextCharFormat()
        text_format.setForeground(color)
        return text_format
