# WSI Cancer Description Multi-Agent System

Welcome to the WSI Cancer Description Multi-Agent System, powered by [crewAI](https://crewai.com). This advanced system is designed to generate comprehensive, medically accurate descriptions of cancer types based on Whole Slide Image (WSI) analysis. The system employs a sophisticated 4-agent architecture to ensure high-quality, structured, and professional medical documentation that meets international pathology standards.

## System Overview

This multi-agent system specializes in generating and refining Whole Slide Image (WSI) cancer descriptions through a collaborative workflow of four specialized agents, each with enhanced expertise and capabilities:

### 🤖 Enhanced Agent Architecture

1. **Planning Agent - WSI Cancer Analysis Planning Specialist**

   - Generates comprehensive, evidence-based content plans for cancer descriptions
   - Ensures systematic coverage of all critical diagnostic aspects
   - Integrates current pathology guidelines and international standards (WHO, CAP)
   - Creates structured frameworks for morphological analysis

2. **Description Generator - WSI Cancer Description Expert & Digital Pathologist**

   - Board-certified pathologist with 20+ years of digital pathology experience
   - Generates detailed morphological identification characteristics
   - Describes visual and architectural features with precision
   - Integrates immunohistochemical and molecular correlations

3. **Description Evaluator - Quality Assurance & Validation Specialist**

   - Performs rigorous medical review and validation
   - Ensures adherence to international pathology standards
   - Validates diagnostic accuracy and completeness
   - Provides comprehensive quality assessment

4. **Finalizer Agent - Medical Documentation & Publishing Specialist**
   - Transforms content into publication-ready medical documentation
   - Ensures compliance with medical publishing standards
   - Creates professional, structured markdown documents
   - Optimizes for medical education and clinical reference

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling.

First, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

### Configuration

**Add your `GEMINI_API_KEY` to the `.env` file**

The system uses Google Gemini for LLM operations and text embeddings. Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Basic Usage

Run the system with the default cancer type (lung cancer):

```bash
crewai run
```

### Specify Cancer Type

Analyze a specific cancer type:

```bash
crewai run "breast cancer"
```

### Supported Cancer Types

The system supports comprehensive analysis of various cancer types including:

- **Lung cancer** (adenocarcinoma, squamous cell carcinoma, large cell carcinoma, small cell lung cancer)
- **Breast cancer** (invasive ductal carcinoma, invasive lobular carcinoma, ductal carcinoma in situ)
- **Liver cancer** (hepatocellular carcinoma, cholangiocarcinoma, metastatic carcinoma)
- **Colorectal cancer** (adenocarcinoma, mucinous adenocarcinoma, signet ring cell carcinoma)
- **Prostate cancer** (adenocarcinoma, ductal adenocarcinoma, neuroendocrine carcinoma)
- And many other cancer types with specialized morphological analysis

### Advanced Usage

#### Training Mode

Train the system for improved performance:

```bash
python -m create_wsi_kl.main train <n_iterations> <training_file> [cancer_type]
```

#### Testing Mode

Test system performance:

```bash
python -m create_wsi_kl.main test <n_iterations> <eval_llm> [cancer_type]
```

#### Scenario 2: Validate from JSON

Use existing cancer descriptions from JSON file as knowledge source:

```bash
# Use JSON file as knowledge source
python -m create_wsi_kl.main "Cancer Type" --json-source knowledge/cancer_descriptions.json

# Example
python -m create_wsi_kl.main "Lung Adenocarcinoma (LUAD)" --json-source knowledge/cancer_descriptions.json
```

#### Replay Mode

Replay execution from a specific task:

```bash
python -m create_wsi_kl.main replay <task_id>
```

## Enhanced Knowledge Base

The system utilizes a comprehensive, professional knowledge base containing:

### 🔬 **Advanced WSI Cancer Data**

- Detailed morphological identification characteristics
- Visual and architectural feature specifications
- Immunohistochemical marker profiles
- Differential diagnosis matrices
- Quantitative analysis parameters

### 📋 **Professional Pathology Guidelines**

- International standards compliance (WHO, CAP, AJCC)
- Standardized documentation requirements
- Quality assurance protocols
- Grading and staging system integration

### 🧪 **Advanced Analysis Techniques**

- Quantitative morphometry
- Digital pathology tools integration
- AI-assisted pattern recognition
- Automated counting and measurement protocols

### Knowledge Sources

- `knowledge/wsi_cancer_data.txt`: Comprehensive cancer type database with advanced morphological criteria
- `knowledge/pathology_guidelines.txt`: International medical documentation standards and protocols
- `knowledge/user_preference.txt`: System configuration and quality standards
- `knowledge/sodapdf-converted.pdf`: Additional reference materials and case studies

## Professional Output

The system generates publication-ready medical documentation in structured markdown format:

### 📄 **Output Specifications**

- **File**: `wsi_cancer_description.md`
- **Format**: Professional markdown with medical documentation standards
- **Structure**: Comprehensive sections with hierarchical organization

### 📊 **Content Includes**

- **Morphological Identification Characteristics**: Detailed cellular and architectural features
- **Visual and Architectural Features**: Comprehensive WSI-specific descriptions
- **Cellular Characteristics**: Quantitative and qualitative assessments
- **Differential Diagnosis**: Distinguishing morphological features
- **Clinical Significance**: Prognostic and therapeutic implications
- **Grading and Staging**: Integration with established classification systems

## Advanced System Features

### 🔬 **Medical Excellence**

- Board-certified pathologist expertise simulation
- Standardized WHO and CAP terminology
- Current medical guidelines compliance
- Rigorous quality assurance validation
- Evidence-based content generation

### 🌐 **International Standards**

- WHO Classification of Tumours compliance
- CAP Protocol integration
- AJCC Staging Manual correlation
- ISUP Guidelines adherence
- International pathology society standards

### 📊 **Quality Assurance**

- Multi-stage review process
- Content validation and verification
- Diagnostic accuracy assessment
- Consistency checks and terminology validation
- Professional formatting standards

### 🤖 **Advanced Technology**

- Autonomous workflow execution
- Sequential task coordination
- Inter-agent communication protocols
- Reproducible medical documentation
- AI-assisted quality control

### 🎯 **Professional Applications**

- Medical education and training materials
- Clinical reference documentation
- Pathology research support
- Educational curriculum development
- Professional certification preparation

## Customization and Extension

### Modifying System Components

- **Agents**: Edit `src/create_wsi_kl/config/agents.yaml` to customize agent expertise and behaviors
- **Tasks**: Modify `src/create_wsi_kl/config/tasks.yaml` to adjust task specifications and requirements
- **Knowledge Base**: Extend `knowledge/` directory with additional medical references and guidelines

### Adding New Cancer Types

- Update `knowledge/wsi_cancer_data.txt` with new cancer type specifications
- Add relevant morphological criteria and diagnostic features
- Include immunohistochemical profiles and differential diagnosis information

### Integration Capabilities

- Compatible with existing pathology information systems
- Supports integration with digital pathology platforms
- Extensible for custom reporting requirements
- Adaptable for institutional guidelines and protocols

## Technical Specifications

### System Requirements

- **Python**: >=3.10 <3.14
- **Dependencies**: CrewAI, Docling, Google Generative AI
- **LLM**: Google Gemini 2.5 Flash Preview
- **Embeddings**: Google text-embedding-004
- **Processing**: Sequential multi-agent workflow

### Performance Characteristics

- **Accuracy**: Validated against pathology literature and guidelines
- **Consistency**: Reproducible results across multiple runs
- **Completeness**: Comprehensive coverage of morphological features
- **Speed**: Optimized for efficient processing and generation

## Support and Resources

For support, questions, or feedback regarding the WSI Cancer Description System:

- Visit the [crewAI documentation](https://docs.crewai.com)
- Check the [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join the Discord community](https://discord.com/invite/X4JWnZnxPb)

### Additional Resources

- **WHO Classification of Tumours**: Latest morphological criteria and standards
- **CAP Protocols**: College of American Pathologists reporting guidelines
- **Digital Pathology Resources**: WSI analysis techniques and best practices
- **Medical Education Materials**: Pathology teaching and training resources

## Medical Disclaimer

This system is designed for educational and research purposes. All generated content should be reviewed and validated by qualified medical professionals before clinical use. The system does not replace professional medical diagnosis or treatment recommendations. Always consult with certified pathologists and healthcare providers for clinical decision-making.

## Compliance and Standards

The system adheres to:

- **HIPAA**: Health Insurance Portability and Accountability Act compliance
- **Medical Device Regulations**: Appropriate classification and usage guidelines
- **International Standards**: WHO, CAP, AJCC, and other professional organization guidelines
- **Quality Assurance**: Continuous validation and improvement protocols

---

_Building the future of AI-assisted medical documentation with the power and precision of specialized multi-agent systems._

**TCGA-Lung Cancer Types**

The TCGA-Lung project includes the following major cancer types:

- **Lung Adenocarcinoma (LUAD)**
- **Lung Squamous Cell Carcinoma (LUSC)**

**TCGA-Renal Cancer Types**

The TCGA-Renal project includes the following major cancer types:

- **Kidney Renal Clear Cell Carcinoma (KIRC)**
- **Kidney Renal Papillary Cell Carcinoma (KIRP)**
- **Kidney Chromophobe (KICH)**

**CAMELYON16 Cancer Types**

The CAMELYON16 project is a benchmark dataset for the detection of lymph node metastases in breast cancer using whole slide images. It focuses on the following cancer-related categories:

- **Breast Cancer Lymph Node Metastasis (Primary focus)**
  - Macro-metastases (large metastatic deposits)
  - Micro-metastases (small metastatic deposits)
- **No Tumor (Negative Lymph Nodes)**
  - Lymph node slides without evidence of metastatic tumor, serving as negative controls

For more information, visit the [CAMELYON16 website](https://camelyon16.grand-challenge.org/).

