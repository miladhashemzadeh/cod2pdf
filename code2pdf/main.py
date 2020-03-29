from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as c


class PdfMaker:

    def __init__(self, extensions, *, output=None, fontSize=8, path=None):
        self.extensions = extensions
        self.fontSize = fontSize
        self.pathOfSource = path
        if output is not None or output != "":
            self.canvas = c.Canvas(self.pathOfSource + "book_of_code.pdf", pagesize=A4)
        else:
            self.canvas = c.Canvas(output + "book_of_code.pdf", pagesize=A4)
        self.w, self.h = A4
        self.lFiles = list()  # [] extensions
        self.dFiles = dict()  # {} file names : content
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
            file = open(fn, "+r")
            content = self.canvas.beginText(0, self.h - 30)
            self.dFiles[str(fn)] = content
            content.setFont("Courier", self.fontSize)
            content.textLine(str(fn).split('/')[0])
            content.textLine('')
            content.textLine('')
            for line in file.read().split("\n"):
                content.textLine(line)
            self.canvas.drawText(content)
            file.close()
            self.canvas.showPage()

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
                                                                                  re.IGNORECASE) is not None and re.match(
                'Mint', dist, re.IGNORECASE) is not None:
                instracture = "sudo  apt - get install tree - y"
            else:
                pass  # ???
        elif _platform == "darwin":
            instracture = "brew install tree"
        elif _platform == "win32" or _platform == "win64":
            pass
        if instracture != "":
            sp = subprocess.run(instracture.split(" "))
            if sp.returncode == 0:
                self._start(stdout=subprocess.run(["tree", self.pathOfSource]).stdout)
            else:
                print("this tool wont make indexPage on your machine!!")

    def _start(self, extensions, *, stdout=None):
        pass


if __name__ == "__main__":
    pathOfSource = "D:/jabjaee/app/src/"
    PdfMaker(['java', 'class'], path=pathOfSource)
