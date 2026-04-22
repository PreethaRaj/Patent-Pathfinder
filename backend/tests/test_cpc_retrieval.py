from backend.services.patent_retrieval import select_top_cpc_codes


def test_select_top_cpc_codes_prefers_repeated_high_score_codes():
    results = [
        {"id": "1", "score": 0.91, "cpc_classes": ["H04R3/00", "G10L21/00"]},
        {"id": "2", "score": 0.88, "cpc_classes": ["H04R3/00", "A61F11/00"]},
        {"id": "3", "score": 0.70, "cpc_classes": ["G10L21/00"]},
    ]
    codes = select_top_cpc_codes(results, max_codes=3, seed_patents=3)
    assert "H04R3/00" in codes
    assert "G10L21/00" in codes


def test_select_top_cpc_codes_adds_subclass_backoff():
    results = [{"id": "1", "score": 0.95, "cpc_classes": ["H04R25/00"]}]
    codes = select_top_cpc_codes(results, max_codes=3, seed_patents=1)
    assert "H04R25/00" in codes
    assert "H04R25" in codes or "H04R" in codes
