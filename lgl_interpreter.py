import array
from datetime import datetime
from random import randint
import sys
import json
from time import time


"""
Operations
"""
def do_kreieren_array(envs, args):
    #creates an array with empty lots like ["create_array", 3] == ['', '', '']
    # create arrays of fixed size
    #value of position i in array (finding, editing)
    #pass
    assert len(args) == 1
    size = do(envs, args[0])
    return ["" for i in range(size)]


def do_array_standort(envs, args):
    #["array_location", ["create_array", 5], 3]
    assert len(args) == 2
    location = do(envs, args[1])
    array = do(envs, args[0])
    return array[location]


def do_setzen_array_wert(envs, args):
    #["set_array_value", ["create_array", 3], 0, 24] == [24, '', '']
    assert len(args) == 3
    location = do(envs, args[1])
    array = do(envs, args[0])
    content = do(envs, args[2])
    array[location] = content
    return array


def do_klasse(envs, args):
    assert len(args) == 2
    class_name = args[0]
    class_body = args[1]
    class_body = do(envs, class_body)
    class_body['_envs'] = [{}]
    class_body['_class'] = class_name
    envs_set(envs, class_name, class_body)
    return ["class", class_name, class_body]


def do_abfolge(envs,args):
    assert len(args) > 0
    for operation in args:
        result = do(envs,operation)
    return result


def do_drucken(envs, args):
    assert args
    statement = do(envs, args[0])
    print(statement)
    return ""


def do_addieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return round(left + right, 2)


def do_absolutwert(envs, args):
    assert len(args) == 1
    value = do(envs, args[0])
    return abs(value)


def do_subtrahieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return round(left - right, 2)


def do_multiplizieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return round(left * right, 2)


def do_potenzieren(envs, args):
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs, args[1])
    return round(left ** right, 2)


def do_dividieren(envs, args):
    assert len(args) == 2
    left = do(envs,args[0])
    right = do(envs, args[1])
    n = left / right
    return round(n, 2)


def do_funktion(_envs, args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion", params, body]


def do_waehrend(envs, args):
    assert len(args) == 4
    counter = do(envs, args[0])
    limit = do(envs, args[2])
    list_operators = ["<", ">", "<=", ">="]
    result = 0
    assert args[1] in list_operators
    if args[1] == "<=":
        while counter <= limit:
            result = do(envs, args[3])
            counter += 1
    if args[1] == ">=":
        while counter >= limit:
            result = do(envs, args[3])
            counter -= 1
    if args[1] == "<":
        while counter < limit:
            result = do(envs, args[3])
            counter += 1
    if args[1] == ">":
        while counter > limit:
            result = do(envs, args[3])
            counter -= 1
    
    return result


def do_wortb(envs, args):
    assert len(args) % 2 == 0
    result = {}
    for i in range(0, len(args), 2):
        key = args[i]
        value = do(envs, args[i + 1])
        result[key] = value
    return result


def do_wortb_wert(envs, args):
    assert len(args) == 2
    dictionary = do(envs, args[0])
    key = do(envs, args[1])
    return dictionary[key]


def do_wortb_wert_setzen(envs, args):
    assert len(args) == 3
    dictionary = do(envs, args[0])
    key = do(envs, args[1])
    value = do(envs, args[2])
    dictionary[key] = value
    return value

def do_wortb_zusammenfuehren(envs, args):
    assert len(args) == 3
    left = do(envs, args[0])
    right = do(envs, args[1])
    operator = do(envs, args[2])
    assert operator == "|"
    result = left.copy()
    result.update(right)
    return result


def log_event(call_id, function_name, event):
    global TRACE_ENABLED
    if not TRACE_ENABLED:
        return

    global TRACE

    now = time()
    now_str = datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S.%f")
    
    TRACE.append((call_id, function_name, event, now_str))


def with_logging(func):
    def wrapper(*args, **kwargs):
        function_name = args[3]

        # Skip internal evaluations
        if isinstance(function_name, list):
            return func(*args, **kwargs)

        # Generate a random 6-digit number to identify the call
        call_id = randint(100000, 999999)

        log_event(call_id, function_name, "start")
        result = func(*args, **kwargs)
        log_event(call_id, function_name, "stop")
        
        return result
    
    return wrapper


def do_aufrufen(envs, args):
    assert len(args) >= 1

    first_argument = do(envs, args[0])

    # Allow class instance to be passed as the first object to evaluate
    # the method on the class instance.
    if isinstance(first_argument, dict) and ('_class' in first_argument or '_classname' in first_argument):
        assert len(args) >= 2

        class_object = first_argument
        name = args[1]
        arguments = args[2:]

        if '_classname' in class_object:
            class_object = envs_get(envs, class_object['_classname']) | class_object
            arguments = [class_object, *args[2:]]
    else:
        class_object = None
        name = first_argument
        arguments = args[1:]

    if class_object:
        func = find_method(envs, class_object, name)
    else:
        func = envs_get(envs, name) if isinstance(name, str) else name
    
    # eager evaluation
    values = [do(envs, arg) for arg in arguments]

    return run_method(envs, func, class_object, name, values)


@with_logging
def run_method(envs, func, class_object, name, values):
    assert isinstance(func, list)
    assert func[0] == "funktion"
    func_params = func[1]
    assert len(func_params) == len(values)

    local_frame = dict(zip(func_params, values))
    envs.append(local_frame)
    body = func[2]

    if class_object:
        result = call_method(envs + class_object['_envs'], class_object, name, values)
    else:
        result = do(envs, body)

    envs.pop()
    return result


def do_setzen(envs, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs, args[1])
    if isinstance(envs[-1], dict) and '_class' in envs[-1]:
        envs[-1][var_name] = value
    else:
        envs_set(envs, var_name, value)
    return value


def do_abrufen(envs, args):
    assert len(args) == 1
    return envs_get(envs, args[0])


"""
Helper functions
"""

def find_method(envs, cls, method_name):
    while cls is not None:
        if isinstance(cls, str):
            cls = envs_get(envs, cls)
        if method_name in cls:
            return cls[method_name]
        try:
            cls = cls["_parent"]
        except KeyError:
            cls = None
    raise NotImplementedError(f"Method not found: {method_name}")


def call_method(envs, obj, method_name, args):
    method = find_method(envs, obj, method_name)
    return do(envs + obj['_envs'], ["aufrufen", method, *args])


def create_object(envs, cls, args):
    obj = {"_class": cls, "_envs": cls['_envs']}
    for key, value in cls.items():
        if key != "_parent" and key != "_envs":
            obj[key] = value
    if "_init" in obj:
        call_method(envs + obj['_envs'], obj, "_init", args)
    return obj


def envs_get(envs, name):
    assert isinstance(name, str)
    for e in reversed(envs):
        if name in e:
            return e[name]
    
    assert False, f"Unknown variable name {name}"


def envs_set(envs,name,value):
    assert isinstance(name,str)
    envs[-1][name] = value


OPERATIONS = {
    func_name.replace("do_",""): func_body
    for (func_name, func_body) in globals().items()
    if func_name.startswith("do_")
}


def do(envs, expr):
    if isinstance(expr, int) or isinstance(expr, str) or isinstance(expr, dict) or isinstance(expr, float):
        return expr
   
    assert isinstance(expr, list)
    assert expr[0] in OPERATIONS, f"Unknown operation {expr[0]}"

    func = OPERATIONS[expr[0]]
    result = func(envs, expr[1:])
    if isinstance(result, list) and result[0] is OPERATIONS:
        result = do(envs, func)

    return result


def main():
    global TRACE_ENABLED
    global TRACE

    if len(sys.argv) > 2 and sys.argv[2] == "--trace":
        TRACE_ENABLED = True
        TRACE = []
        assert len(sys.argv) == 4, "Usage: funcs-demo.py filename.gsc --trace trace-output.log"
    else:
        TRACE_ENABLED = False
        assert len(sys.argv) == 2, "Usage: funcs-demo.py filename.gsc"

    with open(sys.argv[1], "r") as source_file:
        program = json.load(source_file)
    assert isinstance(program, list)
    envs = [{}]
    result = do(envs, program)

    print(f"=> {result}")

    if TRACE_ENABLED:
        trace_output_filename = sys.argv[3]
        with open(trace_output_filename, "w") as trace_output_file:
            trace_output_file.write("id,function_name,event,timestamp\n")
            for call_id, function_name, event, timestamp in TRACE:
                trace_output_file.write(f"{call_id},{function_name},{event},{timestamp}\n")


if __name__ == "__main__":
    main()
