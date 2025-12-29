#!/bin/bash
# Complete RAGFlow + Instella Research Workflow
# This script provides a menu-driven interface for manuscript enhancement

set -e

SCRIPT_DIR="/Users/mac/LIFE"
cd "$SCRIPT_DIR"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}RAGFlow + Instella Research Workflow${NC}"
echo -e "${BLUE}BCC Manuscript Enhancement${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${RED}❌ Virtual environment not found at .venv${NC}"
    echo "Please create it first with: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo -e "${GREEN}✓${NC} Activating virtual environment..."
source .venv/bin/activate

# Check dependencies
echo -e "${GREEN}✓${NC} Checking dependencies..."
python3 -c "import torch, transformers" 2>/dev/null || {
    echo -e "${YELLOW}⚠${NC} Missing dependencies. Installing..."
    pip install --quiet torch transformers accelerate sentencepiece
}

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Select Workflow:${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "1. Test Instella (quick health check)"
echo "2. Summarize all manuscript sections"
echo "3. Refine manuscript outline"
echo "4. Rewrite single section"
echo "5. Run reviewer pass on section"
echo "6. Full Instella pipeline (all phases)"
echo ""
echo "RAGFlow Options (requires Docker):"
echo "7. Check RAGFlow status"
echo "8. Start RAGFlow services"
echo "9. Create RAGFlow user"
echo "10. Upload manuscript to RAGFlow"
echo ""
echo "Hybrid Workflows:"
echo "11. RAG-enhanced section rewrite"
echo "12. Consistency check (RAGFlow + Instella)"
echo ""
echo "SkyPilot GPU Editing (Cloud):"
echo "13. Launch SkyPilot manuscript editing"
echo "14. Check SkyPilot job status"
echo "15. Download SkyPilot results"
echo ""
echo "0. Exit"
echo ""
read -p "Enter choice [0-15]: " choice

case $choice in
    1)
        echo -e "\n${BLUE}Testing Instella...${NC}"
        python3 -c "
from instella_client import instella_chat
print('Loading model...')
response = instella_chat(
    system='You are a helpful assistant.',
    messages=[{'role': 'user', 'content': 'Say hello in one sentence.'}],
    max_new_tokens=20,
    temperature=0.3
)
print(f'✅ Response: {response}')
"
        ;;
    
    2)
        echo -e "\n${BLUE}Summarizing manuscript sections...${NC}"
        python3 summarize_manuscript.py | tee MANUSCRIPT_SUMMARY.md
        echo -e "\n${GREEN}✓${NC} Summary saved to MANUSCRIPT_SUMMARY.md"
        ;;
    
    3)
        echo -e "\n${BLUE}Refining manuscript outline...${NC}"
        python3 refine_outline.py | tee REFINED_OUTLINE.md
        echo -e "\n${GREEN}✓${NC} Outline saved to REFINED_OUTLINE.md"
        ;;
    
    4)
        echo ""
        echo "Available sections:"
        echo "  1. introduction"
        echo "  2. theory"
        echo "  3. methods"
        echo "  4. results"
        echo "  5. discussion"
        echo "  6. conclusion"
        read -p "Select section [1-6]: " sec_choice
        
        case $sec_choice in
            1) section="intro" ;;
            2) section="theory" ;;
            3) section="methods" ;;
            4) section="results" ;;
            5) section="discussion" ;;
            6) section="conclusion" ;;
            *) echo "Invalid choice"; exit 1 ;;
        esac
        
        echo -e "\n${BLUE}Rewriting ${section} section...${NC}"
        python3 rewrite_driver.py \
            "draft_${section}_BCC.md" \
            "draft_${section}_BCC_rewritten.md" \
            "${section}" \
            "Nature Communications"
        echo -e "\n${GREEN}✓${NC} Rewritten section saved to draft_${section}_BCC_rewritten.md"
        ;;
    
    5)
        echo ""
        echo "Available sections:"
        echo "  1. introduction"
        echo "  2. theory"
        echo "  3. methods"
        echo "  4. results"
        echo "  5. discussion"
        echo "  6. conclusion"
        read -p "Select section [1-6]: " sec_choice
        
        case $sec_choice in
            1) section="intro" ;;
            2) section="theory" ;;
            3) section="methods" ;;
            4) section="results" ;;
            5) section="discussion" ;;
            6) section="conclusion" ;;
            *) echo "Invalid choice"; exit 1 ;;
        esac
        
        echo -e "\n${BLUE}Running reviewer pass on ${section}...${NC}"
        python3 reviewer_pass_driver.py \
            "draft_${section}_BCC_rewritten.md" \
            "REVIEW_NOTES_INSTELLA.md" \
            "${section}"
        echo -e "\n${GREEN}✓${NC} Review notes appended to REVIEW_NOTES_INSTELLA.md"
        ;;
    
    6)
        echo -e "\n${BLUE}Running full Instella pipeline...${NC}"
        echo "This will take 4-6 hours. Continue? [y/N]"
        read -p "> " confirm
        if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
            bash run_rewrites.sh
        else
            echo "Cancelled."
        fi
        ;;
    
    7)
        echo -e "\n${BLUE}Checking RAGFlow status...${NC}"
        docker ps | grep ragflow || echo -e "${YELLOW}⚠${NC} RAGFlow containers not running"
        ;;
    
    8)
        echo -e "\n${BLUE}Starting RAGFlow services...${NC}"
        cd ragflow
        docker-compose -f docker/docker-compose.yml up -d
        cd ..
        echo -e "\n${GREEN}✓${NC} RAGFlow started. Access at http://localhost"
        ;;
    
    9)
        echo -e "\n${BLUE}Creating RAGFlow user...${NC}"
        container_id=$(docker ps | grep ragflow | grep api | awk '{print $1}' | head -1)
        if [ -z "$container_id" ]; then
            echo -e "${RED}❌ RAGFlow API container not found. Start services first (option 8)${NC}"
            exit 1
        fi
        docker cp create_user.py "$container_id:/tmp/"
        docker exec -it "$container_id" python /tmp/create_user.py
        ;;
    
    10)
        echo -e "\n${BLUE}Uploading manuscript to RAGFlow...${NC}"
        python3 -c "
from ragflow_client import RAGFlowClient
from pathlib import Path

client = RAGFlowClient(
    base_url='http://localhost',
    email='researcher@ragflow.local',
    password='ragflow123'
)

# Create KB
kb = client.create_knowledge_base(
    name='BCC Manuscript',
    description='Biological Counter-Curvature manuscript'
)
print(f'Created KB: {kb[\"id\"]}')

# Upload sections
sections_dir = Path('life/manuscript/sections')
for tex_file in sections_dir.glob('*.tex'):
    print(f'Uploading {tex_file.name}...')
    client.upload_document(kb['id'], str(tex_file))

print('✅ Upload complete')
"
        ;;
    
    11)
        echo -e "\n${YELLOW}⚠${NC} RAG-enhanced rewrite requires both RAGFlow and Instella"
        echo "Feature coming soon..."
        ;;
    
    12)
        echo -e "\n${YELLOW}⚠${NC} Consistency check requires RAGFlow"
        echo "Feature coming soon..."
        ;;
    
    13)
        echo -e "\n${BLUE}Launching SkyPilot manuscript editing...${NC}"
        echo ""
        echo "Choose instance type:"
        echo "  1. On-demand (guaranteed, ~$0.08)"
        echo "  2. Spot (3-6x cheaper, ~$0.02, may be preempted)"
        read -p "Select [1-2]: " instance_choice
        
        case $instance_choice in
            1)
                echo -e "\n${GREEN}Launching on-demand instance...${NC}"
                ./sky_edit.sh launch
                ;;
            2)
                echo -e "\n${GREEN}Launching spot instance...${NC}"
                ./sky_edit.sh launch-spot
                ;;
            *)
                echo "Invalid choice"
                exit 1
                ;;
        esac
        ;;
    
    14)
        echo -e "\n${BLUE}Checking SkyPilot job status...${NC}"
        ./sky_edit.sh status
        echo ""
        echo "View logs? [y/N]"
        read -p "> " view_logs
        if [ "$view_logs" = "y" ] || [ "$view_logs" = "Y" ]; then
            ./sky_edit.sh logs
        fi
        ;;
    
    15)
        echo -e "\n${BLUE}Downloading SkyPilot results...${NC}"
        ./sky_edit.sh download
        echo ""
        echo "Results downloaded to edited_sections/"
        ls -lh edited_sections/
        ;;
    
    0)
        echo "Exiting..."
        exit 0
        ;;
    
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Workflow complete!${NC}"
echo -e "${GREEN}========================================${NC}"
