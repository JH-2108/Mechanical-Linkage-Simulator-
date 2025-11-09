import json
from linkage import Linkage
from visualize import LinkageVisualizer

example_file = "examples/four_bar_example.json"  
with open(example_file, "r") as f:
    mech_data = json.load(f)

print(f"Loaded mechanism: {mech_data['mechanism_name']}")
print(mech_data["description"])

linkage = Linkage(mech_data["links"], mech_data["joints"])
visualizer = LinkageVisualizer(linkage, mech_data["mechanism_name"])
visualizer.animate()
