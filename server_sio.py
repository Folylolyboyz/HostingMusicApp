# import socketio

# sio = socketio.AsyncServer(async_mode="asgi")
# app = socketio.ASGIApp(sio, static_files={'/' : './'})

# async def task(sid):
#     time = await sio.call("send_time", {"time" : 0}, to=sid)
#     print(time)
#     await sio.sleep(5)

# @sio.event
# async def connect(sid, environ):
#     print(sid, "Connected")
#     sio.start_background_task(task, sid)

# @sio.event
# async def disconnect(sid):
#     print(sid, "Disconnected")
    
# @sio.event
# async def sum(sid, data):
#     return {"result" : data["numbers"][0]+data["numbers"][1]}

import socketio
import uvicorn

# Create an asynchronous Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")
app = socketio.ASGIApp(sio, static_files={'/' : './'})

@sio.event
async def connect(sid, environ):
    print(f"New client connected: {sid}")

@sio.event
async def join_room(sid, data):
    room_name = data.get("roomName")
    username = data.get("username")
    if room_name and username:
        await sio.enter_room(sid, room_name)
        print(f"{username} joined room: {room_name}")
        await sio.emit("user_joined", {"username": username, "message": f"{username} joined the room"}, room=room_name, skip_sid=sid)

@sio.event
async def player_action(sid, data):
    rooms = list(sio.rooms(sid))
    rooms.remove(sid)  # Remove the default room (own socket ID)
    if not rooms:
        print("⚠️ No room joined.")
        return
    room = rooms[0]  # Assuming one room per socket
    print(f"🎵 Player action in room {room}:", data)
    await sio.emit("player_action", data, room=room, skip_sid=sid)

@sio.event
async def track_change(sid, data):
    rooms = list(await sio.rooms(sid))
    rooms.remove(sid)  # Remove the default room
    if not rooms:
        return
    room = rooms[0]
    print(f"Track changed in room {room}:", data)
    await sio.emit("track_change", data, room=room)

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=3000)

if __name__ == "__main__":
    start_server()