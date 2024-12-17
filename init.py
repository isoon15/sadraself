from Database import initialize_database 
from Functions import ConfigHandler


async def initilize():
    await initialize_database() 
    initial = {
        'price_text': 'نرخ سلف تنظیم نشده است', 
        'guide_text': 'متن راهنما تنطیم نشده است', 
        'what_self': 'none', 
        'status':"on",
        "agency_text": "none",
        "agency_status": "on"
        
        
    }
    for i in initial.items(): 
        await ConfigHandler.update_status(i[0], i[1])
    