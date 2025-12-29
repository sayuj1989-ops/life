#!/bin/bash
# SkyPilot Manuscript Editing - Convenience Wrapper
# Simplifies common SkyPilot operations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment
source .venv/bin/activate

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
show_help() {
    echo -e "${BLUE}SkyPilot Manuscript Editor${NC}"
    echo ""
    echo "Usage: ./sky_edit.sh [command]"
    echo ""
    echo "Commands:"
    echo "  launch       - Launch manuscript editing job"
    echo "  launch-spot  - Launch with spot instances (cheaper)"
    echo "  test         - Run test job (Qwen-7B)"
    echo "  status       - Check job status"
    echo "  logs         - View real-time logs"
    echo "  download     - Download edited sections"
    echo "  stop         - Stop and terminate cluster"
    echo "  cost         - Show cost estimate"
    echo "  clusters     - List all clusters"
    echo "  help         - Show this help"
    echo ""
}

launch_job() {
    echo -e "${GREEN}🚀 Launching manuscript editing job...${NC}"
    echo ""
    sky launch manuscript_editing.yaml --cluster manuscript-edit --yes
}

launch_spot() {
    echo -e "${GREEN}🚀 Launching manuscript editing (SPOT)...${NC}"
    echo -e "${YELLOW}⚠️  Using spot instances - may be preempted but 3-6x cheaper${NC}"
    echo ""
    sky launch manuscript_editing_spot.yaml --cluster manuscript-edit-spot --yes
}

test_job() {
    echo -e "${GREEN}🧪 Running test job...${NC}"
    echo ""
    sky launch test_qwen.yaml --cluster test-qwen --yes --down
}

check_status() {
    echo -e "${BLUE}📊 Cluster Status${NC}"
    echo ""
    sky status
}

view_logs() {
    echo -e "${BLUE}📋 Viewing logs...${NC}"
    echo ""
    
    # Check which cluster exists
    if sky status | grep -q "manuscript-edit-spot"; then
        sky logs manuscript-edit-spot --follow
    elif sky status | grep -q "manuscript-edit"; then
        sky logs manuscript-edit --follow
    else
        echo -e "${RED}❌ No active manuscript editing cluster found${NC}"
        exit 1
    fi
}

download_results() {
    echo -e "${GREEN}📥 Downloading edited sections...${NC}"
    echo ""
    
    # Determine cluster name
    if sky status | grep -q "manuscript-edit-spot"; then
        CLUSTER="manuscript-edit-spot"
    elif sky status | grep -q "manuscript-edit"; then
        CLUSTER="manuscript-edit"
    else
        echo -e "${RED}❌ No active cluster found${NC}"
        exit 1
    fi
    
    # Download results
    sky exec $CLUSTER "ls -lh edited_sections/"
    sky down $CLUSTER --yes
    
    echo ""
    echo -e "${GREEN}✅ Results downloaded to edited_sections/${NC}"
}

stop_cluster() {
    echo -e "${YELLOW}🛑 Stopping clusters...${NC}"
    echo ""
    
    # Stop all manuscript editing clusters
    for cluster in manuscript-edit manuscript-edit-spot test-qwen; do
        if sky status | grep -q "$cluster"; then
            echo "Stopping $cluster..."
            sky down $cluster --yes
        fi
    done
    
    echo -e "${GREEN}✅ All clusters stopped${NC}"
}

show_cost() {
    echo -e "${BLUE}💰 Cost Estimate${NC}"
    echo ""
    echo "On-Demand (RTX 4090):"
    echo "  - Hourly rate: ~\$0.39/hr"
    echo "  - Estimated job time: 10-15 minutes"
    echo "  - Estimated cost: \$0.06-0.10"
    echo ""
    echo "Spot Instance (RTX 4090):"
    echo "  - Hourly rate: ~\$0.10/hr"
    echo "  - Estimated job time: 10-15 minutes"
    echo "  - Estimated cost: \$0.02-0.03"
    echo ""
    echo "Actual costs:"
    sky cost-report
}

list_clusters() {
    echo -e "${BLUE}☁️  All Clusters${NC}"
    echo ""
    sky status --all
}

# Main command handler
case "${1:-help}" in
    launch)
        launch_job
        ;;
    launch-spot)
        launch_spot
        ;;
    test)
        test_job
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    download)
        download_results
        ;;
    stop)
        stop_cluster
        ;;
    cost)
        show_cost
        ;;
    clusters)
        list_clusters
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
