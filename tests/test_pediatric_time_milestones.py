import pytest
import os
import pandas as pd
from scripts.experiments.experiment_pediatric_time_milestones import run_pediatric_sweep

def test_pediatric_time_milestones():
    """Verify that the pediatric milestones script outputs the expected files."""
    run_pediatric_sweep()

    assert os.path.exists('outputs/pediatric_milestones/milestone_sweep.csv')
    assert os.path.exists('outputs/pediatric_milestones/pediatric_time_milestones.png')

    df = pd.read_csv('outputs/pediatric_milestones/milestone_sweep.csv')
    assert len(df) > 0
    assert 'Milestone' in df.columns
    assert 'Free_Energy' in df.columns
