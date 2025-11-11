import os
import sys
import json
from scripts.generate_features_index import simple_parse_yaml_like, build_markdown


def test_simple_yaml_parser():
    raw = '''
features:
  - id: TEST-001
    title: Test Feature
    description: Unit test feature
    implemented: true
    tags: [test, unit]
'''
    meta = simple_parse_yaml_like(raw)
    assert 'features' in meta
    assert len(meta['features']) == 1
    assert meta['features'][0]['id'] == 'TEST-001'


def test_build_markdown():
    features = [
        {'id': 'T-1', 'title': 'A', 'implemented': True, 'repo': 'repo1', 'tags': ['t1', 't2'], 'link': '/a'},
        {'id': 'T-2', 'title': 'B', 'implemented': False, 'repo': 'repo2', 'tags': 'x,y', 'link': '/b'},
    ]
    md = build_markdown(features)
    assert 'A' in md
    assert 'B' in md
