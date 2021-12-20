import sys
import zipfile
import xml.dom.minidom as minidom
from opencc import OpenCC

def epub_ct_convert(fileName, mode):
    cc = OpenCC(mode)
    z = zipfile.ZipFile(fileName)
    nz = zipfile.ZipFile(fileName.rstrip('.epub') + mode + '.epub', 'w', zipfile.ZIP_DEFLATED)
    ct = z.read('META-INF/container.xml')
    dom = minidom.parseString(ct)
    fullPath = dom.getElementsByTagName('rootfile')[0].getAttribute('full-path')
    dire = fullPath[:fullPath.find('/') + 1]
    fb = z.read(fullPath)
    dom = minidom.parseString(fb)

    fileList = []
    for e in dom.getElementsByTagName('item'):
        if e.getAttribute("href").endswith('html'):
            fileList.append(e.getAttribute("href"))

    originFileList = []
    for f in z.filelist:
        if not f.filename.endswith('html'):
            originFileList.append(f.filename)
    for n in originFileList:
        file = z.read(n)
        nz.writestr(n, file)

    for f in fileList:
        article = z.read(dire + f).decode()
        converted = cc.convert(article)
        nz.writestr(dire + f, converted)

    z.close()
    nz.close()

def main():
    if len(sys.argv) == 1:
        print ('epubTCSC, coded by xuyiyang')
        print ('usage: epubTCSC.py <t2s/s2t> <*.epub>')
        return
    mode = sys.argv[1]
    files = sys.argv[2:]
    for f in files:
        epub_ct_convert(f[f.rindex('/') + 1:], mode)

if __name__ == '__main__':
    main()
