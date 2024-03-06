from fastapi import FastAPI, HTTPException

app = FastAPI()

machines = ["treadmill", "row", "cable", "chest_press", "elliptical", "stair_master", "leg_press"]

machine_queues = {} # Queues for each machine. key=machine_id value=set of users

user_queues = {} # Users and their respective queues. key=user_id value=list of machine ids

users = set() # Set of current users (UW student ids)

# Initialize machine_queues
for machine in machines:
    machine_queues[machine] = set()

@app.get("/")
def lol():
    return {"message": "Welcome to waitless queue API"}

# user_id is added to set of users
@app.post("/add_user/{user_id}")
def join_queue(user_id: str):

    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users.add(user_id)
    user_queues[user_id] = []

    return {"message": "You have successfully initialized user: {}".format(user_id)}

# user_id is removed from set of users
@app.post("/remove_user/{user_id}")
def join_queue(user_id: str):

    if user_id not in users:
        raise HTTPException(status_code=400, detail="User does not exist")
    
    users.remove(user_id)
    del user_queues[user_id]
    for _, val in machine_queues.items():
        val.remove(user_id)

    return {"message": "You have successfully removed user: {}".format(user_id)}

# user_id joins queue for machine_id
@app.post("/join/{machine_id}/{user_id}")
def join_queue(machine_id: str, user_id: str):

    if user_id not in users:
        raise HTTPException(status_code=400, detail="User does not exist")
    if machine_id not in machine_queues:
        raise HTTPException(status_code=400, detail="Machine not in list")
    if user_id in user_queues and len(user_queues[user_id]) >= 5:
        raise HTTPException(status_code=400, detail="You cannot join more than 5 queues.")
    
    machine_queues[machine_id].add(user_id)
    if user_id not in user_queues:
        user_queues[user_id] = []
    user_queues[user_id].append(machine_id)
    return {"message": "You have successfully joined the queue for machine {}".format(machine_id)}

# user_id exits queue for machine_id
@app.delete("/leave/{machine_id}/{user_id}")
def leave_queue(machine_id: str, user_id: str):

    if user_id not in users:
        raise HTTPException(status_code=400, detail="User does not exist")
    if machine_id not in machine_queues:
        raise HTTPException(status_code=400, detail="Machine not in list")
    if machine_id not in machine_queues or user_id not in machine_queues[machine_id]:
        raise HTTPException(status_code=404, detail="User not found in the queue for machine {}".format(machine_id))
    
    machine_queues[machine_id].remove(user_id)
    user_queues[user_id].remove(machine_id)
    return {"message": "You have successfully left the queue for machine {}".format(machine_id)}

# returns the number of people in queue for machine_id
@app.get("/waiting/{machine_id}")
def get_queue_count(machine_id: str):

    if machine_id not in machine_queues:
        raise HTTPException(status_code=404, detail="Machine {} not found".format(machine_id))
    
    return {"count": len(machine_queues[machine_id])}

# returns the queues that user_id is currently waiting in
@app.get("/queues/{user_id}")
def get_user_queue_count(user_id: str):

    if user_id not in users:
        raise HTTPException(status_code=400, detail="User does not exist")
    if user_id not in user_queues:
        return {"count": 0, "queues": []}
    
    return {"count": len(user_queues[user_id]), "queues": user_queues[user_id]}

