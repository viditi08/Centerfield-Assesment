def process_event_stream(events, buffer_size=3, debug=False):
    results = []
    buffer = []
    
    # Handle empty events list
    if not events:
        return results
    
    for event in events:
        # Validating the incoming events to check structure ( ignoring missing events if anything is missing )
        if not all(key in event for key in ['event_id', 'timestamp', 'value', 'metadata']):
            continue  
            
        # Added placeholder for userid if its missing
        if 'user_id' not in event.get('metadata', {}):
            event['metadata']['user_id'] = 'unknown'
            
        # Add to buffer
        buffer.append(event)
        
        # processing only till buffer size 
        if len(buffer) >= buffer_size:
            if debug:
                # Debug mode: 
                for buffered_event in buffer:
                    print(f"Debug: {buffered_event}")
            else:
                # Regular mode:
                values = [e['value'] for e in buffer]
                user_ids = set(e['metadata']['user_id'] for e in buffer)
                
                result = {
                    'avg_value': sum(values) / len(values) if values else 0,
                    'max_value': max(values) if values else 0,
                    'unique_users': len(user_ids)
                }
                results.append(result)
                
            buffer = []
    
    # Process any remaining events 
    if buffer and not debug:
        values = [e['value'] for e in buffer]
        user_ids = set(e['metadata']['user_id'] for e in buffer)
        
        result = {
            'avg_value': sum(values) / len(values) if values else 0,
            'max_value': max(values) if values else 0,
            'unique_users': len(user_ids)
        }
        results.append(result)
    elif buffer and debug:
        # Debug mode for remaining events
        for buffered_event in buffer:
            print(f"Debug: {buffered_event}")
    
    return results

def main():    
    # Test Case 1: Normal operation (from example)
    events1 = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "value": 40.0, "metadata": {"user_id": "u3"}},
    ]
    
    # Test Case 2: Empty events list
    events2 = []
    
    # Test Case 3: Buffer size larger than number of events
    events3 = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 15.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 25.0, "metadata": {"user_id": "u2"}},
    ]
    
    # Test Case 4: Events with missing keys
    events4 = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},  # Missing event_id
        {"event_id": "e3", "value": 30.0, "metadata": {"user_id": "u1"}},  # Missing timestamp
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "metadata": {"user_id": "u3"}},  # Missing value
        {"event_id": "e5", "timestamp": "2025-04-01T10:00:04Z", "value": 50.0},  # Missing metadata
    ]
    
    # Test Case 5: Events with missing user_id in metadata
    events5 = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {}},  # Missing user_id
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
    ]
    
    # Test Case 6: Debug mode
    events6 = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
    ]
    
    # Test Case 7: Multiple batches
    events7 = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "value": 40.0, "metadata": {"user_id": "u3"}},
        {"event_id": "e5", "timestamp": "2025-04-01T10:00:04Z", "value": 50.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e6", "timestamp": "2025-04-01T10:00:05Z", "value": 60.0, "metadata": {"user_id": "u4"}},
        {"event_id": "e7", "timestamp": "2025-04-01T10:00:06Z", "value": 70.0, "metadata": {"user_id": "u1"}},
    ]
    
    # Test Case 8: Negative buffer size
    events8 = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
    ]

    # Run and compare both implementations on all test cases
    test_cases = [
        ("Test Case 1: Normal operation", events1, 3, False),
        ("Test Case 2: Empty events list", events2, 3, False),
        ("Test Case 3: Buffer size larger than events", events3, 5, False),
        ("Test Case 4: Events with missing keys", events4, 2, False),
        ("Test Case 5: Missing user_id in metadata", events5, 2, False),
        ("Test Case 6: Debug mode", events6, 2, True),
        ("Test Case 7: Multiple batches", events7, 2, False),
        ("Test Case 8: Negative buffer size", events8, -1, False),
    ]

    for test_name, events, buffer_size, debug in test_cases:
        print(f"\n{test_name}")
        result_basic = process_event_stream(events, buffer_size, debug)
        print(f"Result: {result_basic}")
    
if __name__ == "__main__":
    main()