from Functions import Server_Handler, Account_handler 
import asyncio 

ac_info = {
    "server_ip": "141.8.194.203",
    "server_username": "a1012177", 
    "server_password": "cuseucpeug", 
    "phone_number": "+989934525143", 
    "api_id": 25683863,
    "api_hash": "09ddab1458cf53dc3b0f6fde23b323b7"
    
}
my_id = 6463237499
async def main(): 
    await Server_Handler.run_bot(ac_info=ac_info)


text = "Stability and bifurcation analysis in a discrete SIR epidemic mode"

a = text.split(" ")

a.reverse() 

joined_string = ' '.join(a)
print(joined_string) 
    
    