import json

def extract_text_from_rich_json(content):
    """
    Recursively extracts text from a Lexical/RichText JSON structure.
    Handles paragraphs, lists, and indentation.
    """
    node = json.loads(content)
    text_content = ""
    
    print(node)
     
    # 1. Handle Leaf Nodes (Text)
    # If the node contains direct text, we grab it.
    if "text" in node:
        text_content += node["text"]

    # 2. Handle Children (Recursion)
    # If the node has children, we process them in order.
    if "children" in node:
        for child in node["children"]:
            text_content += extract_text_from_rich_json(child)

    # 3. Apply Formatting based on Node Type
    node_type = node.get("type", "")

    # Add a newline after paragraphs
    if node_type == "paragraph":
        # Only add newline if there is actual content or if it's acting as a spacer
        return text_content + "\n"
    
    # Handle List Items (add a bullet point)
    elif node_type == "listitem":
        return f"- {text_content}\n"
    
    # Handle Lists (add extra spacing around the list)
    elif node_type == "list":
        return text_content + "\n"

    # For root or generic wrappers, just return the accumulated content
    return text_content