# Manipulating PDFs with Python
# https://www.binpress.com/tutorial/manipulating-pdfs-with-python/167

# PyPDF2 Documentation
# https://pythonhosted.org/PyPDF2/index.html

# http://pages.cs.wisc.edu/~ghost/


# https://stackoverflow.com/questions/2002055/converting-pdf-to-images-automatically

# Wand
# https://stackoverflow.com/questions/37299666/python-converting-pdf-to-image

# pip3 install -U wxPython
# pip3 install pypdf2

# https://runcode12.blogspot.com/2010/06/
# http://www.gaptre.com/about.php?t=read_pdf_using_python
# https://automatetheboringstuff.com/chapter13/

# google: pypdf2 in kivy
# https://gist.github.com/splanquart/1358169/c16f3af98a87aec923223558d9c57b52cf523f66
# https://groups.google.com/forum/#!topic/kivy-users/AVcEHqswHA8
# https://github.com/kivy/kivy/issues/213


# In order to display .docx, you would need to learn the file format and write your own loader, or use
# an existing loader. A quick Google search turns up python-docx. Once you've loaded the file, if you
# want it displayed then you will need to write your own code to display it in Kivy, or convert it to a
# format which Kivy already supports, like reStructuredText.

# Similarly, for .pdf, Google finds pyPdf2. Again, you would need to convert it to rST or generate Kivy
# widgets/instructions to display the document yourself.


#!/usr/bin/env python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import StringProperty

class PDFReader(BoxLayout):
    filename = StringProperty('')

    def __init__(self, **kwargs):
        super(PDFReader, self).__init__(**kwargs)
        b = Button(text='<')
        b.size_hint = None, None
        b.size = 100, 100
        b.bind(on_release=self.prececent)
        self.add_widget(b)

        self.pdf = Image(source=self.filename)
        self.add_widget(self.pdf)

        b = Button(text='>')
        b.size_hint = None, None
        b.size = 100, 100
        b.bind(on_release=self.next)
        self.add_widget(b)

    def next(self, *_):
        self.pdf.page += 1

    def prececent(self, *_):
        self.pdf.page -= 1

class MyApp(App):
    def build(self):
        #return PDFReader(filename='evaluation software engeener.pdf')
        #return PDFReader(filename='MachineofDeath_FINAL_SPREADS.pdf')
        import io
        from kivy.core.image import Image as CoreImage
        file = 'rsc/test_file.pdf'
        img = Image(source=file)
        #data = io.BytesIO(open(file, 'rb').read())
        #im = CoreImage(data, ext='pdf', filename=file)
        #return PDFReader(filename=file)
        return img
if __name__ == '__main__':
    MyApp().run()