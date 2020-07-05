from llamalogs.llamaLogs import LlamaLogs
from llamalogs.logAggregator import LogAggregator

def test_init():
    LlamaLogs.init({"graphName": "firstG", "accountKey": "keyKey"})

    params = {
        "sender": "Server", 
        "receiver": "Database"
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()
    
    assert len(log_list) == 1
    log = log_list[0]
    assert log["account"] == 'keyKey'
    assert log["sender"] == 'Server'
    assert log["receiver"] == 'Database'
    assert log["message"] == ''
    assert log["errorMessage"] == ''
    assert log["graph"] == 'firstG'
    assert log["count"] == 1
    assert log["errorCount"] == 0
    assert log["clientTimestamp"] > 0

def test_remove_init():
    LlamaLogs.init({"graphName": "", "accountKey": ""})

    params = {
        "sender": "Server", 
        "receiver": "Database"
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()
    # rejects because graphname / account is empty
    assert len(log_list) == 0

def test_disabled_init():
    LlamaLogs.init({"disabled": True })

    params = {
        "sender": "Server", 
        "receiver": "Database",
        "accountKey": "acc2",
        "graphName": "g1"
    }

    LlamaLogs.log(params)
    log_list, _stat_list = LogAggregator.gather_messages()

    assert len(log_list) == 0
    # turning off for other tests
    LlamaLogs.init({"disabled": False })

def test_stop():
    LlamaLogs.init()
    assert LlamaLogs.commThread is not None
    LlamaLogs.stop()
    assert LlamaLogs.commThread is None