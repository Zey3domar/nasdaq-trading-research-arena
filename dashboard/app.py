from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
import random
import asyncio
from datetime import datetime, timedelta

app = FastAPI()

# Mock data for demonstration
strategies = [
    {"id": "STRAT_001", "name": "Momentum Pro", "sharpe": 2.45, "return": 0.23, "drawdown": 0.08, "trades": 1250, "family": "momentum"},
    {"id": "STRAT_002", "name": "Mean Reversion X", "sharpe": 2.12, "return": 0.19, "drawdown": 0.12, "trades": 890, "family": "mean_reversion"},
    {"id": "STRAT_003", "name": "ML Ensemble", "sharpe": 2.38, "return": 0.21, "drawdown": 0.09, "trades": 1560, "family": "machine_learning"},
    {"id": "STRAT_004", "name": "VWAP Breakout", "sharpe": 1.95, "return": 0.17, "drawdown": 0.15, "trades": 720, "family": "momentum"},
    {"id": "STRAT_005", "name": "Stat Arb", "sharpe": 2.08, "return": 0.18, "drawdown": 0.11, "trades": 1100, "family": "statistical"},
]

@app.get("/")
async def get_dashboard():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trading Research Arena</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #1a1a1a; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
            .stat-card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .strategy-list { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .strategy-item { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
            .strategy-item:last-child { border-bottom: none; }
            .metric { display: inline-block; margin-right: 15px; }
            .sharpe { color: #28a745; font-weight: bold; }
            .return { color: #007bff; }
            .drawdown { color: #dc3545; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏆 Nasdaq Trading Research Arena</h1>
                <p>Real-time strategy competition • Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Strategies</h3>
                    <h2>1,000</h2>
                </div>
                <div class="stat-card">
                    <h3>Active Bots</h3>
                    <h2>850+</h2>
                </div>
                <div class="stat-card">
                    <h3>Best Sharpe</h3>
                    <h2>2.45</h2>
                </div>
                <div class="stat-card">
                    <h3>Current Champion</h3>
                    <h2>Momentum Pro</h2>
                </div>
            </div>
            
            <div class="strategy-list">
                <h2>Top Performing Strategies</h2>
    """)
    
    # Add strategy items
    for i, strat in enumerate(strategies[:5]):
        html += f"""
                <div class="strategy-item">
                    <div>
                        <strong>#{i+1} {strat['name']}</strong>
                        <span class="metric sharpe">Sharpe: {strat['sharpe']}</span>
                        <span class="metric return">Return: {strat['return']*100:.1f}%</span>
                        <span class="metric drawdown">DD: {strat['drawdown']*100:.1f}%</span>
                    </div>
                    <div>
                        <small>{strat['trades']} trades • {strat['family']}</small>
                    </div>
                </div>
        """
    
    html += """
            </div>
        </div>
        
        <script>
            // WebSocket for real-time updates
            const ws = new WebSocket('ws://localhost:8000/ws/live-updates');
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                console.log('Real-time update:', data);
                // Update UI with new data
            };
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(html)

@app.get("/api/tournament/status")
async def get_tournament_status():
    return {
        "status": "running",
        "total_strategies": 1000,
        "active_strategies": 850,
        "eliminated_strategies": 150,
        "current_generation": 42,
        "best_sharpe": 2.45,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/strategies/top")
async def get_top_strategies(limit: int = 10):
    sorted_strategies = sorted(strategies, key=lambda x: x['sharpe'], reverse=True)
    return {
        "strategies": sorted_strategies[:limit],
        "total_count": len(strategies)
    }

@app.websocket("/ws/live-updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Send mock real-time data
        update = {
            "timestamp": datetime.now().isoformat(),
            "active_strategies": random.randint(840, 860),
            "top_strategy": random.choice(strategies)['name'],
            "market_regime": random.choice(["trending", "ranging", "volatile"])
        }
        await websocket.send_json(update)
        await asyncio.sleep(5)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
