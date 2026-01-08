from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary using a key, trying both string and int if needed"""
    if not isinstance(dictionary, dict):
        return None
        
    # Try the key as provided (usually a string in templates)
    val = dictionary.get(key)
    if val is not None:
        return val
        
    # Try as string if it was an int
    val = dictionary.get(str(key))
    if val is not None:
        return val
        
    # Try as int if it was a string
    try:
        val = dictionary.get(int(key))
        if val is not None:
            return val
    except (ValueError, TypeError):
        pass
        
    return None

@register.filter
def get_dict_item(dictionary, key):
    """Get item from dictionary, returns empty dict if not found (for nested access)"""
    result = get_item(dictionary, key)
    return result if result is not None else {}

