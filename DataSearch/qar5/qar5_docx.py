# qar5_docx.py (qar5)
# !/usr/bin/env python3
# coding=utf-8
# young.daniel@epa.gov

"""Definition of qar5 docx export methods."""

from docx import Document
from docx.enum.style import WD_BUILTIN_STYLE, WD_STYLE_TYPE
from docx.enum.text import WD_COLOR_INDEX, WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches
from os import path
# import pypandoc
# import tempfile
# from zipfile import ZipFile
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static
from DataSearch.settings import DEBUG, STATIC_ROOT
from qar5.views import get_all_qar5_for_user, get_qapp_info

def export_doc(request, *args, **kwargs):
    """Function to export QAR5 as a Word Document."""
    qapp_id = kwargs.get('pk', None) 
    template_name = 'export/qar5_pdf_template.html'

    if qapp_id is None:
        # TODO: Export ALL QAR5 objects available for this user to Docx.
        qapp_info = get_all_qar5_for_user(request.user)

    else:
        qapp_info = get_qapp_info(request.user, qapp_id)
        if not qapp_info:
            return

        filename = '%s.docx' % qapp_info['qapp'].title

        document = Document()
        styles = document.styles
        
        # #################################################
        # BEGIN COVER PAGE
        # #################################################
        # Coversheet with signatures section:
        # 1) row has WD_ALIGN_PARAGRAPH.LEFT aligned EPA logo.
        if DEBUG:
            logo = path.join(STATIC_ROOT, 'EPA_Files', 'logo.png')
        else:
            logo = static('logo.png')

        document.add_picture(logo, width=Inches(1.25))

        # 2) row has right-aligned box "Quality Assurance Project Plan"
        # Align the picture/text WD_ALIGN_PARAGRAPH.RIGHT
        blue_header_style = document.styles.add_style(
            'blue_header', WD_STYLE_TYPE.PARAGRAPH).paragraph_format
        blue_header_style.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        blue_header = document.add_heading('Quality Assurance Project Plan',
                                           level=1)

        style_center = document.styles.add_style(
            'center_text', WD_STYLE_TYPE.PARAGRAPH).paragraph_format
        style_center.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # TODO Make blue_header text white, add blue background with shadow
        # document.add_picture('blue_background.png', width=Inches(4))
        # background color: rgb(0, 176, 240)

        # The rest of the document will be WD_ALIGN_PARAGRAPH.CENTER

        # blank line
        # 1)  Heading 1 - Office of Research and Development
        document.add_heading('Office of Research and Development', level=1)
        # 2)  Heading 2 - Center for Environmental Solutions & Emergency Response
        document.add_heading(qapp_info['qapp'].division.name, level=1)
        # blank line
        # Next few sections are from the qapp object
        # 3)  Heading 3 - Division Branch
        document.add_heading(qapp_info['qapp'].division_branch, level=3)
        # blank line
        # 4)  Heading 2 - EPA Project Lead
        document.add_heading('EPA Project Lead', level=2)
        for lead in qapp_info['qapp_leads']:
            #     4.n) Heading 3 - NAME ...
            document.add_heading(lead.name, level=3)
        # blank line
        # 5)  Heading 3 - Extramural
        document.add_heading(qapp_info['qapp'].intra_extra, level=3)
        # 6)  Heading 3 - Category
        document.add_heading(qapp_info['qapp'].qa_category, level=3)
        # 7)  Heading 3 - Revision Number
        document.add_heading(qapp_info['qapp'].revision_number, level=3)
        # 8)  Heading 3 - Date
        document.add_heading(str(qapp_info['qapp'].date), level=3)
        # blank line
        # 9) Heading 2 - Prepared By
        document.add_heading('Prepared By', level=2)
        # 10) Heading 3 - NAME
        document.add_heading(
            '%s %s' % (qapp_info['qapp'].prepared_by.first_name,
                       qapp_info['qapp'].prepared_by.last_name,),
            level=3)
        # blank line
        # 11) Heading 3 - STRAP
        document.add_heading(qapp_info['qapp'].strap, level=3)
        # 12) Heading 3 - TRACKING ID
        document.add_heading(qapp_info['qapp'].tracking_id, level=3)
        # #################################################
        # END COVER PAGE
        # BEGIN APPROVAL PAGE
        # #################################################
        # 13) Heading 2 - Approval Page
        document.add_heading('Approval Page', level=2)
        # 14) Create a grid ...
        num_signatures = len(qapp_info['signatures'])
        table = document.add_table(rows=6+num_signatures, cols=12)
        table.style = styles['Table Grid']

        row_cells = table.rows[0].cells
        row_cells[0].text = 'QA Project Plan Title:'
        row_cells[0].merge(row_cells[3])
        row_cells[4].text = qapp_info['qapp_approval'].project_plan_title
        row_cells[4].merge(row_cells[11])

        row_cells = table.rows[1].cells
        row_cells[0].text = 'QA Activity Number:'
        row_cells[0].merge(row_cells[3])
        row_cells[4].text = qapp_info['qapp_approval'].activity_number
        row_cells[4].merge(row_cells[11])

        # TODO: Center text in this row:
        row_cells = table.rows[2].cells
        row_cells[0].text = 'If Intramural or Extramural, EPA Project Approvals'
        row_cells[0].merge(row_cells[11])

        iter_count = 0
        # TODO: Iterate through EPA Project Approvals:
        # Start with row 3 + iter_count++
        for sig in qapp_info['signatures']:
            if not sig.contractor:
                row_cells = table.rows[3 + iter_count].cells
                row_cells[0].text = 'Name:'
                row_cells[1].text = sig.name
                row_cells[1].merge(row_cells[3])

                row_cells[4].text = 'Signature/Date:'
                row_cells[4].merge(row_cells[5])
                row_cells[6].merge(row_cells[11])
                iter_count += 1

        # Always insert a blank entry for hand-written approval sigs
        row_cells = table.rows[3 + iter_count].cells
        row_cells[0].text = 'Name:'
        row_cells[1].merge(row_cells[3])
        row_cells[4].text = 'Signature/Date:'
        row_cells[4].merge(row_cells[5])
        row_cells[6].merge(row_cells[11])

        # TODO: Center text in this row:
        row_cells = table.rows[4 + iter_count].cells
        row_cells[0].text = 'If Extramural, Contractor Project Approvals'
        row_cells[0].merge(row_cells[11])

        # TODO: Iterate through Contractor Project Approvals:
        # Start with row 5 + iter_count++
        for sig in qapp_info['signatures']:
            if sig.contractor:
                row_cells = table.rows[5 + iter_count].cells
                row_cells[0].text = 'Name:'
                row_cells[1].text = sig.name
                row_cells[1].merge(row_cells[3])

                row_cells[4].text = 'Signature/Date:'
                row_cells[4].merge(row_cells[5])
                row_cells[6].merge(row_cells[11])
                iter_count += 1

        # Always insert a blank entry for hand-written approval sigs
        row_cells = table.rows[5 + iter_count].cells
        row_cells[0].text = 'Name:'
        row_cells[1].merge(row_cells[3])
        row_cells[4].text = 'Signature/Date:'
        row_cells[4].merge(row_cells[5])
        row_cells[6].merge(row_cells[11])

        # #################################################
        # END APPROVAL PAGE
        # BEGIN ...... PAGE
        # #################################################


        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.' + \
                'wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        document.save(response)
        #document.save('test_export.docx')
        return response

    return