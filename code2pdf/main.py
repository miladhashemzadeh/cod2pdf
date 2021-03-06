from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as c
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class PdfMaker:

    def __init__(self, extensions, *, lines=70, output=None, fontSize=8, path=None):
        self.lines = lines
        self.extensions = extensions
        self.fontSize = fontSize
        self.pathOfSource = path
        if output is not None or output != "":
            self.canvas = c.Canvas(self.pathOfSource + ".pdf", pagesize=A4)
        else:
            self.canvas = c.Canvas(output + "book_of_code.pdf", pagesize=A4)
        self.w, self.h = A4
        self.lFiles = list()  # [] extensions
        self.dFiles = dict()  # {} file names : content
        pdfmetrics.registerFont(TTFont('source', 'source-code-pro.light.ttf'))
        self._installTreeAndIndexPage()
        self._searchForFiles(extensions)
        self._addFile()
        self._commit()

    def _searchForFiles(self, exts):
        from pathlib import Path
        tmpexts = []
        for ext in exts:
            tmpalph = '*.'
            for a in ext:
                if a.islower():
                    tmpalph += '[%s%s]' % (a, a.upper())
                else:
                    tmpalph += '[%s%s]' % (a.lower(), a)
            tmpexts.append(tmpalph)
        for tmpext in tmpexts:
            for f in Path(self.pathOfSource).rglob(tmpext):
                self.lFiles.append(f)

    def _addFile(self):
        for fn in self.lFiles:  # fn = file name
            file = open(fn, "+r", encoding="utf8")
            content = self.canvas.beginText(0, self.h - 30)
            self.dFiles[str(fn)] = content
            self.makeContent(content, fn)
            cc = 0  # lines per page
            file_read_split = file.read().split("\n")
            for line in file_read_split:
                if cc == self.lines:
                    self.canvas.drawText(content)
                    self.canvas.showPage()
                    content = self.canvas.beginText(0, self.h - 30)
                    self.makeContent(content, fn)
                    cc = 0
                content.textLine(line)
                cc += 1
            file.close()
            content.textLine('')
            content.textLine('')
            self.canvas.drawText(content)
            self.canvas.showPage()

    def makeContent(self, content, fn):
        content.setFont('source', self.fontSize)
        content.textLine(str(fn).split('/')[0])
        content.textLine('')
        content.textLine('')

    def _commit(self):
        self.canvas.save()

    def _installTreeAndIndexPage(self):
        from sys import platform as _platform
        import re
        import subprocess
        instracture = ""
        if _platform == "linux" or _platform == "linux2":
            dist = _platform.linux_distribution()[0]
            if re.match('RHEL', dist, re.IGNORECASE) is not None and re.match('CentOS', dist,
                                                                              re.IGNORECASE) is not None and re.match(
                'Fedora', dist, re.IGNORECASE) is not None:
                instracture = "yum install tree -y"
            elif re.match('Debian', dist, re.IGNORECASE) is not None and re.match('Ubuntu', dist,
                                                                                  re.IGNORECASE) is not None and \
                    re.match('Mint', dist, re.IGNORECASE) is not None:
                instracture = "sudo  apt - get install tree - y"
            else:
                pass  # ???
        elif _platform == "darwin":
            instracture = "brew install tree"
        elif _platform == "win32" or _platform == "win64":
            self._start(stdout=str(subprocess.run(["tree", self.pathOfSource], capture_output=True, shell=True).stdout.decode('cp866', errors='replace')))
        if instracture != "":
            sp = subprocess.run(instracture.split(" "), capture_output=True, shell=True)
            if sp.returncode == 0:
                self._start(stdout=str(subprocess.run(["tree", self.pathOfSource], capture_output=True, shell=True).stdout.decode('cp866', errors='replace')))
            else:
                print("this tool wont make indexPage on your machine!!")

    def _start(self, *, stdout=""):
        tree = stdout.split("\n")[2:]
        content = self.canvas.beginText(0, self.h - 30)
        cc = 0
        self.makeContent(content, fn="index page/index page")
        for line in tree:
            if cc == self.lines:
                self.canvas.drawText(content)
                self.canvas.showPage()
                content = self.canvas.beginText(0, self.h - 30)
                self.makeContent(content, fn="index page/index page")
                cc = 0
            content.textLine(line)
            cc += 1
        content.textLine('')
        content.textLine('')
        self.canvas.drawText(content)
        self.canvas.showPage()


if __name__ == "__main__":
    pathOfSource = "D:/dwonloads/project/open source projects/Timber-master/app/src/main/java"
    PdfMaker(['java', 'h', 'c', 'cpp', 'hpp'], path=pathOfSource)
