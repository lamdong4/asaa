#!/usr/bin/env python3
"""
Entry point for the ASAA application
"""

if __name__ == "__main__":
    import uvicorn
    from src.asaa.main import app
    
    uvicorn.run(
        "src.asaa.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )