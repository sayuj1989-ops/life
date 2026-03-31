const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');

const files = [
  'paper5_draft/sections/01_introduction.md',
  'paper5_draft/sections/02_background_dgg.md',
  'paper5_draft/sections/02b_background_fep.md',
  'paper5_draft/sections/03_theory_derivation.md',
  'paper5_draft/sections/03b_theory_landscape.md',
  'paper5_draft/sections/04_results.md',
  'paper5_draft/sections/05_discussion_clinical.md',
  'paper5_draft/sections/05b_discussion_consciousness.md'
];

let fullText = "";
files.forEach(file => {
  fullText += fs.readFileSync(file, 'utf8') + "\n\n";
});

const paragraphs = fullText.split('\n').map(line => {
  if (line.startsWith('# ')) {
    return new Paragraph({
      text: line.replace('# ', ''),
      heading: HeadingLevel.HEADING_1,
    });
  } else if (line.startsWith('## ')) {
    return new Paragraph({
      text: line.replace('## ', ''),
      heading: HeadingLevel.HEADING_2,
    });
  } else if (line.startsWith('### ')) {
    return new Paragraph({
      text: line.replace('### ', ''),
      heading: HeadingLevel.HEADING_3,
    });
  } else if (line.trim() !== '') {
    return new Paragraph({
      children: [new TextRun(line)],
    });
  }
  return null;
}).filter(p => p !== null);

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        text: "The Predictive Processing Bridge: Reframing Adolescent Scoliosis as a Free-Energy Catastrophe",
        heading: HeadingLevel.TITLE,
      }),
      new Paragraph({
        children: [
            new TextRun({
                text: "Author: Sayuj K.S., MD, Independent Researcher",
                bold: true,
            })
        ]
      }),
      ...paragraphs
    ],
  }],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync("predictive_processing_bridge_paper.docx", buffer);
  console.log("Document created successfully");
});
