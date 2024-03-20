from flask import jsonify
import json

aa = [{"match_id": "3", "ticket_category": "C", "serial_no": "5"}, {"match_id": "4", "ticket_category": "A", "serial_no": "6"}]

# can you jsonify this
print(json.dumps(aa))

## jsonify will give you the following output
print(jsonify(aa)) # TypeError: Object of type 'list' is not JSON serializable