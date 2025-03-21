import asyncio
import uvicorn
from multiprocessing import Process

def run_socketio():
    """Start the Socket.IO server (on port 3000)"""
    from server_sio import start_server
    start_server()  # This is a blocking call, so we use multiprocessing

async def run_fastapi():
    """Start the FastAPI server (on port 8000)"""
    config = uvicorn.Config("ytmusic_interact:app", host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    """Run both FastAPI and Socket.IO concurrently"""
    socketio_process = Process(target=run_socketio)  # Run Socket.IO in a separate process
    socketio_process.start()

    await run_fastapi()  # Run FastAPI normally

    socketio_process.join()  # Wait for Socket.IO process to finish

if __name__ == "__main__":
    asyncio.run(main())
