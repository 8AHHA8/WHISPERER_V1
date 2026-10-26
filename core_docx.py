import os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def make_docx():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Aptos"
    style.font.size = Pt(12)
    style._element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "Aptos")
    return doc

def save_docx_safely(doc, output_path):
    temp_path = output_path + ".tmp.docx"
    doc.save(temp_path)
    try:
        os.replace(temp_path, output_path)
        return True
    except PermissionError:
        return False