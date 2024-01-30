from storage import supabase

def getAttendee(name, day):
    request = supabase.table('attendees').select(
        "*").eq("name", name).eq("day", day).execute()
    return len(request.data)
    
def addAttendee(name: str, location: int = 0):
    data = supabase.table('attendees').insert(
        {"name": name, "location": location}).execute()

    print("Successfully added: ", data)