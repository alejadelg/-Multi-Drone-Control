from codrone_edu.drone import Drone
import time
import datetime
import threading


# Dictionary of drone with their port
ports = ['COM25','COM26','COM27','COM28']
drones = {i+1: Drone() for i in range(len(ports))}

# Function to register and show the time
def log_time(action):
    timestamp = time.time()  # actual time con microsegundos
    formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  
    print(f"[SYNC] {action} - Tiempo: {formatted_time}")
    return timestamp

# conect  cada dron a su puerto correspondiente
for i in drones:
    drones[i].pair(ports[i-1])

def control_drone(drone, drone_id, command):
    """Ejecuta el comando en el dron dado."""
    if command == "a":
        
        drone.takeoff()
        drone.set_pitch(30)
        drone.move(3)
        drone.set_pitch(0)
        drone.set_roll(-30)
        drone.move(2)
        drone.set_roll(0)
        drone.set_pitch(-30)
        drone.move(3)
        drone.set_pitch(0)
        drone.land()
 
    else:
        print(f"[Dron {drone_id}] Comando no reconocido: {command}")

    exec_time = log_time("Comando ejecutado: a")
        
    print(f"[Dron {drone_id}] Latencia: {exec_time - recived_time:.6f} segundos-")


# Bucle para recibir comandos y ejecutarlos en todos los drones
while True:
    command = input("Ingresa un comando para todos los drones ('exit' para salir): ").strip().lower()
    recived_time = log_time(f"Comando enviado: {command}")
    
    if command == "exit":
        print("Desconectando drones...")
        for drone in drones.values():
            drone.close()
        break

    # Crear hilos para ejecutar el comando en paralelo

    #quita esto a ver que pasa... 
    
    threads = [threading.Thread(target=control_drone, args=(drones[i], i, command)) for i in drones]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
