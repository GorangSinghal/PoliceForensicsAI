import os
import zipfile
import xml.etree.ElementTree as ET

def create_docx(filename, title, sections):
    """
    Creates a professionally styled .docx file using standard library zipfile and OpenXML.
    sections is a list of tuples:
      ('heading1', text)
      ('heading2', text)
      ('heading3', text)
      ('paragraph', text)
      ('bullet', text, bold_prefix)
      ('contact', text)
      ('subtitle', text)
    """
    
    # 1. [Content_Types].xml
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

    # 2. _rels/.rels
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

    # 3. word/_rels/document.xml.rels
    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    # 4. word/styles.xml
    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
        <w:sz w:val="21"/> <!-- 10.5 pt -->
        <w:color w:val="222222"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:spacing w:line="276" w:lineRule="auto" w:before="60" w:after="60"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
</w:styles>"""

    # 5. Build word/document.xml body
    doc_elements = []
    
    # Title / Header
    for item in sections:
        itype = item[0]
        
        if itype == 'title':
            text = item[1]
            p = f"""<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="120" w:after="40"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
      <w:b/>
      <w:sz w:val="44"/> <!-- 22 pt -->
      <w:color w:val="0F2C59"/>
    </w:rPr>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>
</w:p>"""
            doc_elements.append(p)
            
        elif itype == 'subtitle':
            text = item[1]
            p = f"""<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="0" w:after="80"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:b/>
      <w:sz w:val="24"/> <!-- 12 pt -->
      <w:color w:val="205295"/>
    </w:rPr>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>
</w:p>"""
            doc_elements.append(p)

        elif itype == 'contact':
            text = item[1]
            p = f"""<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="0" w:after="160"/>
    <w:pBdr>
      <w:bottom w:val="single" w:sz="12" w:space="8" w:color="0F2C59"/>
    </w:pBdr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:sz w:val="20"/> <!-- 10 pt -->
      <w:color w:val="444444"/>
    </w:rPr>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>
</w:p>"""
            doc_elements.append(p)

        elif itype == 'heading1':
            text = item[1]
            p = f"""<w:p>
  <w:pPr>
    <w:spacing w:before="240" w:after="80"/>
    <w:pBdr>
      <w:bottom w:val="single" w:sz="8" w:space="4" w:color="0F2C59"/>
    </w:pBdr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:b/>
      <w:sz w:val="26"/> <!-- 13 pt -->
      <w:color w:val="0F2C59"/>
    </w:rPr>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>
</w:p>"""
            doc_elements.append(p)

        elif itype == 'heading2':
            text = item[1]
            subtext = item[2] if len(item) > 2 else ""
            p = f"""<w:p>
  <w:pPr>
    <w:spacing w:before="140" w:after="40"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:b/>
      <w:sz w:val="22"/> <!-- 11 pt -->
      <w:color w:val="144272"/>
    </w:rPr>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>"""
            if subtext:
                p += f"""
  <w:r>
    <w:rPr>
      <w:i/>
      <w:sz w:val="20"/>
      <w:color w:val="555555"/>
    </w:rPr>
    <w:t> | {escape_xml(subtext)}</w:t>
  </w:r>"""
            p += "\n</w:p>"
            doc_elements.append(p)

        elif itype == 'paragraph':
            text = item[1]
            p = f"""<w:p>
  <w:pPr>
    <w:spacing w:before="40" w:after="80" w:line="260" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>
</w:p>"""
            doc_elements.append(p)

        elif itype == 'bullet':
            text = item[1]
            bold_prefix = item[2] if len(item) > 2 else ""
            p = f"""<w:p>
  <w:pPr>
    <w:ind w:left="360" w:hanging="240"/>
    <w:spacing w:before="30" w:after="40" w:line="260" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/>
      <w:color w:val="0F2C59"/>
    </w:rPr>
    <w:t>• </w:t>
  </w:r>"""
            if bold_prefix:
                p += f"""
  <w:r>
    <w:rPr>
      <w:b/>
      <w:color w:val="111111"/>
    </w:rPr>
    <w:t>{escape_xml(bold_prefix)}: </w:t>
  </w:r>"""
            p += f"""
  <w:r>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>
</w:p>"""
            doc_elements.append(p)

        elif itype == 'quote':
            text = item[1]
            p = f"""<w:p>
  <w:pPr>
    <w:ind w:left="400" w:right="400"/>
    <w:spacing w:before="80" w:after="100"/>
    <w:pBdr>
      <w:left w:val="single" w:sz="18" w:space="12" w:color="0F2C59"/>
    </w:pBdr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:i/>
      <w:sz w:val="21"/>
      <w:color w:val="333333"/>
    </w:rPr>
    <w:t>{escape_xml(text)}</w:t>
  </w:r>
</w:p>"""
            doc_elements.append(p)

    body_content = "\n".join(doc_elements)
    
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
{body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/> <!-- Letter size: 8.5 x 11 in -->
      <w:pgMar w:top="864" w:right="864" w:bottom="864" w:left="864" w:header="720" w:footer="720" w:gutter="0"/> <!-- 0.6 in margins -->
    </w:sectPr>
  </w:body>
</w:document>"""

    # Assemble Zip
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as docx:
        docx.writestr('[Content_Types].xml', content_types)
        docx.writestr('_rels/.rels', root_rels)
        docx.writestr('word/_rels/document.xml.rels', doc_rels)
        docx.writestr('word/styles.xml', styles_xml)
        docx.writestr('word/document.xml', document_xml)
    print(f"[SUCCESS] Created {filename}")

def escape_xml(s):
    if not s:
        return ""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))

def main():
    workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # ----------------------------------------------------
    # DOCUMENT 1: Gorang Resume Draft (.docx)
    # ----------------------------------------------------
    resume_sections = [
        ('title', 'GORANG SINGHAL'),
        ('subtitle', 'AI & Computer Vision Systems Engineer | Machine Learning Engineer'),
        ('contact', 'gorang.singhal06@gmail.com  •  github.com/GorangSinghal/PoliceForensicsAI  •  linkedin.com/in/gorang-singhal  •  India'),
        
        ('heading1', 'PROFESSIONAL SUMMARY'),
        ('paragraph', 'Impact-driven AI & Computer Vision Systems Engineer specializing in high-throughput document intelligence, deep learning image restoration, and edge-deployed Vision-Language Models. Proven track record architecting hybrid pipelines fusing traditional Computer Vision (OpenCV) with state-of-the-art Generative AI (Gemini 1.5, Llama 3 8B) under strict hardware and air-gapped constraints. Strong focus on deterministic guardrails, zero-PII forensic integrity, tensor-level VRAM optimization, and enterprise MLOps.'),
        
        ('heading1', 'CORE TECHNICAL COMPETENCIES'),
        ('bullet', 'Python (Expert), C++, SQL, JavaScript/TypeScript, PyTorch, TorchVision, OpenCV, NumPy, Pandas, Scipy, Scikit-Learn', 'Languages & Frameworks'),
        ('bullet', 'Vision-Language Models (Gemini 1.5 Flash), Meta Llama 3 (8B), TinyLlama (1B), GGUF Quantization (Q4_K_M), llama-cpp-python, LoRA/QLoRA Fine-Tuning, SpaCy NER, EasyOCR, HuggingFace', 'GenAI & OCR Systems'),
        ('bullet', 'CodeFormer GAN, Real-ESRGAN, Image Restoration, Edge Detection, Adaptive Thresholding, Unsharp Masking, Tensor VRAM Allocation, Generative Smoothing Diagnosis', 'Computer Vision & Deep Learning'),
        ('bullet', 'FastAPI, Gradio, REST APIs, React, Vite, TailwindCSS, Docker, PyInstaller (.exe packaging), Git, GitHub Actions (CI/CD), PyTest, Golden Matrix Evaluation Suite, jiwer (WER calculation)', 'MLOps, Web & Tooling'),
        ('bullet', 'Dynamic Licensing Routing (MIT vs. S-Lab), Zero-Trust Fallback, Air-Gapped Intranet Architecture, Zero PII Logging Compliance, Deterministic Guardrails', 'Architecture & Security'),

        ('heading1', 'FEATURED ENGINEERING PROJECTS'),
        ('heading2', 'PoliceForensicsAI: High-Throughput Evidence & Case File Toolkit', 'Production Open-Source System'),
        ('paragraph', 'End-to-end forensic evidence extraction and restoration system designed for law enforcement precincts to process severely degraded surveillance frames and handwritten crime logs.'),
        ('bullet', 'Architected an end-to-end forensic evidence toolkit fusing OpenCV with modern Vision-Language Models (Gemini 1.5 API) and local Small Language Models (Llama 3 8B via llama-cpp-python) to extract structured schema from heavily degraded police records.', 'Hybrid GenAI Pipeline'),
        ('bullet', 'Engineered a dual-engine OCR pipeline combining EasyOCR structural layout analysis with LLM semantic transcription; built deterministic NLP safeguards (SpaCy NER, custom regex validation, date normalization) to eliminate hallucinations and achieve 100% schema integrity.', 'Deterministic Safeguards'),
        ('bullet', 'Optimized deep learning tensor allocations for PyTorch-based GAN (CodeFormer), overriding default VRAM downsampling limits in source code from 4,000 to 4,000,000 pixels to reconstruct high-resolution evidence locally without Out-of-Memory (OOM) crashes.', 'Tensor Optimization'),
        ('bullet', 'Conducted architectural decision spike on Real-ESRGAN upscaler, empirically diagnosing "Generative Smoothing" phenomenon (23.4% character degradation and plate erasure) to mathematically justify S-Lab CodeFormer licensing routing.', 'Failure Mode Analysis'),
        ('bullet', 'Curated and automated a 100-Case Golden Matrix evaluation suite, validating model accuracy mathematically using Word Error Rate (WER via jiwer) and Entity Accuracy against manually verified ground truth.', 'Rigorous Evaluation'),
        ('bullet', 'Engineered dynamic edge-computing architecture utilizing quantized GGUF weights (Q4_K_M) via llama-cpp-python, enabling air-gapped forensic inference on resource-constrained 8GB precinct laptops with zero cloud leakage.', 'Edge Quantization'),
        ('bullet', 'Delivered dual production interfaces: a standalone Windows desktop executable (CyberTerminal.exe via PyInstaller) with dynamic hardware detection (LITE vs PRO mode) and a high-performance FastAPI backend paired with a React/Vite command dashboard.', 'Production Deployment'),

        ('heading2', 'Enterprise Domain-Specific LLM Fine-Tuning Pipeline (LoRA / QLoRA)', 'Deep Learning Pipeline'),
        ('paragraph', 'Automated data engineering and fine-tuning suite to specialize open-weight foundation models on domain-specific structured extraction.'),
        ('bullet', 'Constructed an automated 2,000-sample hybrid dataset pipeline integrating Kaggle SROIE documents, Indian vehicle plate syntax, and OpenCV synthetic weather/lighting augmentations (Gaussian blur, rain streaks, night contrast).', 'Dataset Engineering'),
        ('bullet', 'Fine-tuned parameter-efficient LoRA rank-decomposition adapters on Llama 3 8B using Google Colab/PyTorch, slashing training VRAM footprint by 90% (100GB to 8GB) while enforcing zero-shot JSON output compliance.', 'LoRA Fine-Tuning'),
        ('bullet', 'Exported trained adapter into quantized 4-bit .gguf binaries, achieving sub-second token latency on standard CPU environments.', 'Model Quantization'),

        ('heading2', 'Asynchronous Forensic Batch Processing & Audit Export Engine', 'Backend Systems'),
        ('paragraph', 'High-throughput evidentiary processing engine designed for precinct-scale archives.'),
        ('bullet', 'Designed an asynchronous batch backend capable of concurrently transcribing 10,000+ handwritten case files with minimal latency, outputting structured entities (Vehicle Numbers, Dates, Names) into normalized databases.', 'High-Throughput Ingestion'),
        ('bullet', 'Implemented export workflows to flat CSV and Excel (.xlsx) formats alongside verifiable cryptographic audit records, enforcing zero persistent caching of PII to ensure chain-of-custody compliance.', 'Legal & Compliance'),

        ('heading1', 'EDUCATION'),
        ('heading2', 'Bachelor of Technology (B.Tech) in Computer Science & Engineering', 'Graduation: 2026'),
        ('bullet', 'Key Coursework: Data Structures & Algorithms, Machine Learning, Deep Learning, Computer Vision, Database Management Systems, Operating Systems, Software Engineering.', 'Core Coursework'),
        ('bullet', 'Academic Honors: Active open-source maintainer, AI/ML hackathon participant, lead student researcher in vision-language architectures.', 'Academic Highlights'),

        ('heading1', 'PUBLICATIONS & TECHNICAL WRITEUPS'),
        ('bullet', 'Author of "Architectural Decision Record: The Generative Smoothing Failure Mode in Commercial Upscalers for Forensic Alphanumeric Reconstruction".', 'Technical ADR'),
        ('bullet', 'Technical Annexure: Comprehensive guide on MLOps, Quantization Mathematics (GGUF Q4_K_M), LoRA Rank Decomposition, and Deterministic NLP Interception.', 'Forensic AI Annexure')
    ]
    
    resume_path = os.path.join(workspace, 'Gorang_Resume_Draft.docx')
    create_docx(resume_path, 'Gorang Singhal - Resume Draft', resume_sections)

    # ----------------------------------------------------
    # DOCUMENT 2: Portfolio Writeup & Interview Talking Points (.docx)
    # ----------------------------------------------------
    portfolio_sections = [
        ('title', 'POLICE FORENSICS AI: PORTFOLIO & INTERVIEW GUIDE'),
        ('subtitle', 'Deep ML Mechanics, Architecture Justifications & Interview Talking Points'),
        ('contact', 'Gorang Singhal  •  gorang.singhal06@gmail.com  •  github.com/GorangSinghal/PoliceForensicsAI'),
        
        ('heading1', '1. THE ELEVATOR PITCH'),
        ('quote', '"An end-to-end, high-throughput forensic toolkit that fuses traditional computer vision with modern LLMs to extract data from degraded law enforcement evidence."'),
        ('paragraph', 'Law enforcement agencies sit on massive backlogs of degraded evidence—ranging from blurry CCTV footage of suspects to illegible, messy handwritten notes from crime scenes. Traditional OCR tools (like Tesseract) fail completely on unconstrained handwriting, and existing image enhancers crash on local hardware when processing massive security footage frames.'),

        ('heading1', '2. DEEP ML MECHANICS & INTERVIEW TALKING POINTS'),
        ('paragraph', 'This section highlights exactly how to prove to an interviewer that you understand the underlying mechanics, rather than just acting as an "API wrapper."'),
        
        ('heading2', '1. Hybrid OCR Pipeline (Fusing Determinism with GenAI)'),
        ('bullet', 'Instead of blindly passing an entire image to an API, the system uses a hybrid approach. Dual-Engine Architecture: Uses EasyOCR for structural layout analysis and a local Small Language Model (SLM) for semantic information extraction, completely bypassing cloud API dependencies.', 'The Concept'),
        ('bullet', 'It is like giving a student an exam where the important questions are already highlighted, rather than just throwing a massive textbook at them and asking them to find the answers.', 'The Analogy'),
        ('bullet', 'It proves you know how to reduce the "hallucination space" of an LLM by constraining its inputs using traditional, highly efficient algorithms.', 'Why FAANG Cares'),

        ('heading2', '2. Deterministic NLP Safeguards (Handling AI Failure Modes)'),
        ('bullet', 'Generative AI is probabilistic and prone to hallucinations. Production systems must assume the AI will occasionally fail. We built a strict validation layer using Python (Regex and SpaCy). If the Gemini API transcribes a vehicle license plate or a date from a police report, our Python layer heuristically checks it (e.g., ensuring a date is valid and license plates match state formats).', 'The Concept'),
        ('bullet', 'The AI is the creative, fast-typing writer, but the deterministic Python code is the strict, unforgiving editor that reviews the work before it gets published.', 'The Analogy'),
        ('bullet', 'It proves you understand the fundamental flaws of LLMs and know how to engineer safety guardrails.', 'Why FAANG Cares'),

        ('heading2', '3. Tensor Memory Optimization (Hardware Manipulation)'),
        ('bullet', 'Deep learning models require massive amounts of VRAM. Processing high-resolution evidence footage often causes Out-Of-Memory (OOM) crashes on local machines. Rather than just running the pre-trained CodeFormer script, I went directly into the PyTorch inference code (app.py). The original researchers hardcoded a 4,000-pixel heuristic limit that forced the system to bypass the background enhancer to save memory. I manually overrode this tensor restriction (bumping it to 4,000,000 pixels), forcing the GAN to process the entire high-resolution frame locally.', 'The Concept'),
        ('bullet', 'Instead of letting the car automatic transmission shift for me, I popped the hood and switched it to manual so I could tow a much heavier load than the manufacturer intended.', 'The Analogy'),
        ('bullet', 'It proves you are not afraid to dive into the core PyTorch source code to manipulate tensor flow and optimize for specific hardware constraints.', 'Why FAANG Cares'),

        ('heading2', '4. Architectural Strategy: The Hybrid Cloud/Edge Pipeline'),
        ('bullet', 'Forensic data security requires air-gapped processing, but accuracy requires massive parameters. I implemented a dynamic strategy pattern. For field laptops, the system loads TinyLlama (1B parameters) on CPU/RAM. If the system detects a precinct server with a dedicated GPU, it automatically performs a hot-swap to Llama 3 8B using 4-bit quantization, significantly boosting reasoning quality for complex crime scene reconstruction.', 'The Concept'),
        ('bullet', 'The system is like a specialized search-and-rescue team that carries only essential tools when trekking through difficult terrain (Edge/Laptop), but pulls out the heavy machinery when they arrive at the base camp (Cloud/Server).', 'The Analogy'),
        ('bullet', 'It demonstrates "system-level thinking"—the ability to balance the trade-offs between local compute constraints, latency, and model intelligence.', 'Why FAANG Cares'),

        ('heading1', '3. RESUME BULLET POINTS (READY TO COPY/PASTE)'),
        ('bullet', 'Architected an end-to-end forensic evidence toolkit, fusing traditional Computer Vision (OpenCV) with modern Vision-Language Models (Gemini API) to extract structured data from highly degraded police documents.', 'Core Architecture'),
        ('bullet', 'Engineered a hybrid OCR pipeline that combined deterministic layout analysis with LLM transcription, achieving high accuracy on unconstrained handwriting while implementing custom NLP safeguards (SpaCy/Regex) to prevent AI hallucinations.', 'Hybrid Pipeline'),
        ('bullet', 'Optimized deep learning tensor allocations for a PyTorch-based GAN (CodeFormer), overriding default VRAM downsampling limits in the source code to process massive high-resolution imagery locally without Out-of-Memory (OOM) crashes.', 'Tensor Allocation'),
        ('bullet', 'Designed an asynchronous batch-processing backend capable of concurrently transcribing 10,000+ handwritten case files with minimal latency, outputting structured entities (Vehicle Numbers, Dates, Names) into normalized databases.', 'Batch Backend'),
        ('bullet', 'Implemented rigorous evaluation metrics, validating model performance mathematically using Word Error Rate (WER) for transcriptions and PSNR/SSIM scoring for image restorations.', 'Evaluation & Metrics')
    ]
    
    portfolio_path = os.path.join(workspace, 'docs', 'Portfolio_and_Interview_Guide.docx')
    create_docx(portfolio_path, 'Police Forensics AI Portfolio Guide', portfolio_sections)

if __name__ == '__main__':
    main()
