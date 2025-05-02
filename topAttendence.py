def find_top_attendee(meetings):
    if not meetings:
        return []
    
    # Create a dictionary to store years attended by each person
    attendance = {}
    for person, year in meetings:
        if person not in attendance:
            attendance[person] = set()
        attendance[person].add(year)
    
    #intilization
    max_streak = 0
    top_attendees = []
    
    # Calculate the longest streak for each attendee
    for person, years in attendance.items():
        years_list = sorted(list(years))
        current_streak = 1
        max_personal_streak = 1
        
        for i in range(1, len(years_list)):
            if years_list[i] == years_list[i-1] + 2:  # Checking 2 years apart condition
                current_streak += 1
            else:
                current_streak = 1
            max_personal_streak = max(max_personal_streak, current_streak)
        
        # Update top attendees based on streak length
        if max_personal_streak > max_streak:
            max_streak = max_personal_streak
            top_attendees = [person]
        elif max_personal_streak == max_streak:
            top_attendees.append(person)
    
    # Return single name or sorted list depending on number of top attendees
    if len(top_attendees) == 1:
        return top_attendees[0]
    else:
        return sorted(top_attendees)


def main():
    # Test case 1
    meetings1 = [
        ("Alice", 2000),
        ("Alice", 2002),
        ("Alice", 2004),
        ("Bob", 2000),
        ("Bob", 2002),
        ("Charlie", 2000),
        ("Charlie", 2002),
        ("Charlie", 2004),
        ("Charlie", 2006),
    ]
    print("Test case 1 result:", find_top_attendee(meetings1)) 
    
    # Test case 2
    meetings2 = [
        ("Alice", 2000),
        ("Alice", 2002),
        ("Bob", 2000),
        ("Bob", 2002),
    ]
    print("Test case 2 result:", find_top_attendee(meetings2))  
    
    # Edge case: Empty list
    print("Empty list result:", find_top_attendee([]))  
    
    # Edge case: Single attendee
    meetings3 = [("Dave", 2010)]
    print("Single attendee result:", find_top_attendee(meetings3))  
    
    # Edge case: Non-consecutive years
    meetings4 = [
        ("Eve", 2000),
        ("Eve", 2003),
        ("Eve", 2006),
    ]
    print("Non-consecutive years result:", find_top_attendee(meetings4))  
    
    # Edge case: Duplicate entries
    meetings5 = [
        ("Frank", 2000),
        ("Frank", 2000),
        ("Frank", 2002),
        ("Frank", 2004),
    ]
    print("Duplicate entries result:", find_top_attendee(meetings5))  

if __name__ == "__main__":
    main()