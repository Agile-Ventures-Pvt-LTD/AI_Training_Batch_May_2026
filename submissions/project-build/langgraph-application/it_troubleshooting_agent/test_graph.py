#!/usr/bin/env python3
"""Test script for LangGraph build_graph()"""
from graph import build_graph, visualize_graph

if __name__ == "__main__":
    print("Building LangGraph...")
    try:
        g = build_graph()
        print(f"✓ Graph built successfully!")
        print(f"  Type: {type(g)}")
        print(f"  Graph compiled: {g is not None}")
    except Exception as e:
        print(f"✗ Error building graph: {e}")
        import traceback
        traceback.print_exc()

    print("\nVisualizing graph...")
    try:
        p = visualize_graph()
        print(f"✓ Graph visualization saved to: {p}")
    except Exception as e:
        print(f"✗ Error visualizing graph: {e}")
        import traceback
        traceback.print_exc()
