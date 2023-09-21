import platform
import json
import thumbnail


def lambda_handler(event, _):
    print("System Architecture: ", platform.machine())
    print("Event: \n", json.dumps(event, indent=4))
    thumbnail.generate_thumbnail(
        event["in_file"], event["out_dir"], 'png', event["options"] if "options" in event else None)
