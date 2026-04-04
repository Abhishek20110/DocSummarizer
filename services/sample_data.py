from datetime import datetime

SAMPLE_FOLDER = {
    "folder_id": "1J7IANPE6nn9oX3iQaw76HmIrIaOU4lK3",
    "folder_name": "DocSummarizer",
    "updated_at": datetime.fromisoformat("2026-03-03T06:04:30.095000+00:00")
}

SAMPLE_RESULTS = [
    {
      "filename": "multi_page_energy_forecast.pdf",
      "summary": "### Overview\nThe white paper projects a **200% increase** in **utility-scale battery deployments** by the decade’s end, attributing growth to falling **lithium‑ion battery costs** and expansive **government subsidies**. It also outlines how shifting consumer preferences will expand markets for **green home technologies** and **electric‑vehicle infrastructure**, while the **financial sector** supplies needed capital through **green bonds** and **impact investment funds** to meet **global climate targets**.  \n\n### Key Highlights\n- Forecasted **200% rise** in utility‑scale battery installations by 2030, based on synthesis of data from leading environmental think tanks and financial institutions.  \n- Declining **lithium‑ion battery costs** identified as a primary cost‑reduction driver enabling large‑scale deployment.  \n- Broad **government subsidies** in major economies are expected to accelerate adoption of battery storage and related infrastructure.  \n- Anticipated consumer shift toward sustainable living will generate new demand for **green home technologies** and **electric‑vehicle charging networks**.  \n- Capital mobilization will rely on **green bonds** and **impact investment funds**, positioning the financial sector as a critical enabler of the transition.  \n- The combined market and financing dynamics are framed as essential to achieving **global climate targets** within the next decade.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 10,
        "clarity": 9,
        "structure": 8,
        "overall": 9,
        "reason": "The summary effectively captures key points from the original text, is faithful to the content, and is clear and concise, but has a somewhat simplistic structure."
      }
    },
    {
      "filename": "multi_page_future_tech.pdf",
      "summary": "### Overview\nThe white paper serves as a comprehensive guide to emerging technological trends poised to reshape the global landscape by **2030**. It argues that the convergence of **biotechnology**, **nanotechnology**, and **quantum computing**, together with decentralized **3D printing**, sovereign **AI**, and immersive **augmented reality**/real‑time data visualization, will drive systemic transformation across industries. The analysis scopes the environmental, geopolitical, and operational implications of these shifts.\n\n### Key Highlights\n- The document identifies **biotechnology**, **nanotechnology**, and **quantum computing** as the foundational pillars converging to enable next",
      "evaluation": {
        "coverage": 8,
        "faithfulness": 9,
        "clarity": 9,
        "structure": 8,
        "overall": 8,
        "reason": "The summary covers key ideas, is faithful to the original, and is clear and concise, but lacks depth in certain areas and has some minor structural issues."
      }
    },
    {
      "filename": "multi_page_tech.docx",
      "summary": "### Overview\nThe **Technical Specification v5.1** outlines the system’s architectural components, prescribing a microservices‑based design to meet scalability and reliability goals. It mandates containerized deployments and asynchronous message queues to decouple services, while stressing the need for detailed diagrams to aid engineering visualization. The document serves as a blueprint for building a fault‑tolerant, maintainable platform.\n\n### Key Highlights\n- **Microservices architecture** is adopted to enable independent scaling of each service and isolate failures.  \n- **Containerized deployments** (e.g., Docker/Kubernetes) are required to ensure consistent environments and rapid provisioning across the fleet.  \n- **Asynchronous message queues** (such as RabbitMQ or Kafka) are used for inter‑service communication, reducing coupling and improving overall reliability.  \n- Detailed **system diagrams and flowcharts** are mandated for every component to provide engineers with clear data‑flow visibility.  \n- The specification emphasizes **scalability**, **fault tolerance**, and **operational resilience** as core quality attributes guiding the platform’s implementation.",
      "evaluation": {
        "coverage": 8,
        "faithfulness": 9,
        "clarity": 9,
        "structure": 8,
        "overall": 8,
        "reason": "The summary covers key ideas, is faithful to the original, and is clear and concise, but could improve in terms of fully capturing the repetitive nature of the original text and providing more specific examples."
      }
    },
    {
      "filename": "multi_page_ops.docx",
      "summary": "### Overview\nThe Operational Manual 2026 defines mandatory Standard Operating Procedures for all staff to sustain high‑quality and safety outcomes. It enforces regular audits, quarterly training, and a prescribed escalation matrix, while promoting a non‑punitive reporting culture to drive transparent continuous improvement.\n\n### Key Highlights\n- All five SOPs require universal staff adherence to maintain **high quality and safety standards**.  \n- **Regular audits** are conducted to verify compliance with each procedure.  \n- **Quarterly training sessions** provide updates on best practices and regulatory changes for every employee.  \n- An **escalation matrix** in the appendix outlines the response hierarchy for discrepancies or emergencies.  \n- **Prompt incident reporting** is mandatory, reinforcing a **non‑punitive reporting culture** that encourages openness.  \n- Consistent language across SOPs ensures uniform implementation across all departments.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 10,
        "clarity": 9,
        "structure": 8,
        "overall": 9,
        "reason": "The summary effectively captures the main ideas and key points from the original text, with minor deductions for structure due to some redundancy in the key highlights section."
      }
    },
    {
      "filename": "extensive_notes.txt",
      "summary": "### Overview\nThe document provides a comprehensive project dossier comprising **20 detailed sections**, each delivering an in‑depth analysis of a specific note. It consolidates extensive research and stakeholder interviews to establish a foundational knowledge base for the project’s subsequent strategic phases. Ongoing relevance is ensured through planned continuous monitoring, while anticipated implementation challenges are acknowledged but met with confidence in the chosen methodology.  \n\n### Key Highlights\n- **20 distinct “Deep Dive” sections** systematically explore individual notes, ensuring granular coverage across the project’s scope.  \n- Each section reports **extensive research** complemented by interviews with **multiple key stakeholders**, forming a robust evidentiary base.  \n- The findings are positioned as a **foundational element** for all later phases of the overall strategy, linking analysis directly to execution plans.  \n- A **continuous monitoring and evaluation** process is mandated for the coming months to keep insights current and actionable.  \n- The document explicitly anticipates **implementation challenges**, signaling risk awareness and proactive planning.  \n- Despite identified risks, the authors express **confidence in the methodology**, indicating a strong belief in the project’s execution framework.",
      "evaluation": {
        "coverage": 8,
        "faithfulness": 9,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary accurately captures the essence of the original document, highlighting key aspects such as the comprehensive nature of the project dossier, the methodology, and the approach to challenges, but slightly overstates the number of sections."
      }
    },
    {
      "filename": "long_project_doc.txt",
      "summary": "### Overview\nThe document delivers comprehensive analyses for **20 distinct topics**, forming the analytical backbone of the project. By integrating extensive research and stakeholder input, it establishes a data‑driven foundation for subsequent strategic phases while outlining ongoing monitoring requirements.\n\n### Key Highlights\n- The report is organized into **20 deep‑dive sections**, each targeting a separate project topic.  \n- Every section combines **extensive research** with interviews of **multiple key stakeholders** to generate robust insights.  \n- Findings are designated as a **foundational element** that will inform the next phases of the overall strategy.  \n- A schedule of **continuous monitoring and evaluation** is prescribed to keep the insights relevant over the coming months.  \n- The authors acknowledge **implementation challenges** for each topic, prompting proactive risk‑mitigation planning.  \n- Confidence is expressed in the applied **methodology**, reinforcing trust in the analytical approach despite anticipated hurdles.  \n- The uniform structure across sections supports scalable synthesis and consistent decision‑making throughout the project.",
      "evaluation": {
        "coverage": 8,
        "faithfulness": 9,
        "clarity": 9,
        "structure": 10,
        "overall": 9,
        "reason": "The summary accurately captures the essence of the original document, covering key ideas, and maintaining faithfulness to the original content. It is clear, concise, and well-structured, although it slightly overstates the number of topics as 20, when the original document only goes up to Topic 15."
      }
    },
    {
      "filename": "economic_report.pdf",
      "summary": "### Overview\nThe paper outlines the dominant macro‑economic forces shaping 2026 and their implications for corporate strategy. It argues that digital finance, sustainable energy, and a reconfigured labor market are redefining growth drivers, while divergent inflation trends and cautious monetary policy create uneven risk profiles across regions.\n\n### Key Highlights\n- **Digital currencies** and **DeFi** are becoming mainstream, prompting traditional banks to embed **blockchain** for faster, lower‑cost cross‑border payments.  \n- Investment in **solar**, **wind**, and **green hydrogen** has outpaced fossil‑fuel spending for the **third consecutive year**, spurring rapid advances in **battery storage** and **grid management** technologies.  \n- The rise of the **Gig Economy** and **remote work** detaches talent from geography, intensifying competition for a globally sourced, yet more fragmented, workforce.  \n- Governments are lagging in revising labor legislation, leaving workers in the gig and remote sectors without adequate protections.  \n- **Inflation** has stabilized in most developed economies, but **emerging markets** remain vulnerable to **commodity price** volatility.  \n- **Central banks** are keeping **interest rates** at moderate levels to sustain growth while containing price pressures.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 9,
        "clarity": 8,
        "structure": 9,
        "overall": 9,
        "reason": "The summary effectively captures key ideas, remains faithful to the original, and is clear and structurally correct, but minor details are condensed for conciseness."
      }
    },
    {
      "filename": "global_expansion.txt",
      "summary": "### Overview\nThe Global Expansion Initiative (GEI) launches **Phase 1** in **Q1 2026** to build market research and regulatory compliance foundations in **APAC** and **EMEA**. Its core aim is to secure a **40%** rise in international customer acquisition over the next five years. The phase outlines concrete milestones, risk controls, and resource allocations to enable rapid entry into target regions.\n\n### Key Highlights\n- **Phase 1 timeline**: Q1 – market analysis & site selection; Q2 – legal incorporation & office setup; Q3 – hiring & initial training; Q4 – soft launch in primary markets.  \n- **Legal entity creation**: establish entities in **five key markets** within **six months** to secure local operational footholds.  \n- **Leadership recruitment**: build local executive teams to ensure cultural alignment and drive operational efficiency.  \n- **Product adaptation**: modify offerings to satisfy regional preferences and comply with data‑protection regimes such as **GDPR** and **CCPA**.  \n- **Localized marketing**: roll out campaigns in **12 languages**, tailoring messaging to each market’s cultural context.  \n- **Risk mitigation budget**: allocate **$500,000** as a contingency to address currency volatility, political instability, and intense local competition.  \n- **Compliance audits**: conduct regular audits to verify adherence to international data protection laws and other regulatory requirements.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 10,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary effectively covers key ideas, remains faithful to the original text, and is clear and concise, with a logical structure."
      }
    },
    {
      "filename": "security_protocol.docx",
      "summary": "### Overview\nThe **Cloud Security Protocol v4.2** establishes mandatory controls for all cloud‑hosted infrastructure across the organization. It mandates strict identity safeguards, comprehensive encryption, and rapid incident response to protect data confidentiality, integrity, and availability. Compliance applies to every production system and administrative account.\n\n### Key Highlights\n- **Multi‑factor authentication (MFA)** is compulsory for all administrative accounts, and **role‑based access control (RBAC)** must enforce the principle of least privilege.  \n- Permissions are audited **every 90 days**, and any account idle for **30 days** is automatically disabled.  \n- All data at rest must be encrypted with **AES‑256**, with keys stored in a centralized **Key Management Service (KMS)** backed by a **hardware security module (HSM)**.  \n- Data in transit is required to use **TLS 1.3 or higher** to ensure secure communications.  \n- Upon a suspected breach, the incident response team must be alerted within **15 minutes**.  \n- Logs from every production system are to be aggregated in a **secure, immutable storage location** for forensic analysis.",
      "evaluation": {
        "coverage": 10,
        "faithfulness": 10,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary accurately covers all key points from the original text, is well-structured, and easy to understand."
      }
    },
    {
      "filename": "hr_benefits.docx",
      "summary": "### Overview\nThe document serves as the 2026 HR policy guide for all full‑time employees, detailing compensation, work arrangements, and development resources. It outlines the company’s remote‑first model, leave entitlements, health coverage, wellness incentives, and learning budgets, establishing the baseline benefits package for staff.\n\n### Key Highlights\n- Implements a **remote‑first** work environment with flexible core hours and monthly **Wellness Fridays** where the office closes at 1 PM.  \n- Grants **25 days** of paid annual leave in addition to local public holidays.  \n- Provides **comprehensive health insurance** covering medical, dental, and vision care from day one of employment.  \n- Allocates an annual **$500 stipend** for gym memberships, mental‑health apps, or other wellness‑related expenses.  \n- Offers a **$1,000 yearly budget** for conferences, certifications, and online courses to promote continuous learning.  \n- Allows employees to dedicate **10 % of working hours** to side projects or skill‑development activities.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 10,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary accurately covers key ideas, is faithful to the original text, and is clear and concise, with a well-structured format."
      }
    },
    {
      "filename": "tech_architecture.txt",
      "summary": "### Overview\nThe document defines the 2026 industry standards for constructing high‑performance, scalable full‑stack web applications. It argues that adopting specific frontend frameworks, a microservices backend, and integrated security within CI/CD pipelines is essential for meeting modern user expectations. The scope covers frontend, backend, data storage, security,",
      "evaluation": {
        "coverage": 8,
        "faithfulness": 9,
        "clarity": 9,
        "structure": 8,
        "overall": 8,
        "reason": "The summary covers key ideas, is faithful to the original, and is clear and concise, but lacks some details on specific technologies and practices mentioned in the original text."
      }
    },
    {
      "filename": "ai_strategy.pdf",
      "summary": "### Overview\nThe paper presents a corporate strategy that positions **Artificial Intelligence** as essential for maintaining competitiveness in enterprise software. It contends that AI‑driven automation in supply‑chain forecasting, customer‑experience interfaces, and internal productivity tools is required to preserve operational efficiency and customer satisfaction. The",
      "evaluation": {
        "coverage": 8,
        "faithfulness": 9,
        "clarity": 9,
        "structure": 8,
        "overall": 8,
        "reason": "Summary covers main ideas, is faithful to the original, and clear, but lacks detail on specific AI applications"
      }
    },
    {
      "filename": "project_overview.txt",
      "summary": "### Overview\nThe document outlines **Project Alpha**, which seeks to transform document processing by leveraging AI to extract meaningful insights from raw data. It establishes three sequential milestones—**initial research**, **prototype development**, and **final deployment** slated for **Q4 2026**—defining the project’s timeline and deliverables.\n\n### Key Highlights\n- Goal: replace manual document handling with **AI‑driven extraction** of actionable insights from raw data.  \n- Core technology: deployment of **advanced AI models** for natural language processing and data mining.  \n- Milestone 1 – **initial research**: evaluate existing NLP techniques and design data ingestion pipelines.  \n- Milestone 2 – **prototype development**: build a proof‑of‑concept system,",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 9,
        "clarity": 8,
        "structure": 9,
        "overall": 9,
        "reason": "The summary covers key ideas, is faithful to the original, and has a clear structure, but some points are slightly elaborated upon."
      }
    },
    {
      "filename": "financial_report.pdf",
      "summary": "### Overview\nThe document presents the company’s annual financial summary, highlighting recent performance metrics and future expectations. It reports a **25% year‑over‑year revenue increase to $2 M ARR**, a **15% reduction in operational costs via automated internal tools**, and projects **30% growth for the next fiscal year**. The scope encompasses both historical results and forward‑looking forecasts, indicating a strong financial trajectory.\n\n### Key Highlights\n- Revenue climbed **25% YoY**, reaching **$2 M in annual recurring revenue**, underscoring robust market demand.  \n- Operational expenditures were cut **15%** after deploying **automated internal tools**, improving cost efficiency.  \n- The cost‑saving automation initiative also streamlined workflows, reducing manual processing time (specific time savings not quantified).  \n- Financial outlook projects a **30% increase** in revenue for the upcoming fiscal year, reflecting confidence in continued growth drivers.  \n- Combined revenue growth and cost optimization yield an enhanced profit margin, positioning the company for stronger cash flow and investment capacity.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 8,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary covers key ideas, is clear and concise, and structurally correct, but introduces a minor hallucination about 'specific time savings not quantified' and 'stronger cash flow and investment capacity' not present in the original text."
      }
    },
    {
      "filename": "research_paper.pdf",
      "summary": "### Overview\nThe paper investigates how **large language models** affect routine administrative work. Empirical results show an average weekly time saving of **4 hours per week** per user when employing **automated summarization tools**, leading to the conclusion that **AI** is a **vital component of modern workflow optimization**.\n\n### Key Highlights\n- Evaluates the deployment of **large language models** for daily administrative tasks in a corporate setting.  \n- Compares task completion times with and without **automated summarization tools** to quantify efficiency gains.  \n- Reports a mean reduction of **4 hours per week** in user workload when the AI tools are used.  \n- Focuses on **automated summarization tools** as the primary AI-driven mechanism examined.  \n- Concludes that integrating such tools can markedly boost productivity, positioning **AI** as essential for **workflow optimization**.  \n- Quantifies potential cost savings and enables reallocation of staff to higher‑value activities due to the time saved.  \n- Recommends organizations adopt **large language model**‑based summarization within standard processes to capture measurable efficiency improvements.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 8,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary covers key ideas, is faithful to the original, and is clear and concise, but includes some minor extrapolations not present in the original text."
      }
    },
    {
      "filename": "marketing_plan.docx",
      "summary": "### Overview\nThe 2026 Marketing Strategy aims to promote **DocSummarizer** to professionals who process large document sets. It focuses on positioning the tool’s efficiency to **research analysts** and **content creators** through targeted digital outreach. The plan leverages **social media** and **tech blogs** as primary channels to drive awareness within the defined audience.\n\n### Key Highlights\n- Target audience is explicitly **research analysts** and **content creators** who manage high volumes of documents.  \n- Campaign will be executed on **social media** platforms to reach a broad, tech‑savvy professional community.  \n- **Tech blogs** will be used to provide in‑depth demonstrations of **DocSummarizer**’s efficiency benefits.  \n- The messaging centers on the product’s ability to streamline document handling, positioning efficiency as the core value proposition.  \n- The initiative is scheduled for rollout throughout the **2026** fiscal year to align with broader corporate objectives.  \n- Anticipated outcome is heightened brand visibility and adoption among users with intensive document workflows.",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 10,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary effectively covers key ideas, remains faithful to the original text, and is clear and concise, with a well-structured format."
      }
    },
    {
      "filename": "requirements.docx",
      "summary": "### Overview\nThe document specifies a software system that provides a **web‑based interface** for users to submit documents either by direct upload or by linking **Google Drive** folders. After ingestion, a backend component extracts the content and automatically generates a concise summary of **5–10 sentences** per document. The scope covers the complete ingestion‑to‑summarization workflow without detailing performance, security, or deployment considerations.\n\n### Key Highlights\n- **Web‑based interface** supports both direct file uploads and OAuth‑based linking of **Google Drive** folders, offering dual ingestion pathways.  \n- Integration with the **Google Drive API** retrieves all files within an authorized folder for",
      "evaluation": {
        "coverage": 9,
        "faithfulness": 9,
        "clarity": 8,
        "structure": 9,
        "overall": 9,
        "reason": "The summary accurately covers key ideas, is faithful to the original, and is clear and concise, but slightly elaborates on the original text."
      }
    },
    {
      "filename": "team_notes.txt",
      "summary": "### Overview\nThe document records a brief team sync on March 2, outlining current development tasks and progress. It details work on a **Google Drive integration**, a **frontend layout** employing **CSS glassmorphism**, and testing of **extraction logic** across multiple **document formats**. The notes conclude with the scheduling of the next meeting for **Friday**.\n\n### Key Highlights\n- **Abhishek** is in the final stages of implementing the **Google Drive integration**, indicating readiness for deployment.  \n- **Sarah** is advancing the **frontend layout**, specifically applying **CSS glassmorphism** techniques to the UI.  \n- **Mike** is conducting tests on the **extraction logic**, covering a range of **document formats** to ensure compatibility.  \n- All three contributors are actively progressing on distinct components that together form the product’s core functionality.  \n- The team has set the subsequent coordination point for **Friday**, establishing a clear deadline for reviewing interim results.",
      "evaluation": {
        "coverage": 10,
        "faithfulness": 8,
        "clarity": 9,
        "structure": 9,
        "overall": 9,
        "reason": "The summary covers all key ideas, is mostly faithful, clear, and structurally correct, but slightly elaborates beyond the original text."
      }
    },
    {
      "filename": "Abhishek Dey Resume 2026 (1).pdf",
      "summary": "Error generating summary.",
      "evaluation": None
    }
  ]
