from llamalogs.llamaLogs import LlamaLogs
from llamalogs.logAggregator import LogAggregator

def test_log_no_message():
    params = {
        "sender": "Server", 
        "receiver": "Database", 
        "graphName": "secondary-sub-graph", 
        "accountKey": "testKey"
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()
    
    assert len(log_list) == 1
    log = log_list[0]
    assert log["account"] == 'testKey'
    assert log["sender"] == 'Server'
    assert log["receiver"] == 'Database'
    assert log["message"] == ''
    assert log["errorMessage"] == ''
    assert log["graph"] == 'secondary-sub-graph'
    assert log["count"] == 1
    assert log["errorCount"] == 0
    assert log["clientTimestamp"] > 0

def test_log_message():
    params = {
        "sender": "Server", 
        "receiver": "Database", 
        "graphName": "secondary-sub-graph", 
        "accountKey": "testKey",
        "message": "this is a message"
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()
    
    assert len(log_list) == 1
    log = log_list[0]
    assert log["account"] == 'testKey'
    assert log["sender"] == 'Server'
    assert log["receiver"] == 'Database'
    assert log["message"] == 'this is a message'
    assert log["errorMessage"] == ''
    assert log["graph"] == 'secondary-sub-graph'
    assert log["count"] == 1
    assert log["errorCount"] == 0
    assert log["clientTimestamp"] > 0

def test_log_error_message():
    params = {
        "sender": "Server", 
        "receiver": "Database", 
        "graphName": "secondary-sub-graph", 
        "accountKey": "testKey",
        "message": "this is a message",
        "isError": True
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()
    
    assert len(log_list) == 1
    log = log_list[0]
    assert log["account"] == 'testKey'
    assert log["sender"] == 'Server'
    assert log["receiver"] == 'Database'
    assert log["message"] == ''
    assert log["errorMessage"] == 'this is a message'
    assert log["graph"] == 'secondary-sub-graph'
    assert log["count"] == 1
    assert log["errorCount"] == 1
    assert log["clientTimestamp"] > 0

def test_multiple_logs():
    params = {
        "sender": "Server", 
        "receiver": "Database", 
        "graphName": "secondary-sub-graph", 
        "accountKey": "testKey",
        "message": "this is a message",
        "isError": False
    }

    LlamaLogs.log(params)

    params["isError"] = True
    params["message"] = "errorMessage"
    LlamaLogs.log(params)

    params["isError"] = False
    params["message"] = "original Message"
    params["receiver"] = "otherComp"
    LlamaLogs.log(params)

    params["sender"] = "thirdSender"
    LlamaLogs.log(params)
    
    log_list, _stat_list = LogAggregator.gather_messages()
    
    assert len(log_list) == 3
    log = log_list[0]
    assert log["account"] == 'testKey'
    assert log["sender"] == 'Server'
    assert log["receiver"] == 'Database'
    assert log["message"] == 'this is a message'
    assert log["errorMessage"] == 'errorMessage'
    assert log["graph"] == 'secondary-sub-graph'
    assert log["count"] == 2
    assert log["errorCount"] == 1
    assert log["clientTimestamp"] > 0

    second_log = log_list[1]
    assert second_log["account"] == 'testKey'
    assert second_log["sender"] == 'Server'
    assert second_log["receiver"] == 'otherComp'
    assert second_log["message"] == 'original Message'
    assert second_log["errorMessage"] == ''
    assert second_log["graph"] == 'secondary-sub-graph'
    assert second_log["count"] == 1
    assert second_log["errorCount"] == 0
    assert second_log["clientTimestamp"] > 0

    third_log = log_list[2]
    assert third_log["account"] == 'testKey'
    assert third_log["sender"] == 'thirdSender'
    assert third_log["receiver"] == 'otherComp'
    assert third_log["message"] == 'original Message'
    assert third_log["errorMessage"] == ''
    assert third_log["graph"] == 'secondary-sub-graph'
    assert third_log["count"] == 1
    assert third_log["errorCount"] == 0
    assert third_log["clientTimestamp"] > 0

def test_log_no_sender():
    params = {
        "receiver": "Database", 
        "graphName": "secondary-sub-graph", 
        "accountKey": "testKey"
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()
    
    assert len(log_list) == 0

def test_log_no_receiver():
    params = {
        "sender": "send",
        "graphName": "secondary-sub-graph", 
        "accountKey": "testKey"
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()
    
    assert len(log_list) == 0