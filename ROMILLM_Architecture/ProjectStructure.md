ROMILLM_Project/
├── 1️⃣ 📁 Core_Orchestration/           # 🎯 CENTRAL DOMAIN: Pipeline coordination
│   ├── 📄 README.md                      # Domain documentation
│   ├── 1.1 📁 Pipeline_Manager/         # 🔄 Object: End-to-end processing coordination
│   │   ├── 1.1.1 Config/                 # 📦 PODs: Pipeline configuration DTOs
│   │   ├── 1.1.2 Toolbox/                # 🛠️ Layer 1: Pipeline calculation utilities
│   │   ├── 1.1.3 Core/                   # 💼 Layer 3: Pipeline execution state management
│   │   ├── 1.1.4 Api/                    # 🎯 Layer 4: Pipeline coordination interface
│   │   └── 1.1.5 Tests/                  # 🧪 Domain-specific pipeline tests
│   └── 1.2 📁 Memory_Manager/           # 🧠 Object: Resource allocation & optimization
│       ├── 1.2.1 Config/                 # 📦 PODs: Memory configuration DTOs
│       ├── 1.2.2 Toolbox/                # 🛠️ Layer 1: Memory calculation algorithms
│       ├── 1.2.3 Core/                   # 💼 Layer 3: Pool management & allocation
│       ├── 1.2.4 Api/                    # 🎯 Layer 4: Resource management interface
│       └── 1.2.5 Tests/                  # 🧪 Memory management validation
│
├── 2️⃣ 📁 Ingestion_Pipeline/           # 📥 DOMAIN: Document parsing & entity extraction
│   ├── 📄 README.md                      # Domain documentation
│   ├── 2.1 📁 Document_Parser/          # 📄 Object: Multi-format document processing
│   │   ├── 2.1.1 Config/                 # 📦 PODs: Parser configuration DTOs
│   │   ├── 2.1.2 Toolbox/                # 🛠️ Layer 1: Parsing algorithm utilities
│   │   ├── 2.1.3 Core/                   # 💼 Layer 3: Parser state & format handlers
│   │   ├── 2.1.4 Api/                    # 🎯 Layer 4: Unified parsing interface
│   │   └── 2.1.5 Tests/                  # 🧪 Parser validation tests
│   ├── 2.2 📁 Entity_Extractor/         # 🏷️ Object: NLP entity recognition & classification
│   │   ├── 2.2.1 Config/                 # 📦 PODs: Entity extraction configuration
│   │   ├── 2.2.2 Toolbox/                # 🛠️ Layer 1: Entity matching algorithms
│   │   ├── 2.2.3 Core/                   # 💼 Layer 3: Extractor state & model management
│   │   ├── 2.2.4 Api/                    # 🎯 Layer 4: Entity extraction interface
│   │   └── 2.2.5 Tests/                  # 🧪 Entity extraction accuracy tests
│   └── 2.3 📁 Content_Chunker/          # ✂️ Object: Semantic text segmentation
│       ├── 2.3.1 Config/                 # 📦 PODs: Chunking strategy configuration
│       ├── 2.3.2 Toolbox/                # 🛠️ Layer 1: Segmentation algorithms
│       ├── 2.3.3 Core/                   # 💼 Layer 3: Chunker state & boundary detection
│       ├── 2.3.4 Api/                    # 🎯 Layer 4: Chunking interface
│       └── 2.3.5 Tests/                  # 🧪 Content segmentation validation
│
├── 3️⃣ 📁 Knowledge_Graph_Processing/   # 🕸️ DOMAIN: Graph construction & algorithms
│   ├── 📄 README.md                      # Domain documentation
│   ├── 3.1 📁 Graph_Constructor/        # 🏗️ Object: Entity-relationship knowledge building
│   │   ├── 3.1.1 Config/                 # 📦 PODs: Graph construction parameters
│   │   ├── 3.1.2 Toolbox/                # 🛠️ Layer 1: Graph theory algorithms
│   │   ├── 3.1.3 Core/                   # 💼 Layer 3: Construction state & validation
│   │   ├── 3.1.4 Api/                    # 🎯 Layer 4: Graph building interface
│   │   └── 3.1.5 Tests/                  # 🧪 Graph construction validation
│   ├── 3.2 📁 Graph_Algorithms/         # 🔍 Object: Centrality, clustering, path finding
│   │   ├── 3.2.1 Config/                 # 📦 PODs: Algorithm parameter configurations
│   │   ├── 3.2.2 Toolbox/                # 🛠️ Layer 1: Pure algorithm implementations
│   │   ├── 3.2.3 Core/                   # 💼 Layer 3: Algorithm execution management
│   │   ├── 3.2.4 Api/                    # 🎯 Layer 4: Algorithm execution interface
│   │   └── 3.2.5 Tests/                  # 🧪 Algorithm accuracy & performance
│   └── 3.3 📁 Relationship_Fusion/      # 🔗 Object: Multi-source relationship integration
│       ├── 3.3.1 Config/                 # 📦 PODs: Fusion strategy parameters
│       ├── 3.3.2 Toolbox/                # 🛠️ Layer 1: Relationship fusion algorithms
│       ├── 3.3.3 Core/                   # 💼 Layer 3: Fusion state & conflict resolution
│       ├── 3.3.4 Api/                    # 🎯 Layer 4: Relationship integration interface
│       └── 3.3.5 Tests/                  # 🧪 Relationship fusion validation
│
├── 4️⃣ 📁 Routing_Engine/               # 🎯 DOMAIN: Intent classification & processing
│   ├── 📄 README.md                      # Domain documentation
│   ├── 4.1 📁 Intent_Classifier/        # 🧠 Object: Query intent analysis & categorization
│   │   ├── 4.1.1 Config/                 # 📦 PODs: Classification rule configurations
│   │   ├── 4.1.2 Toolbox/                # 🛠️ Layer 1: Classification algorithm utilities
│   │   ├── 4.1.3 Core/                   # 💼 Layer 3: Classifier state & rule management
│   │   ├── 4.1.4 Api/                    # 🎯 Layer 4: Intent classification interface
│   │   └── 4.1.5 Tests/                  # 🧪 Intent classification accuracy
