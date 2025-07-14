from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Unicode fonts that support many language characters.
# Adjust the paths to point to your installed font files.
pdfmetrics.registerFont(TTFont('NotoSans', '/home/deen/.local/share/fonts/RobotoMonoNerdFontMono-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSans-Bold', '/home/deen/.local/share/fonts/RobotoMonoNerdFontMono-Bold.ttf'))

def generate_pdf(file1, file2, output_pdf):
    # Read text files, split into non-empty lines
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        lines1 = [line.strip() for line in f1 if line.strip()]
        lines2 = [line.strip() for line in f2 if line.strip()]
    
    # Create a document template with margins so text is confined within the page
    doc = SimpleDocTemplate(output_pdf, pagesize=letter,
                            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    
    # Define styles for each type of line
    style1 = ParagraphStyle(
        'Style1',
        fontName='NotoSans-Bold',
        fontSize=14,
        textColor=colors.green,
        spaceAfter=6
    )
    style2 = ParagraphStyle(
        'Style2',
        fontName='NotoSans',
        fontSize=12,
        textColor=colors.grey,
        spaceAfter=6
    )
    
    story = []
    max_lines = max(len(lines1), len(lines2))
    
    # For each index, add one line from file1 and one line from file2 if available.
    for i in range(max_lines):
        if i < len(lines1):
            para = Paragraph(lines1[i], style1)
            story.append(para)
        if i < len(lines2):
            para = Paragraph(lines2[i], style2)
            story.append(para)
        # Add some space between each pair
        story.append(Spacer(1, 12))
    
    # Build the PDF (this method handles text wrapping automatically)
    doc.build(story)
    print(f"PDF '{output_pdf}' generated successfully!")

# Example usage
generate_pdf("20%yor_nolines.txt", "20%yor_nolines.yo.en.txt", "CombinedYoruba.pdf")
